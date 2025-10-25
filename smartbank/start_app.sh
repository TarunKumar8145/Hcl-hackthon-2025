#!/bin/bash

echo "🏦 Starting SmartBank Application..."

# Navigate to project directory
cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Start the application
echo "🚀 Starting server on http://localhost:8000"
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
