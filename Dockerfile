FROM python:3.10-slim

# System dependencies: OpenCV aur Tesseract ke liye
# 'libgl1' use kar rahe hain kyunki purana package hat gaya hai
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

# Gunicorn start command with increased timeout
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "--timeout", "120", "--workers", "1", "main:app"]
