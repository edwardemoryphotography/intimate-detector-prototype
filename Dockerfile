# Stage 1: Build the frontend
FROM node:18 AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Build the backend
FROM python:3.9
WORKDIR /app
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist
COPY backend/requirements.txt ./
RUN pip install -r requirements.txt
COPY backend/ ./
EXPOSE 5000
CMD ["python", "app.py"]
