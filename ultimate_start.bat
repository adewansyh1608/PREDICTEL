@echo off
setlocal enabledelayedexpansion
echo.
echo ============================================
echo    PREDICTEL - Ultimate Start Script
echo    Clean Launch Without Directory Issues
echo ============================================
echo.

:: Set working directory to script location
cd /d "%~dp0"
echo [INFO] Working directory: %CD%

:: Check if we're in the right directory
if not exist Home.py (
    echo [ERROR] Home.py not found in current directory!
    echo [INFO] This script must be in the PREDICTEL folder
    echo [INFO] Current location: %CD%
    pause
    exit /b 1
)

:: Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found in PATH
    echo [SOLUTION] Install Python from https://python.org
    echo [SOLUTION] Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

:: Display Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo [INFO] Python version: %python_version%

:: Create/activate virtual environment
echo [STEP 1] Setting up isolated Python environment...
if not exist venv (
    echo [INFO] Creating new virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
)

:: Activate virtual environment (force absolute path)
echo [STEP 2] Activating virtual environment...
call "%CD%\venv\Scripts\activate.bat"
if errorlevel 1 (
    echo [WARNING] Standard activation failed, trying alternative method...
    set "VIRTUAL_ENV=%CD%\venv"
    set "PATH=%CD%\venv\Scripts;%PATH%"
)

:: Verify activation
python -c "import sys; print('[SUCCESS] Virtual environment active' if 'venv' in sys.prefix else '[WARNING] Using system Python')"

:: Update pip to latest version
echo [STEP 3] Updating package installer...
python -m pip install --upgrade pip --quiet

:: Install core dependencies (no cache to avoid directory issues)
echo [STEP 4] Installing core dependencies...
python -m pip install --no-cache-dir pandas>=1.5.0 numpy>=1.21.0 scikit-learn>=1.2.0 "streamlit>=1.29.0,<2.0.0" matplotlib>=3.5.0

:: Check core installation
python -c "import pandas, numpy, sklearn, streamlit, matplotlib; print('[SUCCESS] Core libraries installed')"
if errorlevel 1 (
    echo [ERROR] Core installation failed
    pause
    exit /b 1
)

:: Install optional enhanced libraries
echo [STEP 5] Installing enhanced visualization libraries...
python -m pip install --no-cache-dir seaborn>=0.11.0 plotly>=5.15.0 Pillow>=9.0.0 --quiet
if errorlevel 1 (
    echo [WARNING] Some enhanced libraries failed, using basic mode
)

:: Clear any cached configs
echo [STEP 6] Clearing cached configurations...
if exist "%USERPROFILE%\.streamlit" (
    rmdir /s /q "%USERPROFILE%\.streamlit" 2>nul
)

:: Create clean config directory
if not exist .streamlit mkdir .streamlit

:: Write minimal, clean config
echo [STEP 7] Creating clean configuration...
(
echo [theme]
echo primaryColor = "#0ea5e9"
echo backgroundColor = "#0a0a0a"
echo secondaryBackgroundColor = "#111111"
echo textColor = "#ffffff"
echo font = "sans serif"
echo.
echo [server]
echo headless = true
echo port = 8501
echo enableXsrfProtection = false
echo maxUploadSize = 200
echo.
echo [browser]
echo gatherUsageStats = false
echo.
echo [runner]
echo magicEnabled = true
echo.
echo [logger]
echo level = "info"
) > .streamlit\config.toml

:: Final verification
echo [STEP 8] Final system check...
python -c "
import sys
import os
print(f'[INFO] Python executable: {sys.executable}')
print(f'[INFO] Working directory: {os.getcwd()}')
print(f'[INFO] Virtual environment: {"YES" if "venv" in sys.prefix else "NO"}')

# Test critical imports
try:
    import streamlit
    import pandas
    import numpy
    import sklearn
    import matplotlib
    print('[SUCCESS] All core libraries working')

    # Test optional libraries
    extras = []
    try:
        import seaborn
        extras.append('seaborn')
    except ImportError:
        pass

    try:
        import plotly
        extras.append('plotly')
    except ImportError:
        pass

    if extras:
        print(f'[BONUS] Enhanced libraries: {", ".join(extras)}')
    else:
        print('[INFO] Using basic visualization mode')

except ImportError as e:
    print(f'[ERROR] Import test failed: {e}')
    exit(1)
"

if errorlevel 1 (
    echo [ERROR] System verification failed
    pause
    exit /b 1
)

:: Launch application
echo.
echo ============================================
echo    READY TO LAUNCH PREDICTEL!
echo ============================================
echo.
echo [LAUNCH INFO]
echo ✓ Clean environment: Isolated from system conflicts
echo ✓ Fresh configuration: No cached settings
echo ✓ Direct execution: Bypassing directory issues
echo ✓ Modern dark theme: Professional appearance
echo.
echo [APPLICATION FEATURES]
echo ✓ Customer Churn Prediction with ML
echo ✓ Advanced Data Preprocessing
echo ✓ Interactive Dark Theme Dashboard
echo ✓ Real-time Individual Predictions
echo ✓ Business Intelligence Analytics
echo.
echo [CONTROLS]
echo • Application will open in your default browser
echo • URL: http://localhost:8501
echo • Press Ctrl+C in this window to stop
echo • Close browser tab to stop using the app
echo.

set /p launch="Launch PREDICTEL now? (y/n): "
if /i "!launch!"=="y" (
    echo.
    echo [LAUNCHING] Starting PREDICTEL Customer Churn Analytics...
    echo [INFO] If browser doesn't open, manually go to: http://localhost:8501
    echo.

    :: Launch with clean environment
    streamlit run Home.py --server.headless true --server.port 8501 --browser.gatherUsageStats false

    if errorlevel 1 (
        echo.
        echo [RETRY] Trying alternative port...
        streamlit run Home.py --server.port 8502
    )

) else (
    echo.
    echo [INFO] PREDICTEL is ready to launch
    echo [CMD] To start later, run: streamlit run Home.py
    echo [CMD] Or double-click this script again
)

echo.
echo [INFO] Virtual environment remains active for this session
echo [INFO] To manually activate later: call venv\Scripts\activate.bat
echo.
pause
