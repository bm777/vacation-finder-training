import uvicorn
import pandas as pd
from fastapi import FastAPI
from Model import get_prediction

app = FastAPI()

## load temperature predictor


@app.get("/temp")
def get_temp(date_forecast: str):
    # red model and get prediction
    df = pd.read_pickle("temp_model.pkl")
    pred = get_prediction(df, date_forecast)
    pred_in_C = (pred - 32) * 5/9
    return {
    "type": "Temperature in °C",
    "response": pred_in_C
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
