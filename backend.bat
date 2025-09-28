@echo off
cd backend

IF NOT EXIST "venv" python -m venv venv

call venv\Scripts\activate
pip install -r requirements.txt

start cmd /k "uvicorn main:app --reload --port 8000"
