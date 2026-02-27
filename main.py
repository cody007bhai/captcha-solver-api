import os
import base64
import numpy as np
import cv2
from flask import Flask, request
import pytesseract
from PIL import Image

app = Flask(__name__)

@app.route('/')
def home():
    return "OpenCV Pro Solver is Online!"

@app.route('/solve', methods=['POST'])
def solve():
    try:
        data = request.get_json()
        img_bytes = base64.b64decode(data['image'])
        
        # OpenCV format mein load karna
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # --- Surgical Preprocessing ---
        # 1. Image ko Grayscale mein badalna
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 2. Binary Thresholding (Sirf ekdam dark pixels rakhenge)
        # Isse blue/green/red circles white background mein mil jayenge
        _, binary = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY)
        
        # 3. Denoising: Chote dots ko hatane ke liye
        kernel = np.ones((1,1), np.uint8)
        clean = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        
        # Tesseract Config (Capital Letters + Numbers)
        config = r'--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        result = pytesseract.image_to_string(clean, config=config).strip()
        
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
