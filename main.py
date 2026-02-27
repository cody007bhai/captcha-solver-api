import os
from flask import Flask, request
import base64
from PIL import Image
import io
import pytesseract

app = Flask(__name__)

@app.route('/')
def home():
    return "Lite Solver is Online!"

@app.route('/solve', methods=['POST'])
def solve():
    try:
        data = request.json
        img_64 = data.get('image')
        img_bytes = base64.b64decode(img_64)
        
        # Image ko PIL mein convert karna
        img = Image.open(io.BytesIO(img_bytes))
        
        # Tesseract se text nikalna (Simple & Fast)
        result = pytesseract.image_to_string(img, config='--psm 6').strip()
        
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
