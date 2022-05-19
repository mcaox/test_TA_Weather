from datetime import datetime
from pathlib import Path

import joblib


import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from test_TA_Weather.assets.model import ModelGetter

import uvicorn



MEAN_LAT = 45.478172
MEAN_LONG = 3.451461
MEAN_ALT = 193.196708
MEAN_DD = 185.492402
MEAN_FF = 3.41
MEAN_T = 13.26
MEAN_U = 71.29
MEAN_PRES = 0.35


URL_PREDICT = f"?date={datetime.now().strftime('%x')}&"\
f"latitude={MEAN_LAT}&longitude={MEAN_LONG}&altitude={MEAN_ALT}&"\
f"dd={MEAN_DD}&ff={MEAN_FF}&t={MEAN_T}&u={MEAN_U}&pres={MEAN_PRES}&dd_sin=0&dd_cos=0"


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
    return {"Example": URL_PREDICT}


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


    if message:
        return {
            "pluvieux": 0,
            "error": 1,
            "message":message
        }
    else:
        X = pd.DataFrame(dd,index=[0])
        y_pred = ModelGetter.get().predict(X)
        return {
            "pluvieux": int(y_pred[0]),
            "error": 0,
            "message":""
        }
