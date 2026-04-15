from celery import Celery
from app.db import SessionLocal
from app.models import Order
from app.prompts import generate_facts, generate_movies, generate_songs, generate_prices
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
    facts = generate_facts(order.date).get("headlines", [])
    movies = generate_movies(order.date).get("movies", [])
    songs = generate_songs(order.date).get("songs", [])
    prices = generate_prices(order.date).get("items", [])

    # 2. Process image
    img = Image.open(order.image_path).convert("L")
    img_base64 = pil_to_base64(img)

    qr = qrcode.make(f"https://www.youtube.com/results?search_query={songs[0]['title']}")
    buf = io.BytesIO()
    qr.save(buf, format="jpeg")
    buf.seek(0)
    qr_spotify = f"data:image/jpg;base64,{base64.b64encode(buf.read()).decode('utf-8')}"

    qr = qrcode.make(f"https://www.imdb.com/find/?q={movies[0]['title']}")
    buf = io.BytesIO()
    qr.save(buf, format="jpeg")
    buf.seek(0)
    qr_imdb = f"data:image/jpg;base64,{base64.b64encode(buf.read()).decode('utf-8')}"

    stars = get_stars()
    (lat, lng) = get_coordinates(order.location)
    #sky_base64 = f"data:image/png;base64,{plot_stars(5, stars, order.date, lat, lng)}"
    stars = get_stars_visible(5, stars, order.date, lat, lng)

    # 4. Render HTML
    html = Template(HTML_TEMPLATE).render(
        name=order.name,
        date=order.date,
        location=order.location,
        facts=facts,
        movies=movies,
        songs=songs,
        prices=prices,
        photo=img_base64,
        stars=stars,
        spotify=qr_spotify,
        imdb=qr_imdb
    )

    # 5. Generate PDF
    pdf_path = f"{OUTPUT_DIR}/report_{order_id}.pdf"
    HTML(string=html).write_pdf(pdf_path)

    html_path = f"{OUTPUT_DIR}/report_{order_id}.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    # 6. Save result
    order.pdf_path = html_path
    order.status = "done"
    db.commit()

    send_download_link(order.email, str(order.id), order.secret)

    print(f"Report generated: {html_path}")
    