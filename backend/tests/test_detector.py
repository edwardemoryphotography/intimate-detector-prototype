import sys
import os
import pytest

# Add the backend directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from detector import _score, detect_text_safe, detect_text_strict, detect_image_safe, detect_image_strict

def test_score():
    score = _score(b"test", "salt")
    assert isinstance(score, float)
    assert 0 <= score <= 1

def test_detect_text_safe(monkeypatch):
    # Mock _score to control its output
    scores = {"sexual": 0.8, "intimate": 0.3}
    monkeypatch.setattr('detector._score', lambda b, salt: scores[salt])
    result = detect_text_safe("any text", 0.5)
    assert result["labels"][0]["score"] == 0.8
    assert result["labels"][1]["score"] == 0.3

def test_detect_text_strict(monkeypatch):
    # Mock _score to control its output
    scores = {"penis_text": 0.9, "breasts_text": 0.2, "dirty_text": 0.4}
    monkeypatch.setattr('detector._score', lambda b, salt: scores[salt])
    result = detect_text_strict("any text", 0.5)
    assert result["labels"][0]["score"] == 0.9
    assert result["labels"][1]["score"] == 0.2
    assert result["labels"][2]["score"] == 0.4

def test_detect_image_safe_no_regions(monkeypatch):
    # Mock _score to return a value below the threshold
    monkeypatch.setattr('detector._score', lambda content, salt: 0.4)
    result = detect_image_safe(b"any content", 0.5)
    assert len(result["regions"]) == 0

def test_detect_image_safe_with_regions(monkeypatch):
    # Mock _score to return a value above the threshold
    monkeypatch.setattr('detector._score', lambda content, salt: 0.6)
    result = detect_image_safe(b"any content", 0.5)
    assert len(result["regions"]) == 1
    assert result["regions"][0]["confidence"] == 0.6

def test_detect_image_strict_no_regions(monkeypatch):
    # Mock _score to return a value below the threshold
    monkeypatch.setattr('detector._score', lambda content, salt: 0.4)
    result = detect_image_strict(b"any content", 0.5)
    assert len(result["regions"]) == 0

def test_detect_image_strict_with_regions(monkeypatch):
    # Mock _score to return a value above the threshold
    monkeypatch.setattr('detector._score', lambda content, salt: 0.6)
    result = detect_image_strict(b"any content", 0.5)
    assert len(result["regions"]) == 1
    assert result["regions"][0]["confidence"] == 0.6
