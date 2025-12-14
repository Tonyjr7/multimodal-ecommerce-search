@echo off
REM Quick Start Script for AI E-commerce Search (Windows)
REM This script helps you get started quickly

echo ========================================
echo AI E-commerce Search - Quick Start
echo ========================================
echo.

REM Check if .env exists
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo WARNING: Please edit .env and add your PINECONE_API_KEY
    echo.
    pause
)

REM Check for required files
echo Checking for required model files...
set MISSING_FILES=0

if not exist "ecommerce_cnn_model.h5" (
    echo Missing: ecommerce_cnn_model.h5
    set MISSING_FILES=1
)

if not exist "class_names.pkl" (
    echo Missing: class_names.pkl
    set MISSING_FILES=1
)

if not exist "datasets\Cleaned_Dataset.csv" (
    echo Missing: datasets\Cleaned_Dataset.csv
    set MISSING_FILES=1
)

if %MISSING_FILES%==1 (
    echo.
    echo WARNING: Some required files are missing.
    echo Please ensure all model files are present.
    echo.
    pause
) else (
    echo All required files found!
)

echo.
echo Choose deployment method:
echo 1) Docker (Recommended)
echo 2) Local Python
echo.
set /p choice="Enter choice (1 or 2): "

if "%choice%"=="1" (
    echo.
    echo Starting with Docker...
    
    REM Check if Docker is running
    docker version >nul 2>&1
    if errorlevel 1 (
        echo Docker is not running. Please start Docker Desktop first.
        pause
        exit /b 1
    )
    
    echo Building and starting containers...
    docker-compose up --build -d
    
    echo.
    echo Application started successfully!
    echo.
    echo Access the application at: http://localhost:5000
    echo Health check: http://localhost:5000/health
    echo.
    echo To view logs: docker-compose logs -f
    echo To stop: docker-compose down
    
) else if "%choice%"=="2" (
    echo.
    echo Starting with local Python...
    
    REM Check if Python is installed
    python --version >nul 2>&1
    if errorlevel 1 (
        echo Python is not installed. Please install Python 3.10+ first.
        pause
        exit /b 1
    )
    
    REM Create virtual environment if it doesn't exist
    if not exist "venv" (
        echo Creating virtual environment...
        python -m venv venv
    )
    
    REM Activate virtual environment
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
    
    REM Install dependencies
    echo Installing dependencies...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    
    REM Check for Tesseract
    tesseract --version >nul 2>&1
    if errorlevel 1 (
        echo.
        echo WARNING: Tesseract OCR is not installed.
        echo OCR features will not work.
        echo Download from: https://github.com/UB-Mannheim/tesseract/wiki
        echo.
    )
    
    echo.
    echo Starting application...
    start python main.py
    
    timeout /t 3 /nobreak >nul
    
    echo.
    echo Application started successfully!
    echo.
    echo Access the application at: http://localhost:5000
    echo Health check: http://localhost:5000/health
    echo.
    
) else (
    echo Invalid choice. Exiting.
    pause
    exit /b 1
)

echo.
echo Setup complete! Happy searching!
pause
