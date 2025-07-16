# Intimate Detector Prototype

This project demonstrates a simple image API for detecting sensitive body parts using [NudeNet](https://github.com/notAI-tech/NudeNet).
It includes a Flask backend, a small React web UI and an example React Native mobile app tested on iPhone 16 Pro via Expo.

## Backend

The backend uses Flask and NudeNet to process images.

```bash
cd backend
pip install -r requirements.txt
python app.py
```

The API will be available at `http://localhost:5000/api/detect`.

## Web Frontend

The `frontend` folder contains a minimal React component that can be used with any build setup. It posts an image file to the API and displays the JSON result.

## Mobile App

The `mobile` directory contains an [Expo](https://expo.dev/) project so it can run easily on iOS or Android devices.

Install the dependencies and start the development server:

```bash
cd mobile
npm install
npm run ios  # or npm run android
```

Use the Expo Go app on your device (tested on iPhone 16 Pro) to scan the QR code and interact with the backend API.

## License

This code is provided as a prototype for demonstration purposes only.
