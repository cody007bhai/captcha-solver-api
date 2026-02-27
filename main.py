from flask import Flask, request, jsonify
import base64
import os

app = Flask(__name__)

# OCR ko global define karenge par load baad mein karenge
ocr = None

def get_ocr():
    global ocr
    if ocr is None:
        import ddddocr
        ocr = ddddocr.DdddOcr(show_ad=False)
    return ocr

@app.route('/')
def home():
    return "Captcha Solver is Live and Active! Battery low toh nahi? :P"

@app.route('/solve', methods=['POST'])
def solve():
    try:
        solver = get_ocr()
        data = request.json
        img_base64 = data['image']
        img_bytes = base64.b64decode(img_base64)
        result = solver.classification(img_bytes)
        return result
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    app.run(host='0.0.0.0', port=port)

