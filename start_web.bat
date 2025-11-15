@echo off
echo ========================================
echo  Crypto Trend Scanner - Web Interface
echo ========================================
echo.
echo Installing dependencies...
py -m pip install -r requirements.txt
echo.
echo Starting web server...
echo.
echo Open your browser and go to:
echo http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.
py app.py
