from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
from nudenet import NudeDetector

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = '/tmp/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
detector = NudeDetector()

@app.route('/api/detect', methods=['POST'])
def detect():
    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    detections = detector.detect(filepath)
    mapping = {
        "BUTTOCKS_EXPOSED": "buttocks",
        "FEMALE_BREAST_EXPOSED": "breast",
    }
    filtered = [
        {
            "label": mapping[d["class"]],
            "confidence": d["score"],
            "box": d["box"],
        }
        for d in detections
        if d["class"] in mapping
    ]

    return jsonify({"filename": filename, "detections": filtered})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
