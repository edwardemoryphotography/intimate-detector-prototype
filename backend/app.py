from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
from nudenet import NudeDetector
import threading

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = '/tmp/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

detector = None

detector_lock = threading.Lock()

def _init_detector():
    global detector
    with detector_lock:
        if detector is None:
            detector = NudeDetector()

def get_detector():
    if detector is None:
        _init_detector()
    return detector

@app.route('/api/health')
def health_check():
    return jsonify({"status": "ready" if detector else "loading"})

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory('../frontend', path)

@app.route('/api/detect', methods=['POST'])
def detect():
    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    detections = get_detector().detect(filepath)
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
    threading.Thread(target=_init_detector).start()
    app.run(debug=True, host='0.0.0.0', port=5000)
