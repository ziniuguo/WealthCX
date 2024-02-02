#!/bin/bash

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
pm2 restart uvicorn --name="fastapi-app" --watch main:app --log-date-format="YYYY-MM-DD HH:mm Z" --log "logs/fastapi-app.log" --log "logs/error.log"

echo "Script execution completed."
