@echo off
TITLE Telugu Speech-to-Sign App
echo ==================================================
echo      Launching Telugu Speech-to-Sign App
echo ==================================================
echo.

:: Navigate to the project directory
cd /d "%~dp0telugu_speech_to_sign"

:: Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo WARNING: Virtual environment not found at venv\Scripts\activate.bat
    echo Attempting to run with global python...
)

:: Run the application
echo Starting GUI...
python launch_gui.py

:: Pause if it crashes so user can see error
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ==================================================
    echo    ERROR: An error occurred (Exit Code: %ERRORLEVEL%)
    echo ==================================================
    pause
)
