from openai import OpenAI
import os
from json import loads

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

model=os.getenv("OPENAI_API_MODE") if os.getenv("OPENAI_API_MODE") else "gpt-5.4"

def generate_facts(date):
    response = client.chat.completions.create(
        model=model,
        messages=[{
            "role": "user",
            "content": f"Respond in clean HTML only. Use <b> tags. No markdown. Describe in two, three sentences what have happened on {date} without politics, include several major events. Please, include 3 facts but omit the music and movies."
        }]
    )
    return response.choices[0].message.content

def generate_astrology_facts(date):
    response = client.chat.completions.create(
        model=model,
        messages=[{
            "role": "user",
            "content": f"Respond in clean HTML only. Use <b> tags. No markdown. Give the description of the astrological facts for the {date}. Provide three sentences description"
        }]
    )
    return response.choices[0].message.content

def generate_movie_fact(date):
    response = client.chat.completions.create(
        model=model,
        messages=[{
            "role": "user",
            "content": f"Respond in clean HTML only. Use <b> tags. No markdown. Give the description of top movie for the {date}. Provide two sentences description."
        }]
    )
    return response.choices[0].message.content

def generate_song_fact(date):
    response = client.chat.completions.create(
        model=model,
        messages=[{
            "role": "user",
            "content": f"Respond in clean HTML only. Use <b> tags. No markdown. Give the description of top music hit for the {date}. Provide two sentences description."
        }]
    )
    return response.choices[0].message.content

def generate_prices_and_trands(date):
    response = client.chat.completions.create(
        model=model,
        messages=[{
            "role": "user",
            "content": f"Respond in clean HTML only. Use <b> tags. No markdown. Provide description of the mood of the day for {date}. Include prices for 5 major goods, include what was trending in fashion. Also include the exchange rates for the major currencies. Please keep it short 3 sentences is enough."
        }]
    )
    return response.choices[0].message.content

def generate_political_news(date):
    response = client.chat.completions.create(
        model=model,
        messages=[{
            "role": "user",
            "content": f"Respond in clean HTML only. Use <b> tags. No markdown. Provide description one or two major political events for {date}. Please keep it short."
        }]
    )
    return response.choices[0].message.content