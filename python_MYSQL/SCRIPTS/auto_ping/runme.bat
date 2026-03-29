@echo off

:: Check if venv exists, if not create it
if not exist "venv\"
(
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

:: Run the script with any arguments passed to the bat file
echo Starting autoping...
python autoping.py %*

:: Deactivate venv when script stops
deactivate