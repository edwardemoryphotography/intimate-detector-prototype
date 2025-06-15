# Intimate Detector Prototype

This project provides a simple web application for detecting intimate areas in uploaded images.

## Backend

- **Framework**: Flask
- **Detection Model**: [NudeNet](https://github.com/notAI-tech/NudeNet) via the `nudenet` Python package.
- **Setup**:
  ```bash
  cd backend
  pip install -r requirements.txt
  python app.py
  ```

## Frontend

The frontend is built with [Vite](https://vitejs.dev/).

- **Setup**:
  ```bash
  cd frontend
  npm install
  npm run dev
  ```

## Running Tests

- Backend tests use `pytest`:
  ```bash
  pytest backend
  ```
- Frontend tests use `vitest`:
  ```bash
  cd frontend
  npm test
  ```
