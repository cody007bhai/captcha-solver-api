import os
from flask import Flask, request
import base64
import ddddocr # Pehle hi import kar liya

app = Flask(__name__)
# Global init taaki har request pe load na ho (Memory bachegi)
ocr = ddddocr.DdddOcr(show_ad=False)

@app.route('/')
def home():
    return "Beast Solver is Online!"

@app.route('/solve', methods=['POST'])
def solve():
    try:
        data = request.json
        img_64 = data.get('image')
        if not img_64: return "No Image", 400
        
        img_bytes = base64.b64decode(img_64)
        # Solve logic
        res = ocr.classification(img_bytes)
        return str(res)
    except Exception as e:
        return f"Error: {str(e)}", 500 # Server crash hone par error message bhejega

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

