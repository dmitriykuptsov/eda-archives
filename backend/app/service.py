from app.db import SessionLocal
from app.models import Order
from app.worker import generate_report
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

model=os.getenv("OPENAI_API_MODE") if os.getenv("OPENAI_API_MODE") else "gpt-5.4"

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

def generate_facts(date):
    response = client.chat.completions.create(
        model=model,
        messages=[{
            "role": "user",
            "content": f"Give structured JSON list of 10 worldwide historical facts for {date}. The JSON output should contain at the top level headlines element with title and description elements inside"
        }],
        response_format={"type": "json_object"}
    )
    return response.choices[0].message.content


def generate_movies(date):
    response = client.chat.completions.create(
        model=model,
        messages=[{
            "role": "user",
            "content": f"Give structured JSON list of 3 top movies for {date} worldwide. The JSON output should contain at the top level movies element with title and description elements inside"
        }],
        response_format={"type": "json_object"}
    )
    return response.choices[0].message.content

def generate_songs(date):
    response = client.chat.completions.create(
        model=model,
        messages=[{
            "role": "user",
            "content": f"Give structured JSON list of 3 hit songs for {date} worldwide. The output should contain at the top level songs element with title and description elements inside"
        }],
        response_format={"type": "json_object"}
    )
    return response.choices[0].message.content

def generate_prices(date):
    response = client.chat.completions.create(
        model=model,
        messages=[{
            "role": "user",
            "content": f"Give structured JSON list with prices for gold, gasoline, milk, break, housing for {date} in US. The output should contain at the top level item element with title and price as a single number elements inside"
        }],
        response_format={"type": "json_object"}
    )
    return response.choices[0].message.content