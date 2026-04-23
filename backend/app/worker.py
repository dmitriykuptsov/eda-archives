from celery import Celery
from app.db import SessionLocal
from app.models import Order
from app.prompts import generate_facts, generate_movie_fact, generate_song_fact, generate_prices_and_trands, generate_astrology_facts
from app.utils import get_date_formatted
from PIL import Image
import qrcode
from weasyprint import HTML
from jinja2 import Template
import os
from io import BytesIO
import base64
from app.email_helper import send_download_link
from app.stars import get_coordinates
from app.stars import get_stars
from app.stars import get_stars_visible
from datetime import datetime
import io

celery = Celery(__name__, broker="redis://redis:6379/0")

OUTPUT_DIR = os.getenv("REPORT_DIR") if os.getenv("REPORT_DIR") else "/storage/reports"
os.makedirs(OUTPUT_DIR, exist_ok=True)
REPORT_TEMPLATE = os.getenv("REPORT_TEMPLATE") if os.getenv("REPORT_TEMPLATE") else "/storage/templates"
os.makedirs(REPORT_TEMPLATE, exist_ok=True)
HTML_TEMPLATE = open(REPORT_TEMPLATE + "/template_old.html", "r").read()

print(HTML_TEMPLATE)

def pil_to_base64(img: Image.Image) -> str:
    buffer = BytesIO()
    img.save(buffer, format="PNG")  # or JPEG
    img_bytes = buffer.getvalue()

    base64_str = base64.b64encode(img_bytes).decode("utf-8")

    return f"data:image/jpg;base64,{base64_str}"

@celery.task
def generate_report(order_id):
    print("___________^^_____________")
    print(".....Starting Celary task.....")
    print("___________^^_____________")
    db = SessionLocal()
    order = db.query(Order).get(order_id)
    if not order:
        return
    # 1. Generate facts, movies, and songs
    news = generate_facts(order.date)
    movie = generate_movie_fact(order.date)
    song = generate_song_fact(order.date)
    trends = generate_prices_and_trands(order.date)
    astrology = generate_astrology_facts(order.date)
    # 2. Process image
    img = Image.open(order.image_path).convert("L")
    img_base64 = pil_to_base64(img)
    buf = io.BytesIO()
    qr = qrcode.QRCode()
    qr.add_data(f"https://eda-archives.com/order_id={order_id}&secret={order.secret}")
    img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    data = img.getdata()
    new_data = []
    for item in data:
        if item[:3] == (255, 255, 255):
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    img.putdata(new_data)
    img.save(buf, format="PNG")
    buf.seek(0)
    personal_url = f"data:image/jpg;base64,{base64.b64encode(buf.read()).decode('utf-8')}"
    #stars = get_stars()
    #(lat, lng) = get_coordinates(order.location)
    ##sky_base64 = f"data:image/png;base64,{plot_stars(5, stars, order.date, lat, lng)}"
    #stars = get_stars_visible(5, stars, order.date, lat, lng)
    # 4. Render HTML
    html = Template(HTML_TEMPLATE).render(
        name=order.name,
        date=order.date,
        location=order.location,
        order_id=order_id,
        date_formatted=get_date_formatted(datetime.strptime(order.date, "%d.%m.%Y")),
        news=news,
        movie=movie,
        song=song,
        trends=trends,
        astrology=astrology,
        photo=img_base64,
        personal_url=personal_url
    )
    # 5. Generate PDF
    pdf_path = f"{OUTPUT_DIR}/report_{order_id}.pdf"
    HTML(string=html).write_pdf(pdf_path)
    # 6. Save result
    order.pdf_path = pdf_path
    order.status = "done"
    db.commit()
    # 6. Send the download link to the user
    send_download_link(order.email, str(order.id), order.secret)
    print(f"Report generated: {pdf_path}")
    
