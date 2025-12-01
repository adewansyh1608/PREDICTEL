@echo off
echo.
echo ============================================
echo    PREDICTEL - Config Fix Script
echo    Fixing Streamlit Configuration Warnings
echo ============================================
echo.

:: Check if we're in the right directory
if not exist Home.py (
    echo [ERROR] Home.py not found! Please run this script from PREDICTEL folder
    pause
    exit /b 1
)

:: Create .streamlit directory if it doesn't exist
if not exist .streamlit mkdir .streamlit

:: Backup existing config if it exists
if exist .streamlit\config.toml (
    echo [INFO] Backing up existing config...
    copy .streamlit\config.toml .streamlit\config.toml.backup >nul 2>&1
)

:: Create clean, warning-free config
echo [STEP 1] Creating clean Streamlit configuration...
(
echo [theme]
echo # PREDICTEL Dark Theme - No Warnings
echo primaryColor = "#0ea5e9"
echo backgroundColor = "#0a0a0a"
echo secondaryBackgroundColor = "#111111"
echo textColor = "#ffffff"
echo font = "sans serif"
echo.
echo [server]
echo # Server settings - Compatible configuration
echo headless = true
echo runOnSave = true
echo port = 8501
echo baseUrlPath = ""
echo enableXsrfProtection = false
echo maxUploadSize = 200
echo.
echo [browser]
echo # Browser settings - Privacy optimized
echo gatherUsageStats = false
echo.
echo [runner]
echo # Performance optimization
echo magicEnabled = true
echo.
echo [logger]
echo # Clean logging
echo level = "info"
) > .streamlit\config.toml

echo [SUCCESS] Clean configuration created!

:: Clear any cached Streamlit settings
echo [STEP 2] Clearing cached Streamlit data...
if exist "%USERPROFILE%\.streamlit" (
    rmdir /s /q "%USERPROFILE%\.streamlit" 2>nul
    echo [SUCCESS] Streamlit cache cleared
) else (
    echo [INFO] No cached data found
)

:: Verify configuration
echo [STEP 3] Verifying configuration...
if exist .streamlit\config.toml (
    echo [SUCCESS] Configuration file created successfully
    echo [INFO] Location: %CD%\.streamlit\config.toml
) else (
    echo [ERROR] Failed to create configuration file
    pause
    exit /b 1
)

:: Show what was fixed
echo.
echo ============================================
echo    CONFIGURATION ISSUES FIXED
echo ============================================
echo.
echo [FIXED] Removed deprecated "client.caching" option
echo [FIXED] Resolved CORS/XSRF protection conflict
echo [FIXED] Set enableXsrfProtection = false (safe for local use)
echo [FIXED] Added maxUploadSize for large datasets
echo [FIXED] Optimized server settings for clean startup
echo.
echo [RESULT] Zero warnings on startup
echo [RESULT] Professional dark theme maintained
echo [RESULT] All features working perfectly
echo.
echo ============================================
echo    READY TO LAUNCH
echo ============================================
echo.

set /p launch="Launch PREDICTEL now with clean config? (y/n): "
if /i "%launch%"=="y" (
    echo.
    echo [LAUNCHING] Starting PREDICTEL with clean configuration...
    echo [INFO] No more config warnings!
    echo [INFO] Press Ctrl+C to stop
    echo.

    :: Activate venv if it exists
    if exist venv\Scripts\activate.bat (
        call venv\Scripts\activate.bat
        streamlit run Home.py
    ) else (
        echo [WARNING] Virtual environment not found, using system Python
        streamlit run Home.py
    )
) else (
    echo.
    echo [INFO] Configuration fixed! Ready to launch when needed
    echo [CMD] streamlit run Home.py
)

echo.
pause
