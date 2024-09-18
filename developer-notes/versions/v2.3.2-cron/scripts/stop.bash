#!/bin/bash

# Stop backend server
pkill -f "python3 server.py"

# Stop frontend server
pkill -f "npm run deploy"

# Stop microcontroller server
pkill -f "python3 main.py"

echo "Servers stopped."
