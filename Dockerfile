FROM python:3.9.1-slim

WORKDIR /app
EXPOSE 8000

RUN apt-get update && \
    apt-get install -y vim && \
    pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["uvicorn", "app.main:app"]

