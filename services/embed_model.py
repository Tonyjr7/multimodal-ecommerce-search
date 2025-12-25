from sentence_transformers import SentenceTransformer
import logging

# Configure logging
logger = logging.getLogger(__name__)

"""Load the embedding model (all-MiniLM-L6-v2)"""
try:
    embed_model = SentenceTransformer('all-MiniLM-L6-v2')
    logger.info("Embedding model loaded successfully")
except Exception as e:
    logger.error(f"Error loading embedding model: {e}")
    embed_model = None  # Set fallback