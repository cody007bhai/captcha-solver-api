# Python ka lightweight version use kar rahe hain
FROM python:3.10-slim

# Tesseract OCR engine aur zaroori libraries install karna
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && apt-get clean

# App directory set karna
WORKDIR /app
COPY . /app

# Requirements install karna
RUN pip install --no-cache-dir -r requirements.txt

# Render ke liye port binding
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "main:app"]

