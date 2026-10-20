@echo off
setlocal
title Telugu Speech-to-Sign

cd /d "%~dp0.."

if exist ".venv\Scripts\activate.bat" (
    call ".venv\Scripts\activate.bat"
) else if exist "venv\Scripts\activate.bat" (
    call "venv\Scripts\activate.bat"
) else (
    echo [warn] No virtual environment found. Using the global Python.
)

python app.py %*
if errorlevel 1 (
    echo.
    echo The application exited with an error.
    pause
)
