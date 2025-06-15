import os
import tempfile
import json
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

def test_detect_endpoint():
    client = app.test_client()
    tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
    from PIL import Image
    img = Image.new("RGB", (10, 10), color="white")
    img.save(tmp.name)
    tmp.close()
    with open(tmp.name, 'rb') as f:
        data = {'file': (f, 'test.jpg')}
        res = client.post('/api/detect', data=data, content_type='multipart/form-data')
    os.unlink(tmp.name)
    assert res.status_code == 200
    result = json.loads(res.data.decode('utf-8'))
    assert 'detections' in result
