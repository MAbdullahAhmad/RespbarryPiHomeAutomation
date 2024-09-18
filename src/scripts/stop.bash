#!/bin/bash

# Stop backend server
pkill -f "python3 server.py"

# Stop frontend server
pkill -f "npm start"

# Stop microcontroller server
pkill -f "python3 main.py"

echo "Servers stopped."
