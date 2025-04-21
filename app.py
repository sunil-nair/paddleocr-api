from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
from PIL import Image
import pytesseract
import io
import os

app = Flask(__name__)
CORS(app)  # ✅ This allows cross-origin requests from anywhere by default

@app.route("/ocr", methods=["POST"])
def ocr():
    try:
        data = request.get_json(force=True)

        image_b64 = data.get("image_base64")
        if not image_b64:
            return jsonify({"error": "Missing 'image_base64' field"}), 400

        try:
            image_data = base64.b64decode(image_b64)
        except base64.binascii.Error as e:
            return jsonify({"error": f"Base64 decoding failed: {str(e)}"}), 400

        image = Image.open(io.BytesIO(image_data))
        text = pytesseract.image_to_string(image)

        return jsonify({"text": text})

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)