from flask import Blueprint
from flask import request, jsonify

from services.embed_model import embed_model
from services.vector_database import pinecone_index

text_search_bp = Blueprint('text_search', __name__)

# API 1: Text Search
@text_search_bp.route('/api/text', methods=['POST'])
def api_text():
    """
    Processes a text query to retrieve similar products from the vector database.

    Args:
        query (str): The text query provided by the user.

    Returns:
        dict: A dictionary containing the query and a list of matching products.
    """

    # Get the query from the request
    data = request.get_json()
    query = data.get('query', '')
    
    # Validate the query
    if not query:
        return jsonify({"error": "No query provided"}), 400

    if pinecone_index is None:
        return jsonify({"error": "Pinecone service is unavailable"}), 503

    # Process the query
    vector = embed_model.encode(query).tolist()
    
    # Search the vector database
    results = pinecone_index.query(vector=vector, top_k=5, include_metadata=True)
    
    # Get the matches
    matches = [m['metadata'] for m in results['matches']]

    # Return the results
    return jsonify({"message": f"Showing results for: '{query}'", "products": matches})