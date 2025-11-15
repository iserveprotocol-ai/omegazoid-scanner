================================================================================
                    CRYPTO TREND SCANNER - DEPLOYMENT GUIDE
================================================================================

WHAT THIS TOOL DOES:
- Scans top 500 cryptocurrencies for trend-following opportunities
- Uses technical indicators: EMA, RSI, MACD, ADX, Bollinger Bands
- Provides exact BUY/SELL prices with stop loss and profit targets
- Supports Kraken exchange filtering
- Scores cryptos 0-100 based on trend strength

================================================================================
OPTION 1: RUN ON ANOTHER WINDOWS COMPUTER
================================================================================

1. COPY ENTIRE FOLDER
   - Copy the entire "scanner" folder to the new computer
   - Keep all files together in the same folder

2. INSTALL PYTHON (if not installed)
   - Download Python 3.10 or higher from python.org
   - During installation, CHECK "Add Python to PATH"

3. INSTALL DEPENDENCIES
   - Open Command Prompt in the scanner folder
   - Run: pip install -r requirements.txt

4. START THE SCANNER
   - Double-click: start_web.bat
   - OR run in Command Prompt: python app.py
   - Open browser to: http://localhost:5000

================================================================================
OPTION 2: RUN ON MAC/LINUX
================================================================================

1. COPY FOLDER
   - Copy the entire "scanner" folder to Mac/Linux

2. INSTALL DEPENDENCIES
   - Open Terminal in scanner folder
   - Run: pip3 install -r requirements.txt

3. START THE SCANNER
   - Run: python3 app.py
   - Open browser to: http://localhost:5000

================================================================================
OPTION 3: DEPLOY TO A WEBSITE (24/7 ONLINE ACCESS)
================================================================================

RECOMMENDED PLATFORMS (All have FREE tiers):

A) RENDER.COM (Easiest - Recommended)
   1. Create account at render.com
   2. Click "New +" → "Web Service"
   3. Connect your GitHub (upload code there first)
   4. Select: Python
   5. Build Command: pip install -r requirements.txt
   6. Start Command: gunicorn app:app
   7. Click "Create Web Service"
   8. You'll get a URL like: https://your-scanner.onrender.com

B) RAILWAY.APP (Fast deployment)
   1. Go to railway.app
   2. Click "Start a New Project"
   3. Deploy from GitHub
   4. Railway auto-detects Python and deploys
   5. Get instant URL

C) HEROKU (Popular but requires credit card)
   1. Create account at heroku.com
   2. Install Heroku CLI
   3. Run: heroku create your-app-name
   4. Run: git push heroku main
   5. Access at: https://your-app-name.herokuapp.com

D) PYTHONANYWHERE.COM (Python-specific)
   1. Create account at pythonanywhere.com
   2. Upload files via web interface
   3. Configure web app settings
   4. Get URL like: https://yourusername.pythonanywhere.com

================================================================================
FILES NEEDED FOR DEPLOYMENT
================================================================================

Core files (MUST include):
✓ app.py                    - Main Flask application
✓ stock_scanner.py          - Scanner logic
✓ scanner_presets.py        - Preset configurations
✓ requirements.txt          - Python dependencies
✓ templates/index.html      - Web interface

Optional files:
- start_web.bat            - Windows launcher (not needed online)
- README.txt               - This file (not needed online)

================================================================================
ENVIRONMENT VARIABLES (For Online Deployment)
================================================================================

If deploying online, set these environment variables:
- CMC_API_KEY = 24fb5bf708c346b099c9900c3b1082bc

Most platforms let you set this in their dashboard.

================================================================================
QUICK START - GITHUB + RENDER DEPLOYMENT (RECOMMENDED)
================================================================================

1. CREATE GITHUB REPO
   - Go to github.com
   - Create new repository
   - Upload these files:
     * app.py
     * stock_scanner.py
     * scanner_presets.py
     * requirements.txt
     * templates/index.html

2. DEPLOY TO RENDER
   - Go to render.com and sign up
   - Click "New +" → "Web Service"
   - Connect GitHub repository
   - Settings:
     * Name: crypto-scanner
     * Environment: Python 3
     * Build Command: pip install -r requirements.txt
     * Start Command: gunicorn app:app
   - Click "Create Web Service"
   - Wait 2-3 minutes
   - Get your live URL!

3. ACCESS FROM ANYWHERE
   - Open: https://crypto-scanner-xxxx.onrender.com
   - Use on phone, tablet, any device
   - Scan 24/7 without running on your PC

================================================================================
TROUBLESHOOTING
================================================================================

ERROR: "ModuleNotFoundError"
FIX: Run: pip install -r requirements.txt

ERROR: "Port already in use"
FIX: Change port in app.py: app.run(port=5001)

ERROR: "No data found"
FIX: Check internet connection, Yahoo Finance might be down

ERROR: On render.com - "Application failed to start"
FIX: Add Procfile with: web: gunicorn app:app

================================================================================
SECURITY NOTES
================================================================================

⚠ API KEY: The CoinMarketCap API key is currently hardcoded
   - For public deployment, move to environment variable
   - Add to .env file or platform's environment settings

⚠ PRODUCTION: For real production use:
   - Set debug=False in app.py
   - Use proper WSGI server (gunicorn)
   - Add HTTPS (most platforms provide this free)

================================================================================
SUPPORT & UPDATES
================================================================================

Location: c:\Users\david\OneDrive\Desktop\scanner
Version: 1.0
Last Updated: 2025-11-03

To update on deployment platform:
1. Make changes locally
2. Push to GitHub
3. Platform auto-deploys (or click "Deploy" button)

================================================================================
