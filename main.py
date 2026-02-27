import os
import base64
import numpy as np
import cv2
from flask import Flask, request
import pytesseract

app = Flask(__name__)

@app.route('/')
def home():
    return "OpenCV Beast Solver is Online!"

@app.route('/solve', methods=['POST'])
def solve():
    try:
        data = request.get_json()
        img_bytes = base64.b64decode(data['image'])
        
        # Image ko OpenCV format mein load karna
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # --- Advanced Color Filtering ---
        # Sirf ekdam dark (black) pixels ko pakdenge (Threshold < 100)
        # Isse colored circles (blue/red/green) white background mein mil jayenge
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        
        # Cleanup: Thoda noise aur hatane ke liye
        kernel = np.ones((2,2), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        
        # Tesseract logic
        config = r'--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        result = pytesseract.image_to_string(binary, config=config).strip()
        
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
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
