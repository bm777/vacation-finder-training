from fastapi import FastAPI
from random import choice

app = FastAPI()

fake_data = [
    23, 37, 25, 28, 39, 37
]

@app.get("/temp")
def get_temp(date_forecast: str):
    return {
    "type": "Temperature in °C",
    "response": choice(fake_data)
    }
