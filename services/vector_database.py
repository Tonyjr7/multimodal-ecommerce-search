from pinecone import Pinecone
import logging

import settings

# Configure logging
logger = logging.getLogger(__name__)

"""Load Pinecone Index"""
PINECONE_API_KEY = settings.PINECONE_API_KEY
INDEX_NAME = settings.INDEX_NAME

try:
    pc = Pinecone(api_key=PINECONE_API_KEY)
    pinecone_index = pc.Index(INDEX_NAME)
except Exception as e:
    logger.error(f"Error loading Pinecone index: {e}")
    pinecone_index = None