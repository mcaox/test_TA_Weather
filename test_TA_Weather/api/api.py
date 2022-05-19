from pathlib import Path

import joblib


import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from test_TA_Weather.assets.model import ModelGetter

import uvicorn


DATE_URL_FMT = "%Y"
URL_PREDICT = "?date=2022-05-01&latitude=-73.9996&longitude=40.6501&altitude=40.6501&dd=-73.9496&ff=1&t=30&u=0&pres=0&dd_sin=0&dd_cos=0"


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# define a root `/` endpoint
@app.get("/")
def index():
    return {"Status": "Up and running"}


@app.get("/predict")
def predict(date:str,
latitude:float,
longitude:float,
altitude:float,
dd:float,
ff:float,
t:float,
u:float,
pres:float,
dd_sin:float,
dd_cos:float):
    message = ""
    try:
        pd.to_datetime(date)
    except:
        message = f"{date} non reconnue"

    dd = {
        "date":date,
        "Latitude":latitude,
        "Longitude":longitude,
        "Altitude":altitude,
        "dd":dd,
        "ff":ff,
        "t":t,
        "u":u,
        "pres":pres,
        "dd_sin":dd_sin,
        "dd_cos":dd_cos
    }
    X = pd.DataFrame(dd,index=[0])
    y_pred = ModelGetter.get().predict(X)
    if message:
        return {
            "pluvieux": 0,
            "error": 1,
            "message":message
        }
    else:
        return {
            "pluvieux": y_pred[0],
            "error": 0,
            "message":""
        }





