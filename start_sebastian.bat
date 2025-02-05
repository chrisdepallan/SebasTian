@echo off
cd C:\path\to\sebastian
call venv\Scripts\activate
uvicorn src.main:app --host 0.0.0.0 --port 8000 