#!/bin/bash

echo "🚀 Stopping existing backend (port 8000) and frontend (port 5173)..."

# Kill processes running on backend and frontend ports
lsof -ti :8000 | xargs kill -9 2>/dev/null
lsof -ti :5173 | xargs kill -9 2>/dev/null

echo "✅ Ports cleared."

# Activate virtual environment (modify this if needed)
echo "🔧 Activating virtual environment..."
source .repo.ai/bin/activate || source .repo.ai/Scripts/activate

# Run database schema setup
echo "🛠️ Setting up DuckDB schemas..."
python backend/db/config_testdb.py
python backend/db/config_proddb.py

# Start the FastAPI backend in the background
echo "🚀 Starting FastAPI backend..."
cd backend
uvicorn server:app --host 0.0.0.0 --port 8000 --reload --reload-exclude cloned_repos &

# Wait a few seconds to let the backend start
sleep 2

# Start the frontend
echo "🚀 Starting frontend..."
cd ../
npm run dev

echo "✅ Backend and frontend are running!"
