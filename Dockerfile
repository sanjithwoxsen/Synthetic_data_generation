FROM python:3.9

WORKDIR /app

COPY requirements.txt /app
COPY main.py /app
COPY logo.jpeg /app
COPY backend.py /app
COPY .env /app

RUN pip install -r requirements.txt

ENTRYPOINT ["streamlit","run " ,"main.py"]

