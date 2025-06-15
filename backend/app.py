from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/detect', methods=['POST'])
def detect():
    """Handle image upload and return fake detection results."""
    uploaded_file = request.files.get('file')
    if uploaded_file is None or uploaded_file.filename == "":
        return jsonify({"error": "No file provided"}), 400

    filename = secure_filename(uploaded_file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    uploaded_file.save(filepath)

    result = {
        "filename": filename,
        "detections": [
            {"label": "buttocks", "confidence": 0.87},
            {"label": "breast", "confidence": 0.92}
        ]
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
