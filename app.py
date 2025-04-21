from flask import Flask, request, jsonify
from flask_cors import CORS
import base64, pytesseract
from PIL import Image
import io, os

app = Flask(__name__)
CORS(app)  # This enables CORS on all routes by default

@app.route("/ocr", methods=["POST", "OPTIONS"])
def ocr():
    # ✅ Respond to preflight (OPTIONS) requests
    if request.method == "OPTIONS":
        return '', 204

    try:
        data = request.get_json(force=True)
        image_b64 = data.get("image_base64")

        if not image_b64:
            return jsonify({"error": "Missing 'image_base64' field"}), 400

        image_data = base64.b64decode(image_b64)
        image = Image.open(io.BytesIO(image_data))
        text = pytesseract.image_to_string(image)

        return jsonify({"text": text})

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

# Optional: base route to test API is live
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "OCR API is running"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)