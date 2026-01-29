@echo off
echo Installing Python dependencies with pip...
echo.

pip install -r requirements.txt

echo.
echo Installation complete!
echo You can now run: python evaluate_model.py
pause
