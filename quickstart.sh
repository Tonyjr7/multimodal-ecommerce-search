#!/bin/bash

# Quick Start Script for AI E-commerce Search
# This script helps you get started quickly

set -e

echo "🚀 AI E-commerce Search - Quick Start"
echo "======================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your PINECONE_API_KEY"
    echo ""
    read -p "Press Enter after you've updated .env file..."
fi

# Check for required files
echo "🔍 Checking for required model files..."
MISSING_FILES=0

if [ ! -f "ecommerce_cnn_model.h5" ]; then
    echo "❌ Missing: ecommerce_cnn_model.h5"
    MISSING_FILES=1
fi

if [ ! -f "class_names.pkl" ]; then
    echo "❌ Missing: class_names.pkl"
    MISSING_FILES=1
fi

if [ ! -f "datasets/Cleaned_Dataset.csv" ]; then
    echo "❌ Missing: datasets/Cleaned_Dataset.csv"
    MISSING_FILES=1
fi

if [ $MISSING_FILES -eq 1 ]; then
    echo ""
    echo "⚠️  Some required files are missing. Please ensure all model files are present."
    echo "   You can continue, but some features may not work."
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ All required files found!"
fi

echo ""
echo "Choose deployment method:"
echo "1) Docker (Recommended)"
echo "2) Local Python"
echo ""
read -p "Enter choice (1 or 2): " choice

case $choice in
    1)
        echo ""
        echo "🐳 Starting with Docker..."
        
        # Check if Docker is installed
        if ! command -v docker &> /dev/null; then
            echo "❌ Docker is not installed. Please install Docker first."
            exit 1
        fi
        
        # Check if docker-compose is installed
        if ! command -v docker-compose &> /dev/null; then
            echo "❌ docker-compose is not installed. Please install docker-compose first."
            exit 1
        fi
        
        echo "Building and starting containers..."
        docker-compose up --build -d
        
        echo ""
        echo "✅ Application started successfully!"
        echo ""
        echo "📍 Access the application at: http://localhost:5000"
        echo "🏥 Health check: http://localhost:5000/health"
        echo ""
        echo "To view logs: docker-compose logs -f"
        echo "To stop: docker-compose down"
        ;;
        
    2)
        echo ""
        echo "🐍 Starting with local Python..."
        
        # Check if Python is installed
        if ! command -v python3 &> /dev/null; then
            echo "❌ Python 3 is not installed. Please install Python 3.10+ first."
            exit 1
        fi
        
        # Check Python version
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        echo "Python version: $PYTHON_VERSION"
        
        # Create virtual environment if it doesn't exist
        if [ ! -d "venv" ]; then
            echo "Creating virtual environment..."
            python3 -m venv venv
        fi
        
        # Activate virtual environment
        echo "Activating virtual environment..."
        source venv/bin/activate
        
        # Install dependencies
        echo "Installing dependencies..."
        pip install --upgrade pip
        pip install -r requirements.txt
        
        # Check for Tesseract
        if ! command -v tesseract &> /dev/null; then
            echo "⚠️  Tesseract OCR is not installed. OCR features will not work."
            echo "   Install it with: sudo apt-get install tesseract-ocr (Ubuntu/Debian)"
            echo "                    brew install tesseract (macOS)"
        fi
        
        echo ""
        echo "Starting application..."
        python main.py &
        APP_PID=$!
        
        # Wait for app to start
        sleep 3
        
        echo ""
        echo "✅ Application started successfully!"
        echo ""
        echo "📍 Access the application at: http://localhost:5000"
        echo "🏥 Health check: http://localhost:5000/health"
        echo ""
        echo "To stop: kill $APP_PID"
        ;;
        
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "🎉 Setup complete! Happy searching!"
