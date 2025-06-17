from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search # Or other search tools
import os
from dotenv import load_dotenv
from .import prompt

load_dotenv()



def semantic_search_mongodb(query: str, limit: int = 5) -> list:
    """
    Perform semantic search in MongoDB using vector embeddings.
    
    Args:
        query: The search query text
        limit: Maximum number of results to return (default: 5)
        
    Returns:
        List of documents matching the query, sorted by relevance
    """
    from vertexai.language_models import TextEmbeddingModel
    from pymongo import MongoClient
    import os
    
    # Get MongoDB connection details from environment variables
    MONGODB_URI = os.environ.get("MONGODB_URI")
    DB_NAME = os.environ.get("DB_NAME")
    COLLECTION_NAME = os.environ.get("COLLECTION_NAME")
    
    if not MONGODB_URI or not DB_NAME or not COLLECTION_NAME:
        return {"error": "MongoDB connection details not configured in environment variables"}
    
    try:
        # Connect to MongoDB
        client = MongoClient(MONGODB_URI)
        collection = client[DB_NAME][COLLECTION_NAME]
        
        # Generate embedding for the query using Vertex AI
        model = TextEmbeddingModel.from_pretrained("gemini-embedding-001")
        embeddings = model.get_embeddings([query])
        
        if not embeddings or len(embeddings) == 0:
            return {"error": "Failed to generate embedding for query"}
            
        query_embedding = embeddings[0].values
        
        # Perform vector search in MongoDB Atlas
        results = collection.aggregate([
            {
                "$vectorSearch": {
                    "index": "vector_index",  # Make sure this matches your index name
                    "queryVector": query_embedding,
                    "path": "embedding",
                    "numCandidates": 100,
                    "limit": limit
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "id": 1,
                    "content": 1,
                    "score": {"$meta": "vectorSearchScore"},
                    "metadata": 1
                }
            }
        ])
        
        # Convert results to list
        results_list = list(results)
        
        # Format the results for better readability
        formatted_results = []
        for doc in results_list:
            formatted_doc = {
                "id": doc.get("id"),
                "content": doc.get("content"),
                "score": doc.get("score"),
                "metadata": doc.get("metadata", {})
            }
            formatted_results.append(formatted_doc)
            
        return formatted_results
        
    except Exception as e:
        return {"error": f"Error performing semantic search: {str(e)}"}

# --- 3. Create Your Simple Agent ---
# The Agent class orchestrates the model and tools.
# Provide clear instructions to guide the agent's behavior.
vsearch_agent = Agent(
    model="gemini-2.0-flash-001",
    name="mongogeq_Agent",
    description= prompt.MODEL_DESCRIPTION,
    instruction= prompt.VSEARCH_PROMPT,
    tools=[
        semantic_search_mongodb
    ]
)
