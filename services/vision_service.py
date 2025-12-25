from werkzeug.datastructures.file_storage import FileStorage
import logging
import numpy as np

from services.model_service import cnn_model, class_names
from services.vector_database import pinecone_index
from services.embed_model import embed_model
from services import product_lookup

from utils.image_processor import prepare_image


# Configure Logging
logger = logging.getLogger(__name__)

"""Vision Service Using CNN"""
if not cnn_model or class_names is None:
    logger.error("Model or class names not loaded. Please check model_service.py")
    raise Exception("Model or class names not loaded")

def vision_service(file: FileStorage) -> dict:
    """
    Processes an uploaded image to classify it using a CNN model and retrieve
    similar products from the vector database.

    Args:
        file (FileStorage): The image file uploaded by the user.

    Returns:
        dict: A dictionary containing the predicted class and a list of matching products.
    """
    try:
        if not file:
            logger.error("No file provided")
            return {"error": "No file provided"}

        # Process image
        processed = prepare_image(file.read())

        if pinecone_index is None:
            logger.error("Pinecone index not loaded. Please check vector_database.py")
            raise Exception("Pinecone index not loaded")

        # Get predictions
        preds = cnn_model.predict(processed)
        idx = np.argmax(preds[0])
        stock_code = class_names[idx]
        confidence = float(np.max(preds[0]) * 100)
        
        # Get product description
        description = product_lookup.get(stock_code, "Unknown Product")
        
        # Get similar items
        similar_items = []
        if description != "Unknown Product" and embed_model and pinecone_index:
            vector = embed_model.encode(description).tolist()
            related = pinecone_index.query(vector=vector, top_k=3, include_metadata=True)
            similar_items = [m['metadata'] for m in related['matches']]
        
        return {
            "detected_product": description,
            "detected_stock_code": stock_code,
            "confidence": f"{confidence:.1f}%",
            "similar_products": similar_items
        }
    except Exception as e:
        logger.error(f"Error in vision processing: {str(e)}")
        return {"error": str(e)}




