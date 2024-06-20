FROM python:3.8

WORKDIR /app

COPY model/ model/

ENTRYPOINT ["python", "model/train.py"]