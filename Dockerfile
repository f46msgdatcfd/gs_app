# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app
COPY main.py .
COPY .env.example .env

# Copy frontend files into static folder
RUN mkdir static
COPY index.html ./static/index.html

# Install simple HTTP server for frontend
RUN apt-get update && apt-get install -y --no-install-recommends     curl && rm -rf /var/lib/apt/lists/*

# Expose ports: 8000 (FastAPI) and 8080 (HTML)
EXPOSE 8000 8080

# Start both backend and frontend
CMD sh -c "python3 -m http.server 8080 --directory static & uvicorn main:app --host 0.0.0.0 --port 8000"
