import ddddocr
from flask import Flask, request, jsonify
import base64

app = Flask(__name__)
# OCR engine initialization
ocr = ddddocr.DdddOcr(show_ad=False)

@app.route('/')
def home():
    return "Captcha Solver is Active!"

@app.route('/solve', methods=['POST'])
def solve():
    try:
        data = request.json
        if not data or 'image' not in data:
            return jsonify({"error": "No image data provided"}), 400
            
        img_base64 = data['image']
        img_bytes = base64.b64decode(img_base64)
        result = ocr.classification(img_bytes)
        return result
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

