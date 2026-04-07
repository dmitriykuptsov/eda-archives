from fastapi import APIRouter, UploadFile, File, Form, Request, FileResponse
from app.services import create_order, trigger_task
from app.db import SessionLocal
from app.models import Order
from utils import hash_bytes, validate_jpeg, is_jpeg_magic
import stripe
import os
import re
from os import urandom
from binascii import hexlify

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

router = APIRouter()

UPLOAD_DIR = os.getenv("UPLOAD_DIR") if os.getenv("UPLOAD_DIR") else "/storage/uploads"
OUTPUT_DIR = os.getenv("OUTPUT_DIR") if os.getenv("OUTPUT_DIR") else "/storage/reports"
PAYMENT_PER_PRODUCT = 2900

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@router.post("/order")
async def create_order_with_payment(
    date: str = Form(...),
    location: str = Form(...),
    name: str = Form(...),
    email: str = Form(...),
    file: UploadFile = File(...)
):
    
    if not re.match(r"^[0-9A-Za-z_]+.(JPG|JPEG)$", file.filename):
        return {
            "success": False, 
            "reason": "Invalid filename. Should be JPG or JPEG file"
        }
    
    if not re.match(r"^[A-Za-z]+,\s{0,1}[A-Z]{2}$", location):
        return {
            "success": False, 
            "reason": "Invalid location. Should be city, state"
        }
    
    if not re.match(r"^[A-Za-z\_0-9\.\-]+@[A-Za-z0-9]+\.[a-z]+$", email):
        return {
            "success": False, 
            "reason": "Invalid email address"
        }
    
    if not re.match(r"^[0-9]{2}\.[0-9]{2}\.[0-9]{4}$", date):
        return {
            "success": False, 
            "reason": "Invalid birth date. Should be dd.mm.YYYY"
        }
    
    file_bytes = await file.read()

    if not validate_jpeg(file_bytes) or not is_jpeg_magic(file_bytes):
        return {
            "success": False, 
            "reason": "Invalid image file. Should be JPEG file"
        }
    
    file_path = f"{UPLOAD_DIR}/{str(hash_bytes(file_bytes))}.JPEG"
    with open(file_path, "wb") as f:
        f.write(file_bytes)

    secret = hexlify(urandom(128)).decode("ASCII")
    order = create_order(secret, date, location, name, email, file_path)

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": "EDA-Archives Report",
                },
                "unit_amount": PAYMENT_PER_PRODUCT,
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=f"https://eda-archives.com/payment_success",
        cancel_url=f"https://eda-archives.com/payment_cancel/{order.id}",
        metadata={"order_id": order.id}
    )

    return {"checkout_url": session.url}

@router.post("/order_without_payment")
async def create_order_without_payment(
    date: str = Form(...),
    location: str = Form(...),
    name: str = Form(...),
    email: str = Form(...),
    file: UploadFile = File(...)
):

    if not re.match(r"^[0-9A-Za-z_]+.(JPG|JPEG)$", file.filename):
        return {
            "success": False, 
            "reason": "Invalid filename. Should be JPG or JPEG file"
        }
    
    if not re.match(r"^[A-Za-z]+,\s{0,1}[A-Z]{2}$", location):
        return {
            "success": False, 
            "reason": "Invalid location. Should be city, state"
        }
    
    if not re.match(r"^[A-Za-z\_0-9\.\-]+@[A-Za-z0-9]+\.[a-z]+$", email):
        return {
            "success": False, 
            "reason": "Invalid email address"
        }
    
    if not re.match(r"^[0-9]{2}\.[0-9]{2}\.[0-9]{4}$", date):
        return {
            "success": False, 
            "reason": "Invalid birth date. Should be dd.mm.YYYY"
        }
    
    file_bytes = await file.read()

    if not validate_jpeg(file_bytes) or not is_jpeg_magic(file_bytes):
        return {
            "success": False, 
            "reason": "Invalid image file. Should be JPEG file"
        }

    file_path = f"{UPLOAD_DIR}/{str(hash_bytes(file_bytes))}.JPEG"
    with open(file_path, "wb") as f:
        f.write(file_bytes)

    secret = hexlify(urandom(128)).decode("ASCII")
    order = create_order(secret, date, location, name, email, file_path)
    trigger_task.delay(order.id)

    return {
        "success": True, 
        "order_id": order.id
        }

@router.post("/payment_success")
async def stripe_success(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    event = stripe.Webhook.construct_event(
        payload,
        sig_header,
        os.getenv("STRIPE_WEBHOOK_SECRET")
    )

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        order_id = session["metadata"]["order_id"]

        db = SessionLocal()
        order = db.query(Order).filter(
                Order.id == order_id
            ).first()
        
        if not order:
            return {
                "success": False, 
                "reason": "Order was not found"
            }

        order.status = "paid"
        db.commit()

        trigger_task.delay(order_id)

        return {"success": True, "order_id": order_id}
    
    return {"success": False, "reason": "Payment was not completed"}


@router.post("/payment_cancel/{order_id}")
def cancel_order(order_id: int):
    db = SessionLocal()
    order = db.query(Order).filter(
                Order.id == order_id
            ).first()
    
    if not order:
        return {"sucess": False, "reason": "Order was not found"}

    if order.status == "pending":
        order.status = "cancelled"
        db.commit()

    return {"success": True, "status": "cancelled"}

@router.get("/was_paied/{order_id}/{secret}")
def was_paied(order_id: int, secret: str):
    db = SessionLocal()
    order = db.query(Order).filter(
                Order.id == order_id,
                Order.secret == secret
            ).first()

    if not order:
        return {"success": False, "reason": "Order was not found"}

    if order.status != "paid" or order.status != "done":
        return {"success": False, "reason": "Order was not paid"}

    return {"success": True, "status": "paid"}

@router.get("/is_ready/{order_id}/{secret}")
def is_ready(order_id: int, secret: str):
    db = SessionLocal()
    order = db.query(Order).filter(
                Order.id == order_id,
                Order.secret == secret
            ).first()

    if not order:
        return {"success": False, "reason": "Order was not found"}

    if order.status != "done":
        return {"success": False, "reason": "Order is not ready"}

    return {"success": True, "status": "done"}

@router.get("/download/{order_id}/{secret}")
def download_pdf(order_id: int, secret: str):
    db = SessionLocal()
    order = db.query(Order).filter(
                Order.id == order_id,
                Order.secret == secret
            ).first()

    if not order:
        return {"success": False, "reason": "Order was not found"}

    if order.status != "done":
        return {"success": False, "reason": "Order is not ready"}

    if not order.pdf_path or not os.path.exists(order.pdf_path):
        return {"success": False, "reason": "File was not found"}

    return FileResponse(
        path=order.pdf_path,
        media_type="application/pdf",
        filename=f"eda_report_{order_id}.pdf"
    )
