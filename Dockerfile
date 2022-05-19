FROM python:3.8.12-slim-buster

COPY dist /dist

RUN mkdir -p /models
COPY test_TA_Weather/assets/model.joblib /models/model.joblib
ENV MODEL_PATH=/models/model.joblib

RUN pip install --upgrade pip
RUN pip install test_TA_Weather -f /dist

CMD uvicorn test_TA_Weather.api.api:app --host 0.0.0.0 --port $PORT
