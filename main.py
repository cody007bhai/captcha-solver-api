import os
from flask import Flask, request
import base64

app = Flask(__name__)

# Global variable for OCR
ocr_instance = None

def get_ocr():
    global ocr_instance
    if ocr_instance is None:
        # Import yahan karne se startup crash nahi hoga
        import ddddocr
        ocr_instance = ddddocr.DdddOcr(show_ad=False)
    return ocr_instance

@app.route('/')
def home():
    return "Captcha Solver is Live and Active! Final Push, Adarsh!"

@app.route('/solve', methods=['POST'])
def solve():
    try:
        data = request.json
        img_base64 = data.get('image')
        if not img_base64:
            return "No image provided", 400
            
        img_bytes = base64.b64decode(img_base64)
        solver = get_ocr()
        result = solver.classification(img_bytes)
        return result
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

