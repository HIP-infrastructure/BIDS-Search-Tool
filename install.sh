#!/bin/bash

# Get current path
CWD="$(pwd)"
echo "Current directory: $CWD"
echo "Checking that all important directories exist..."
DIR_DATA="$CWD/data"
# Check if the directory does not exist
if [ ! -d "$DIR_DATA" ]; then
    # Directory does not exist, so create it
    mkdir "$DIR_DATA"
    echo "Directory $DIR_DATA created."
else
    echo "Directory $DIR_DATA exists."
fi

DIR_CSV="$DIR_DATA/csv_files"

# Check if the directory does not exist
if [ ! -d "$DIR_CSV" ]; then
    # Directory does not exist, so create it
    mkdir "$DIR_CSV"
    echo "Directory $DIR_CSV created."
else
    echo "Directory $DIR_CSV exists."
fi

DIR_PARQUET="$DIR_DATA/parquet_files"

# Check if the directory does not exist
if [ ! -d "$DIR_PARQUET" ]; then
    # Directory does not exist, so create it
    mkdir "$DIR_PARQUET"
    echo "Directory $DIR_PARQUET created."
else
    echo "Directory $DIR_PARQUET exists."
fi

# Check if 'python3' is installed
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo "Neither python nor python3 is installed. Please install a recent version of python."
    exit 1
fi

echo "Using command $PYTHON_CMD"

$PYTHON_CMD -m venv .streamlit
if [ $? -eq 0 ]; then
    echo "SUCCEEDED '$PYTHON_CMD -m venv .streamlit'"
else
    echo "FAILED '$PYTHON_CMD -m venv .streamlit'"
fi

echo "Activating virtual environment..."
source .streamlit/bin/activate
if [ $? -eq 0 ]; then
    echo "SUCCEEDED 'source .streamlit/bin/activate'"
else
    echo "FAILED 'source .streamlit/bin/activate'"
fi

echo "Installing app..."
pip install .
if [ $? -eq 0 ]; then
    echo "SUCCEEDED 'pip install .'"
else
    echo "FAILED 'pip install .'"
fi

echo "Finally, launching app in browser..."
streamlit run src/start.py
if [ $? -eq 0 ]; then
    echo "SUCCEEDED 'streamlit run src/start.py'"
else
    echo "FAILED 'streamlit run src/start.py'"
fi