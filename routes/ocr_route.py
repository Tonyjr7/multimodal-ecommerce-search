from flask import Blueprint
from flask import request, jsonify

from services.ocr_service import ocr_service
from services.embed_model import embed_model
from services.vector_database import pinecone_index
from utils.input_validation import validate_image_file

# Blueprint for OCR Search Route
ocr_search_bp = Blueprint('ocr_search', __name__)

# API 2: Handwriting OCR (Uses EasyOCR)
@ocr_search_bp.route('/api/ocr', methods=['POST'])
def api_ocr():
    """
    Processes an uploaded image to extract text using EasyOCR and retrieve
    similar products from the vector database.

    Args:
        file (FileStorage): The image file uploaded by the user.

    Returns:
        dict: A dictionary containing the detected text and a list of matching products.
    """

    if 'file' not in request.files: 
        return jsonify({"error": "No file"}), 400
    
    # Add validation
    is_valid, error_msg = validate_image_file(request.files['file'])
    if not is_valid:
        return jsonify({"error": error_msg}), 400

    if pinecone_index is None:
        return jsonify({"error": "Pinecone index not loaded"}), 503
    
    try:
        detected_text = ocr_service(request.files['file'])

        if not detected_text or len(detected_text) < 2:
            return jsonify({"error": "No text detected. Try writing clearer."}), 400

        # Search Vector Database (Pinecone)
        vector = embed_model.encode(detected_text).tolist()
        results = pinecone_index.query(vector=vector, top_k=5, include_metadata=True)
        
        return jsonify({
            "detected_text": detected_text, 
            "products": [m['metadata'] for m in results['matches']]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500