from flask import Flask, render_template, jsonify
import logging
import easyocr

from routes.text_route import text_search_bp
from routes.ocr_route import ocr_search_bp
from routes.vision_route import vision_search_bp

from services.model_service import cnn_model
from services.embed_model import embed_model
from services.vector_database import pinecone_index

# --- LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

# --- FLASK APP ---
app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

# --- BLUEPRINT ROUTING ---
app.register_blueprint(text_search_bp)
app.register_blueprint(ocr_search_bp)
app.register_blueprint(vision_search_bp)

# --- PAGE ROUTING ---
@app.route('/health')
def health():
    """Health check endpoint for monitoring."""
    return jsonify({
        "status": "healthy",
        "models": {
            "cnn_model": cnn_model is not None,
            "embed_model": embed_model is not None,
            "pinecone_index": pinecone_index is not None
        }
    })

@app.route('/')
def page_text(): 
    return render_template('text.html')

@app.route('/ocr')
def page_ocr(): 
    return render_template('ocr.html')

@app.route('/vision')
def page_vision(): 
    return render_template('vision.html')

# --- RUN APP ---
if __name__ == '__main__':
    app.run(port=5000)
