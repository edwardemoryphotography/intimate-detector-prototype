from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/detect', methods=['POST'])
def detect():
    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

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