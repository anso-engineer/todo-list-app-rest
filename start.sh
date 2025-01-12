#!/bin/bash

PORT=5000

# Function to check if the port is in use
check_port() {
    lsof -i :$PORT | grep LISTEN > /dev/null
    return $?
}

# Function to prompt and stop the process
stop_process() {
    local PID
    PID=$(lsof -t -i :$PORT)
    echo "Process running on port $PORT with PID $PID."

    # Prompt user to close the process
    read -p "Do you want to stop it? (yes/no): " choice
    case "$choice" in
        yes|y|Y)
            echo "Stopping process with PID $PID..."
            sudo kill -9 $PID
            echo "Process stopped."
            ;;
        no|n|N)
            echo "Keeping the existing process running."
            exit 0
            ;;
        *)
            echo "Invalid input. Exiting."
            exit 1
            ;;
    esac
}

# Function to start the Flask app
start_flask() {
    echo "Starting Flask app on port $PORT..."
    export FLASK_APP=app.py  # Replace with the correct entry point file if it's not `app.py`
    export FLASK_ENV=development  # Optional: Enables debug mode
    nohup flask run --host=0.0.0.0 --port=$PORT > flask_output.log 2>&1 &
    echo "Flask app started with nohup. Logs are being written to flask_output.log."
}

# Main logic
if check_port; then
    echo "Something is already running on port $PORT."
    stop_process
fi

start_flask

