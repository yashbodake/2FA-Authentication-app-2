# Stage 1: Build the Vue.js application
FROM node:18 as build-stage

WORKDIR /app/frontend

COPY frontend/package*.json ./

RUN npm install

COPY frontend/ .

RUN npm run build

# Stage 2: Build the Python backend
FROM python:3.10-slim

WORKDIR /app

# Copy frontend build artifacts
COPY --from=build-stage /app/frontend/dist /app/static

# Install backend dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
