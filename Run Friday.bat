@echo off
TITLE F.R.I.D.A.Y. Launcher
CLS
echo ==================================================
echo         F.R.I.D.A.Y. SYSTEM LAUNCHER
echo ==================================================
echo.

:: 1. Navigate to Project Directory (Handles Spaces)
cd /d "%~dp0"
echo [INFO] Working Directory: %CD%

:: 2. Check for Python
if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Python not found in .venv!
    echo Please make sure the '.venv' folder exists.
    echo Expected: %CD%\.venv\Scripts\python.exe
    pause
    exit
)

:: 3. Run Application
echo [INFO] Launching Neural Interface...
echo.
".venv\Scripts\python.exe" src/main.py --gui

:: 4. Crash Handler
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ==================================================
    echo [CRITICAL] SYSTEM CRASHED (Exit Code: %ERRORLEVEL%)
    echo ==================================================
    echo Read the error message above for details.
    pause
) else (
    echo [INFO] System Shutdown Normal.
)
