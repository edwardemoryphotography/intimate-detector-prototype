import io
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.app import app


def test_detect_success():
    client = app.test_client()
    data = {"file": (io.BytesIO(b"fake"), "test.jpg")}
    resp = client.post("/api/detect", data=data, content_type="multipart/form-data")
    assert resp.status_code == 200
    result = resp.get_json()
    assert "filename" in result
    assert "detections" in result


def test_detect_missing_file():
    client = app.test_client()
    resp = client.post("/api/detect", data={}, content_type="multipart/form-data")
    assert resp.status_code == 400

