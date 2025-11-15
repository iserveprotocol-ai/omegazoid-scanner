@echo off
echo ================================================================
echo          CREATING DEPLOYMENT PACKAGE
echo ================================================================
echo.
echo This will create a ZIP file ready for deployment
echo.

REM Create deployment folder
if not exist "deployment" mkdir deployment

REM Copy essential files
echo Copying files...
xcopy /Y app.py deployment\
xcopy /Y stock_scanner.py deployment\
xcopy /Y scanner_presets.py deployment\
xcopy /Y requirements.txt deployment\
xcopy /Y Procfile deployment\
xcopy /Y .gitignore deployment\

REM Copy templates folder
if not exist "deployment\templates" mkdir deployment\templates
xcopy /Y templates\*.* deployment\templates\

echo.
echo ================================================================
echo DEPLOYMENT PACKAGE READY!
echo ================================================================
echo.
echo Files are in the "deployment" folder
echo.
echo NEXT STEPS:
echo 1. Upload to GitHub OR
echo 2. ZIP the "deployment" folder and upload to hosting platform
echo.
echo For GitHub deployment:
echo   cd deployment
echo   git init
echo   git add .
echo   git commit -m "Initial deployment"
echo   git remote add origin YOUR_GITHUB_URL
echo   git push -u origin main
echo.
pause
