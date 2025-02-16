#!/bin/bash

# Get the Codespace name
CODESPACE_NAME=$(echo $CODESPACE_NAME)

# Construct the API URL
API_URL="https://${CODESPACE_NAME}-8000.app.github.dev"

# Write the API URL to the `.env` file for Vite
echo "VITE_API_URL=$API_URL" > .env

echo "✅ VITE_API_URL set to: $API_URL"
