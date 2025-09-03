import hashlib, random

def _score(b: bytes, salt: str) -> float:
    h = hashlib.sha256(b + salt.encode()).hexdigest()
    return int(h[:8], 16) / 0xFFFFFFFF

def detect_image_safe(content: bytes, threshold: float):
    explicit = _score(content, "explicit")
    nudity = _score(content, "nudity")
    labels = [
        {"name":"explicit","score":explicit},
        {"name":"nudity","score":nudity},
    ]
    regions = []
    if max(explicit, nudity) > threshold:
        regions = [ {"box":[24,24,160,160], "confidence":max(explicit,nudity)} ]
    return {"labels": labels, "regions": regions}

def detect_image_strict(content: bytes, threshold: float):
    # More granular demo labels
    penis = _score(content, "penis")
    breasts = _score(content, "breasts")
    butt = _score(content, "butt")
    sex_act = _score(content, "sex_act")
    labels = [
        {"name":"penis","score":penis},
        {"name":"breasts","score":breasts},
        {"name":"butt","score":butt},
        {"name":"sex_act","score":sex_act},
    ]
    regions = []
    if max(penis, breasts, butt, sex_act) > threshold:
        regions = [ {"box":[48,48,120,120], "confidence":max(penis, breasts, butt, sex_act)} ]
    return {"labels": labels, "regions": regions}

def detect_text_safe(text: str, threshold: float):
    b = text.encode()
    sexual = _score(b,"sexual")
    intimate = _score(b,"intimate")
    return {"labels":[{"name":"sexual","score":sexual},{"name":"intimate","score":intimate}],"regions":[]}

def detect_text_strict(text: str, threshold: float):
    b = text.encode()
    penis = _score(b,"penis_text")
    breasts = _score(b,"breasts_text")
    dirty = _score(b,"dirty_text")
    return {"labels":[{"name":"penis","score":penis},{"name":"breasts","score":breasts},{"name":"dirty","score":dirty}],"regions":[]}
