# #!/bin/bash

# ############# 1. Kill any process using port 8000 #############
# echo "🔴 Stopping any process using port 8000..."
# lsof -ti :8000 | xargs kill -9 2>/dev/null
# echo "✅ Port 8000 cleared."

# ############# 2. Set the Codespace API URL for Vite #############
# echo "🔄 Setting up API URL for frontend..."
# # Get the Codespace name
# CODESPACE_NAME=$(echo $CODESPACE_NAME)

# # Construct the API URL
# API_URL="https://${CODESPACE_NAME}-8000.app.github.dev"

# # Write the API URL to the `.env` file for Vite frontend
# echo "VITE_API_URL=$API_URL" > .env

# echo "✅ VITE_API_URL set to: $API_URL"

# ############# 3. Ensure Port 8000 is Public in GitHub Codespaces #############
# echo "🌍 Making port 8000 public for external access..."
# gh codespace ports visibility 8000:public
# echo "✅ Port 8000 is now public."

# ############# 4. Start the FastAPI Backend #############
# echo "🚀 Starting the FastAPI backend..."
# cd backend  # Navigate to the backend directory

# # Start the FastAPI server using Uvicorn with proxy headers for proper external access
# uvicorn server:app --host 0.0.0.0 --port 8000 --reload --proxy-headers
