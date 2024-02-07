#!/bin/bash

if ! command -v npm &> /dev/null; then
  echo "npm is not installed. Please install npm."
  exit 1
fi

# Check if pm2 is installed
if ! command -v pm2 &> /dev/null; then
  echo "pm2 is not installed. Installing pm2..."
  npm install -g pm2
  if [ $? -eq 0 ]; then
    echo "pm2 has been successfully installed."
  else
    echo "Failed to install pm2. Please install pm2 manually."
    exit 1
  fi
fi

# Check if uvicorn process is running on port 8000
uvicorn_pid=$(lsof -ti :8000)

if [ -n "$uvicorn_pid" ]; then
  echo "Uvicorn process is running on port 8000. Shutting it down..."
  kill -9 "$uvicorn_pid"
  echo "Uvicorn process has been shut down."
fi

# Run git pull
echo "Running git pull..."
git pull

# Restart uvicorn with pm2
echo "Restarting Uvicorn with pm2..."
pm2 reload start_wealthcx.sh --name="fastapi-app" --watch server:app --log-date-format="YYYY-MM-DD HH:mm Z" --log "logs/fastapi-app.log" --log "logs/error.log"

echo "Script execution completed."
