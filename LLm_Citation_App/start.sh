#!/bin/sh

# Exit immediately if a command fails
set -e

echo "Starting the setup for your LLM citation app..."

# Function to install Python if missing (Debian/Ubuntu based)
install_python() {
    echo "Python3 is not installed. Attempting to install it now..."
    if [ "$(uname)" = "Darwin" ]; then
        echo "Detected macOS. Please install Python manually using: brew install python3"
        exit 1
    elif [ -f /etc/debian_version ]; then
        echo "Detected Debian/Ubuntu system. Installing Python..."
        sudo apt update
        sudo apt install python3 python3-venv python3-pip -y
    elif [ -f /etc/redhat-release ]; then
        echo "Detected RedHat/CentOS system. Installing Python..."
        sudo yum install python3 python3-venv python3-pip -y
    else
        echo "Unsupported system. Please install Python manually."
        exit 1
    fi
}

# Check if Python is installed, otherwise install it
if ! command -v python3 >/dev/null 2>&1; then
    install_python
else
    echo "Python3 is already installed."
fi

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating a virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
echo "Activating the virtual environment..."
# Universal method for activating the virtual environment across shells
if [ -f "./venv/bin/activate" ]; then
    . ./venv/bin/activate
else
    echo "Error: Could not activate the virtual environment."
    exit 1
fi

# Upgrade pip and install dependencies
echo "Upgrading pip and installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Optional: Download the LLM model if not present
if [ ! -f "models/Mistral-Nemo-Instruct-2407.Q3_K_S.gguf" ]; then
    echo "Downloading the Mistral model..."
    mkdir -p models
    curl -L -o models/Mistral-Nemo-Instruct-2407.Q3_K_S.gguf "https://huggingface.co/MaziyarPanahi/Mistral-Nemo-Instruct-2407-GGUF/resolve/main/Mistral-Nemo-Instruct-2407.Q3_K_S.gguf"
fi

# Launch the Streamlit app
echo "Starting the Streamlit app..."
streamlit run app.py

# Deactivate the virtual environment after closing the app
deactivate
