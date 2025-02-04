# How to install the app

This is how you install the app locally:

1. Download this repo to your computer (Windows, iOS or Linux)
2. In the folder, locate install.sh and in a console run:
3. ```./install.sh```

# Separate commands in case install.sh doesn't work

1. cd into project's dir
2. Make sure you have the requirements: Python version > 3.9

3. ```python -m venv .streamlit```
4. ```source .streamlit/bin/activate```
5. ```pip install .```
6. ```python -m streamlit run src/app.py```
7. `deactivate` to switch off our streamlit venv
