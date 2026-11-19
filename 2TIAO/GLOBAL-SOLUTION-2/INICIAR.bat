@echo off
cd /d "%~dp0"
where py >nul 2>&1
if errorlevel 1 (set "PY_CMD=python") else (set "PY_CMD=py")
%PY_CMD% -c "import streamlit" 2>nul
if errorlevel 1 %PY_CMD% -m pip install -r requirements.txt
if errorlevel 1 goto erro
%PY_CMD% -m streamlit run src/app.py
if not errorlevel 1 exit /b 0
:erro
pause
