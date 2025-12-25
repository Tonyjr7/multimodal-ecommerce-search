from flask import Blueprint, request, jsonify
import logging

from services.vision_service import vision_service
from utils.input_validation import validate_image_file

# Configure logging
logger = logging.getLogger(__name__)

# Create Blueprint for Vision Search Route
vision_search_bp = Blueprint('vision_search', __name__)

# Vision Search Route
@vision_search_bp.route('/api/vision', methods=['POST'])
def api_vision():
    """
    Processes an uploaded image to classify it using a CNN model and retrieve
    similar products from the vector database.

    Args:
        file (FileStorage): The image file uploaded by the user.

    Returns:
        dict: A dictionary containing the predicted class and a list of matching products.
    """
    if 'file' not in request.files: 
        logger.error("No file provided")
        return jsonify({"error": "No file"}), 400

    is_valid, error_msg = validate_image_file(request.files['file'])
    if not is_valid:
        return jsonify({"error": error_msg}), 400

    try:
        result = vision_service(request.files['file'])
        logger.info(f"Vision processing result: {result}")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in vision processing: {str(e)}")
        return jsonify({"error": str(e)}), 500