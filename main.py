import os
import io
import pickle
import numpy as np
import pandas as pd
import tensorflow as tf
from flask import Flask, request, jsonify, render_template
from pyngrok import ngrok
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from PIL import Image
import logging
import easyocr

from utils.ocr import ocr_core
from utils.image_processor import prepare_image

import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- CONFIGURATION ---
PINECONE_API_KEY = settings.PINECONE_API_KEY

# EasyOCR Initialization
ocr_reader = easyocr.Reader(['en']) 

app = Flask(__name__)

# 1. Load Recommendation Models
logger.info("Loading Pinecone & Embeddings...")
pc = Pinecone(api_key=PINECONE_API_KEY)
pinecone_index = pc.Index(settings.INDEX_NAME)
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Load Vision Models (CNN)
logger.info("Loading CNN...")
cnn_model = tf.keras.models.load_model(settings.CNN_MODEL_PATH)
with open(settings.CLASS_NAMES_PATH, 'rb') as f:
    class_names = pickle.load(f)

# 3. Load Data & Fallbacks
try:
    df = pd.read_csv(settings.DATA_PATH)
    product_lookup = df.set_index(df['StockCode'].astype(str).str.strip())['Description'].to_dict()
except Exception as e:
    logger.warning(f"Could not load data from {settings.DATA_PATH}: {e}")
    product_lookup = {}

DEMO_PRODUCT_MAP = {
    "22727": "ALARM CLOCK BAKELIKE RED", "22423": "REGENCY CAKESTAND 3 TIER",
    "20726": "LUNCH BAG WOODLAND", "21034": "REX CASH+CARRY JUMBO SHOPPER",
    "21931": "JUMBO STORAGE BAG SUKI", "22077": "6 RIBBONS RUSTIC CHARM",
    "22112": "CHOCOLATE HOT WATER BOTTLE", "22139": "RETROSPOT TEA SET CERAMIC 11 PC",
    "22384": "LUNCH BAG PINK POLKADOT", "23298": "SPOTTY BUNTING"
}
product_lookup.update(DEMO_PRODUCT_MAP)

# --- PAGE ROUTING ---
@app.route('/')
def page_text(): return render_template('text.html')

@app.route('/ocr')
def page_ocr(): return render_template('ocr.html')

@app.route('/vision')
def page_vision(): return render_template('vision.html')

# Health check endpoint for Docker/monitoring
@app.route('/health')
def health_check():
    """Health check endpoint for container orchestration and monitoring"""
    try:
        # Check if models are loaded
        if pinecone_index and embed_model and cnn_model:
            return jsonify({
                "status": "healthy",
                "service": "AI E-commerce Search",
                "models": {
                    "pinecone": "connected",
                    "embeddings": "loaded",
                    "cnn": "loaded"
                }
            }), 200
        else:
            return jsonify({"status": "unhealthy", "error": "Models not loaded"}), 503
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 503

# --- API ENDPOINTS ---

# API 1: Text Search
@app.route('/api/text', methods=['POST'])
def api_text():
    data = request.get_json()
    query = data.get('query', '')
    vector = embed_model.encode(query).tolist()
    results = pinecone_index.query(vector=vector, top_k=5, include_metadata=True)
    matches = [m['metadata'] for m in results['matches']]
    return jsonify({"message": f"Showing results for: '{query}'", "products": matches})

# API 2: Handwriting OCR (Updated for Tesseract)
@app.route('/api/ocr', methods=['POST'])
def api_ocr():
    if 'file' not in request.files: return jsonify({"error": "No file"}), 400
    file = request.files['file']
    try:
        # Read file bytes
        file_bytes = file.read()
        
        # expected result format: [[bbox, text, conf], [bbox, text, conf]]
        result = ocr_reader.readtext(file_bytes)
        
        # Combine all detected words into one sentence
        detected_text = " ".join([res[1] for res in result])
        
        if not detected_text or len(detected_text) < 2:
            return jsonify({"error": "Could not read handwriting. Try writing clearer."}), 400

        print(f"DEBUG OCR Read: {detected_text}") # debug printing on collab

        # Search Pinecone Index
        vector = embed_model.encode(detected_text).tolist()
        results = pinecone_index.query(vector=vector, top_k=5, include_metadata=True)
        return jsonify({"detected_text": detected_text, "products": [m['metadata'] for m in results['matches']]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API 3: Vision (CNN)
@app.route('/api/vision', methods=['POST'])
def api_vision():
    if 'file' not in request.files: return jsonify({"error": "No file"}), 400
    try:
        processed = prepare_image(request.files['file'].read())
        preds = cnn_model.predict(processed)
        idx = np.argmax(preds[0])
        stock_code = class_names[idx]
        confidence = float(np.max(preds[0]) * 100)
        
        description = product_lookup.get(stock_code, "Unknown Product")
        
        similar_items = []
        if description != "Unknown Product":
            vector = embed_model.encode(description).tolist()
            related = pinecone_index.query(vector=vector, top_k=3, include_metadata=True)
            similar_items = [m['metadata'] for m in related['matches']]
        
        return jsonify({
            "detected_product": description,
            "detected_stock_code": stock_code,
            "confidence": f"{confidence:.1f}%",
            "similar_products": similar_items
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
