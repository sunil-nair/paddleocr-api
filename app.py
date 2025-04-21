from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return "👋 OCR Service is Running!"

@app.route('/ocr', methods=['POST'])
def ocr():
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()

        if 'image_base64' not in data:
            return jsonify({"error": "Missing 'image_base64' field"}), 400

        image_data = base64.b64decode(data['image_base64'])
        image = Image.open(io.BytesIO(image_data))

        text = pytesseract.image_to_string(image)
        return jsonify({'text': text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)