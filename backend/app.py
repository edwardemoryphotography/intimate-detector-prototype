from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
from nudenet import NudeDetector
from concurrent.futures import ThreadPoolExecutor
import tempfile
import os

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

detector = NudeDetector()
executor = ThreadPoolExecutor(max_workers=2)

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/detect', methods=['POST'])
def detect():
    if 'file' not in request.files:
        return jsonify({"error": "file not provided"}), 400

    file = request.files['file']
    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "invalid file"}), 400

    filename = secure_filename(file.filename)
    with tempfile.NamedTemporaryFile(delete=False, dir=UPLOAD_FOLDER, suffix=os.path.splitext(filename)[1]) as tmp:
        file.save(tmp.name)
        filepath = tmp.name

    def run_detection(path: str):
        return detector.detect(path)

    future = executor.submit(run_detection, filepath)
    detections = future.result()

    result = {
        "filename": filename,
        "detections": detections,
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
