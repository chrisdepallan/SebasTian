@echo off
REM Change directory to SebasTian project folder  
REM PS: if running manually it doesnt matter since its in the correct folder
cd  E:\path\to\SebasTian 
call .venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.main:app --host localhost --port 8000 --reload