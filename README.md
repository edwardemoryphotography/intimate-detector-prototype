# Intimate Detector Prototype

This project contains a small Flask backend and a React frontend for testing an "intimate area" detection API.

## Setup

Install Python dependencies and start the backend:

```bash
cd backend
pip install -r requirements.txt
python app.py
```

In a separate terminal, start the frontend (requires Node.js):

```bash
cd frontend
# Using a tool like create-react-app, for example
npm start
```

The backend runs on `http://localhost:5000`. The frontend expects the backend at this URL.

