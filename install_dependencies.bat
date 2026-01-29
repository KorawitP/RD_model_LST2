@echo off
echo Installing Python dependencies...
echo.

REM ติดตั้ง uv (Python package manager)
echo [1/2] Installing uv...
pip install uv
echo.

REM ติดตั้ง dependencies ด้วย uv
echo [2/2] Installing project dependencies...
uv pip install -r requirements.txt
echo.

echo Installation complete!
echo You can now run: python evaluate_model.py
pause
