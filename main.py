import ddddocr
from flask import Flask, request, jsonify
import base64
import os

app = Flask(__name__)

# OCR engine ko ek hi baar load karenge memory bachane ke liye
try:
    ocr = ddddocr.DdddOcr(show_ad=False)
except Exception as e:
    ocr = None

@app.route('/')
def home():
    return "Captcha Solver is Live and Active!"

@app.route('/solve', methods=['POST'])
def solve():
    if ocr is None:
        return "OCR Engine not initialized", 500
    try:
        data = request.json
        if not data or 'image' not in data:
            return "No image data", 400
            
        img_base64 = data['image']
        img_bytes = base64.b64decode(img_base64)
        result = ocr.classification(img_bytes)
        return result
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    # Render automatically port assign karta hai
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

