# #!/bin/bash

# ############# 1. Kill Any Process Using Backend (8000) & Frontend (5173) Ports #############
# echo "🔴 Stopping any processes using ports 8000 and 5173..."
# lsof -ti :8000 | xargs kill -9 2>/dev/null
# lsof -ti :5173 | xargs kill -9 2>/dev/null
# echo "✅ Ports 8000 and 5173 cleared."

# ############# 2. Set the Codespace API URL for Vite Frontend #############
# echo "🔄 Setting up API URL for frontend..."

# # Check if CODESPACE_NAME is available
# if [[ -z "$CODESPACE_NAME" ]]; then
#   echo "❌ Error: CODESPACE_NAME is not set. Are you running this inside GitHub Codespaces?"
#   exit 1
# fi

# # Construct the API URL
# API_URL="https://${CODESPACE_NAME}-8000.app.github.dev"

# # Write the API URL to the `.env` file for the frontend
# echo "VITE_API_URL=$API_URL" > .env
# echo "✅ VITE_API_URL set to: $API_URL"

# ############# 3. Make Backend & Frontend Ports Public in GitHub Codespaces #############
# echo "🌍 Making ports 8000 (backend) and 5173 (frontend) public for external access..."
# gh codespace ports visibility 8000:public
# gh codespace ports visibility 5173:public
# echo "✅ Ports 8000 and 5173 are now public."

# ############# 4. Start the FastAPI Backend #############
# echo "🚀 Starting the FastAPI backend..."
# cd backend  # Navigate to the backend directory

# # Start FastAPI server with proxy headers for external access
# uvicorn server:app --host 0.0.0.0 --port 8000 --reload --proxy-headers &

# ############# 5. Start the Vite Frontend #############
# echo "🌐 Starting the Vite frontend..."
# cd ../  # Move back to the root directory

# # Run frontend with correct API URL
# npm run dev -- --host 0.0.0.0 --port 5173 &

# echo "✅ Backend and Frontend are running successfully!"
