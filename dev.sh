#!/usr/bin/env bash
set -euo pipefail
IP="$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo 127.0.0.1)"
echo "Using IP: $IP"
cat > frontend/config.js <<EOF
window.APP_CONFIG={BACKEND_BASE:"http://$IP:8000"};
EOF
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000 &
cd ../frontend
python3 -m http.server 5500 &
echo "Open frontend at: http://$IP:5500"
echo "Backend health:   http://$IP:8000/health"
wait
