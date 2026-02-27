import os
import base64
import io
from flask import Flask, request
from PIL import Image
import pytesseract

app = Flask(__name__)

@app.route('/')
def home():
    return "Color-Isolated Beast Solver is Online!"

@app.route('/solve', methods=['POST'])
def solve():
    try:
        data = request.get_json()
        img_bytes = base64.b64decode(data['image'])
        img = Image.open(io.BytesIO(img_bytes)).convert("RGBA")
        
        # --- Advanced Color Isolation (The Fix) ---
        # Nayi white image banana
        clean_img = Image.new("L", img.size, 255)
        pixels = img.load()
        clean_pixels = clean_img.load()

        for y in range(img.size[1]):
            for x in range(img.size[0]):
                r, g, b, a = pixels[x, y]
                # Agar pixel kaafi gehra (blackish) hai toh usey rakho
                # Letters black hain, toh R,G,B teeno kam honge (e.g. < 90)
                if r < 100 and g < 100 and b < 100:
                    clean_pixels[x, y] = 0 # Black pixel
                else:
                    clean_pixels[x, y] = 255 # White background (colored arcs gayab)

        # Accuracy badhane ke liye image ko 2x bada karna
        clean_img = clean_img.resize((img.size[0]*2, img.size[1]*2), Image.Resampling.LANCZOS)
        
        # Tesseract configuration
        custom_config = r'--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        
        result = pytesseract.image_to_string(clean_img, config=custom_config).strip()
        
        return str(result)
        
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
        
        result = pytesseract.image_to_string(img, config=custom_config).strip()
        
        # Clean up
        del img_bytes
        return str(result)
        
    except Exception as e:
        return f"Internal Error: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
