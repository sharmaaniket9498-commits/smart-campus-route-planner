@echo off
setlocal
cd /d "%~dp0"
title Smart Campus Route Planner
echo.
echo  ============================================
echo   Smart Campus Route Planner - Startup
echo  ============================================
echo.
where py >nul 2>nul
if %errorlevel%==0 (
  set "PY=py -3"
) else (
  where python >nul 2>nul
  if errorlevel 1 (
    echo ERROR: Python was not found.
    echo Install Python 3.10 or newer from https://www.python.org/downloads/
    echo During installation, enable "Add Python to PATH".
    pause
    exit /b 1
  )
  set "PY=python"
)
if not exist ".venv\Scripts\python.exe" (
  echo Creating project virtual environment...
  %PY% -m venv .venv
  if errorlevel 1 (
    echo ERROR: Could not create virtual environment.
    echo Check Python installation and folder permissions.
    pause
    exit /b 1
  )
)
echo Checking and installing required packages...
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
  echo ERROR: Dependency installation failed.
  echo Check your internet connection and try again.
  pause
  exit /b 1
)
echo Starting Smart Campus Route Planner...
".venv\Scripts\python.exe" app.py
if errorlevel 1 (
  echo.
  echo The application exited with an error. See the message above.
  pause
  exit /b 1
)
endlocal
