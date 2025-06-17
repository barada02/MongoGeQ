from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search # Or other search tools
import os
from dotenv import load_dotenv

load_dotenv()


# --- 1. Define and Configure Your Vertex AI Model ---
# This initializes a Vertex AI model wrapper for ADK

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

modelinstruction = """
You are a specialized medical information assistant with access to a comprehensive database of medical conditions, medications, and pathogens. 

Your role is to provide accurate, reliable information about:
- Medical conditions and diseases (e.g., influenza, malaria, headaches)
- Medications and treatments (e.g., aspirin, penicillin, methotrexate)
- Pathogens and infectious agents (e.g., Coronavirus, Zika virus, E. coli)

To answer questions, you must:
1. ALWAYS use the semantic_search_mongodb tool to retrieve relevant information before answering
2. Formulate an effective search query that will return the most relevant documents
3. Review all retrieved documents carefully
4. Synthesize information from the documents to provide a comprehensive answer
5. If the search doesn't return relevant information, try reformulating your query and searching again

IMPORTANT GUIDELINES:
- Never make up or hallucinate information that isn't in the retrieved documents
- Clearly indicate when information is limited or not available in your database
- For medical questions outside your knowledge base, advise users to consult healthcare professionals
- Present information in a clear, organized manner suitable for general audiences
- Cite your sources by referencing document IDs when providing specific information

Remember: Your answers must be based SOLELY on information retrieved through the semantic_search_mongodb tool. Always search for information before attempting to answer."""

# --- 3. Create Your Simple Agent ---
# The Agent class orchestrates the model and tools.
# Provide clear instructions to guide the agent's behavior.
root_agent = Agent(
    model="gemini-2.0-flash-001",
    name="multi_tool_agent",
    description="""I am MedInfo, a specialized medical information assistant that provides accurate information about medical conditions, medications, and pathogens.

I can answer questions about:
- Medical conditions and diseases (such as influenza, malaria, headaches)
- Medications and treatments (like aspirin, penicillin, methotrexate)
- Pathogens and infectious agents (including Coronavirus, Zika virus, E. coli)

My answers are based on reliable medical information stored in a specialized database. I search this database in real-time to provide you with accurate, up-to-date information.

While I have access to a comprehensive knowledge base, I'm not a substitute for professional medical advice. For personal medical concerns, please consult with a qualified healthcare provider.

How can I help you with medical information today?""",
    instruction= modelinstruction,
    tools=[
        semantic_search_mongodb
    ]
)
