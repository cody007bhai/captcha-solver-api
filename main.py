import os
import base64
import io
from flask import Flask, request
from PIL import Image, ImageOps, ImageEnhance
import pytesseract

app = Flask(__name__)

@app.route('/')
def home():
    return "Super-Sharp Solver is Online!"

@app.route('/solve', methods=['POST'])
def solve():
    try:
        data = request.get_json()
        img_bytes = base64.b64decode(data['image'])
        img = Image.open(io.BytesIO(img_bytes))
        
        # --- Super Preprocessing ---
        # 1. Image ko 2 guna bada karna (OCR scaling se accuracy badhti hai)
        width, height = img.size
        img = img.resize((width*2, height*2), Image.Resampling.LANCZOS)
        
        # 2. Grayscale aur Contrast badhana
        img = img.convert('L') 
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0) # Contrast double
        
        # 3. Clean Binarization (Otsu-style threshold)
        # Isse saare colored arcs white ho jayenge aur sirf black letters bachenge
        img = img.point(lambda p: p > 140 and 255)
        
        # Tesseract Config: Sirf Alpha-Numeric Whitelist
        custom_config = r'--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        
        result = pytesseract.image_to_string(img, config=custom_config).strip()
        
        # Clean up
        del img_bytes
        return str(result)
        
    except Exception as e:
        return f"Internal Error: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
