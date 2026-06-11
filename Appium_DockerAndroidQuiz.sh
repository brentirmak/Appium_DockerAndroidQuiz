#!/bin/bash

# Get directory where script is located
SCRIPT_DIR=$(dirname "$0")

# Get absolute path of script directory
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

# Get directory where script was called FROM
CALLED_FROM=$(pwd)

echo "Script lives in: $SCRIPT_DIR"
echo "Called from: $CALLED_FROM"

echo "Running the Appium_DockerAndroidQuiz script"
#python3 Appium_Test.py
pytest -s
echo "Storing the results for the Appium_Test script run"
python3 Appium_DockerAndroidQuiz_StoreDB.py
echo "Results have been stored - will remove txt results file"
rm Appium_DockerAndroidQuiz.txt