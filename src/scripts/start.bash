#!/bin/bash

# Navigate to the project directory
cd ~/Documents/pi-project/src

# Start the backend server
cd backend/
nohup python3 server.py > backend.log 2>&1 &

# Start the frontend server
cd ../frontend/
nohup npm start > frontend.log 2>&1 &

# Start the microcontroller server
cd ../microcontrollers/
nohup python3 main.py > microcontrollers.log 2>&1 &

echo "Servers started."
