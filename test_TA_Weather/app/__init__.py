import math
import sys
import streamlit as st
import pandas as pd
import requests
import numpy as np
from test_TA_Weather.api.api import MEAN_LAT,MEAN_LONG,MEAN_T,MEAN_U,MEAN_FF,MEAN_ALT,MEAN_DD
import folium
from streamlit_folium import folium_static,st_folium




class MyApp:
    def __init__(self,URL_BASE):
        self.URL_BASE = URL_BASE
        st.markdown("# Get the prevision")
        self.map = folium.Map(location=(MEAN_LAT,MEAN_LONG), zoom_start=16)
        self.col_loc,self.col_when = st.columns(2)
        with self.col_loc:
            self.st_map = st_folium(self.map,key="map")
            st.write(self.format_coord(self.st_map["last_clicked"]))
        with self.col_when:
            self.date = st.date_input("When ?")
            self.alt = st.number_input("Altitude ?",value=MEAN_ALT,min_value=0.0,max_value=9000.0)

        self.col_wind,self.col_pres_temp = st.columns(2)
        with self.col_wind:
            self.angle = st.slider("Wind Direction ?",min_value=0,max_value=360,value=0)
            self.force = st.number_input("Wind Force ?",min_value=0.0,value=MEAN_DD)
        
        with self.col_pres_temp:
            self.pres = st.number_input("Presure (Pa) ?",min_value=0.0,value=1013.25)
            self.temp = st.number_input("Temp (°C) ?",value=MEAN_T)
            self.hum = st.number_input("Humidity rate ?",value=MEAN_U)
        
        if st.button("Predict"):
            rain = self.get_prediction()
            s = ["☀️","☔","⚠️"]
            st.write("".join([s[rain]]*10))



    def get_prediction(self):
        lat_long = self.st_map["last_clicked"]
        if lat_long is None:
            return 2
        url = f"{self.URL_BASE}?date={self.date.strftime('%Y-%m-%d')}&"\
        f"latitude={lat_long['lat']}&longitude={lat_long['lng']}&altitude={self.alt}&"\
        f"dd={self.angle}&ff={self.force}&t={self.temp}&u={self.hum}&pres={self.pres}&dd_sin={math.sin(math.radians(self.angle))}&dd_cos={math.cos(math.radians(self.angle))}"
        resp = requests.get(
            url=url
        )
        if resp.status_code==200:
            if not int(resp.json()["error"]):
                return int(resp.json()["pluvieux"])
            print(resp.json())
        else:
            print(resp.text)
        print(url)
        return 2

    def format_coord(self,dd):
        if dd is None:
            return f"Please click to choose the prediction place"
        return f"Prediction at {dd['lat']:5.3f}, {dd['lng']:5.3f}"

if __name__=="__main__":
    MyApp(sys.argv[1])