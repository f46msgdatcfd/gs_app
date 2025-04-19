#!/bin/bash

# This script is only for local use outside Docker (optional)
echo "Starting frontend at http://localhost:8080"
python3 -m http.server 8080 --directory . &

echo "Starting FastAPI backend at http://localhost:8000"
uvicorn main:app --host 0.0.0.0 --port 8000
