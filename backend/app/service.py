from app.db import SessionLocal
from app.models import Order
from app.worker import generate_report

def create_order(secret, date, location, name, email, image_path):
    db = SessionLocal()
    order = Order(
        secret=secret,
        date=date,
        location=location,
        image_path=image_path,
        name=name,
        email=email,
        status="pending"
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def trigger_task(order_id):
    generate_report.delay(order_id)

