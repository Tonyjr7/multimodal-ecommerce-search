"""
Configuration settings for AI E-commerce Search application.
Loads environment variables with proper defaults and validation.
"""
import os
from decouple import config

# Pinecone Configuration
PINECONE_API_KEY = config('PINECONE_API_KEY', default='')

# Flask Configuration
FLASK_ENV = config('FLASK_ENV', default='production')
FLASK_DEBUG = config('FLASK_DEBUG', default=False, cast=bool)

# Application Settings
INDEX_NAME = config('INDEX_NAME', default='ecommerce-products')
DATA_PATH = config('DATA_PATH', default='./datasets/Cleaned_Dataset.csv')

# Model Paths
CNN_MODEL_PATH = config('CNN_MODEL_PATH', default='ecommerce_cnn_model.h5')
CLASS_NAMES_PATH = config('CLASS_NAMES_PATH', default='class_names.pkl')

# Server Configuration
HOST = config('HOST', default='0.0.0.0')
PORT = config('PORT', default=5000, cast=int)
WORKERS = config('WORKERS', default=2, cast=int)

# Validate required settings
if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY environment variable is required")

# Validate file paths
if not os.path.exists(DATA_PATH):
    print(f"Warning: Data file not found at {DATA_PATH}")

if not os.path.exists(CNN_MODEL_PATH):
    print(f"Warning: CNN model not found at {CNN_MODEL_PATH}")

if not os.path.exists(CLASS_NAMES_PATH):
    print(f"Warning: Class names file not found at {CLASS_NAMES_PATH}")
