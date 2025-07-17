# Intimate Area Detector

This is a simple web application that uses the `nudenet` library to detect intimate areas in images.

## Setup

### Prerequisites

*   [Docker](https://www.docker.com/)

### Running the application

1.  Build the Docker image:

    ```bash
    docker build -t intimate-area-detector .
    ```

2.  Run the Docker container:

    ```bash
    docker run -p 5000:5000 intimate-area-detector
    ```

3.  Open your browser and go to `http://localhost:5000`.

## Development

### Prerequisites

*   [Python 3.9](https://www.python.org/downloads/release/python-390/)
*   [Node.js 18](https://nodejs.org/en/download/releases/)

### Backend

1.  Create a virtual environment:

    ```bash
    python3 -m venv venv
    ```

2.  Activate the virtual environment:

    ```bash
    source venv/bin/activate
    ```

3.  Install the dependencies:

    ```bash
    pip install -r backend/requirements.txt
    ```

4.  Run the backend server:

    ```bash
    python backend/app.py
    ```

### Frontend

1.  Install the dependencies:

    ```bash
    cd frontend
    npm install
    ```

2.  Run the frontend development server:

    ```bash
    npm run dev
    ```
