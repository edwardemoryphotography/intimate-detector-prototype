import sys
import os
import pytest
from fastapi.testclient import TestClient

# Add the backend directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, MAX_UPLOAD

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    json = response.json()
    assert json["ok"] == True
    assert json["model_loaded"] == True

def test_detect_text_api_safe(monkeypatch):
    # Mock the detector function
    monkeypatch.setattr('app.detect_text_safe', lambda text, threshold: {"labels": [], "regions": []})
    response = client.post("/api/detect-text", json={"text": "hello"})
    assert response.status_code == 200
    json = response.json()
    assert "labels" in json
    assert json["threshold"] == 0.5

def test_detect_text_api_strict(monkeypatch):
    # Mock the detector function
    monkeypatch.setattr('app.detect_text_strict', lambda text, threshold: {"labels": [], "regions": []})
    response = client.post("/api/detect-text", json={"text": "hello", "strict": True, "threshold": 0.8})
    assert response.status_code == 200
    json = response.json()
    assert "labels" in json
    assert json["threshold"] == 0.8

def test_detect_image_api_safe(monkeypatch):
    # Mock the detector function
    monkeypatch.setattr('app.detect_image_safe', lambda content, threshold: {"labels": [], "regions": []})
    response = client.post(
        "/api/detect-image",
        files={"file": ("test.jpg", b"fake image data", "image/jpeg")},
        data={"threshold": 0.5, "strict": "False"}
    )
    assert response.status_code == 200
    json = response.json()
    assert "labels" in json
    assert json["threshold"] == 0.5

def test_detect_image_api_strict(monkeypatch):
    # Mock the detector function
    monkeypatch.setattr('app.detect_image_strict', lambda content, threshold: {"labels": [], "regions": []})
    response = client.post(
        "/api/detect-image",
        files={"file": ("test.jpg", b"fake image data", "image/jpeg")},
        data={"threshold": 0.7, "strict": "True"}
    )
    assert response.status_code == 200
    json = response.json()
    assert "labels" in json
    assert json["threshold"] == 0.7

def test_upload_limit():
    # Create a dummy file that is larger than MAX_UPLOAD
    large_file_content = b"a" * (MAX_UPLOAD + 1)
    response = client.post(
        "/api/detect-image",
        files={"file": ("large.jpg", large_file_content, "image/jpeg")},
    )
    assert response.status_code == 413
