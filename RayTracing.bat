@echo off

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python 3 is not installed. Please install Python 3 and try again.
    pause
    exit /b
)

python source\RayTracing.py
pause