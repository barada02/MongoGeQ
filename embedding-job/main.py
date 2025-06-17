import json
import os
from typing import List, Dict, Any
import time

# Import Vertex AI libraries
from vertexai.language_models import TextEmbeddingModel
from pymongo import MongoClient

# === CONFIGURATION ===
PROJECT_ID = os.environ.get("PROJECT_ID")
LOCATION = os.environ.get("LOCATION", "us-central1")
MONGODB_URI = os.environ.get("MONGODB_URI", "your-mongodb-atlas-uri")
DB_NAME = os.environ.get("DB_NAME", "your_db")
COLLECTION_NAME = os.environ.get("COLLECTION_NAME", "your_collection")


# Ensure environment variables are set
if not PROJECT_ID or not MONGODB_URI:
    raise ValueError("Please set the PROJECT_ID and MONGODB_URI environment variables.")
# === SETUP MONGO ===
mongo_client = MongoClient(MONGODB_URI)
collection = mongo_client[DB_NAME][COLLECTION_NAME]

# === EMBEDDING FUNCTION USING VERTEX AI SDK ===
def get_embedding(text: str) -> List[float]:
    """
    Generate embeddings using Vertex AI's TextEmbeddingModel
    
    Args:
        text: The text to generate embeddings for
        
    Returns:
        List of float values representing the embedding
    """
    try:
        # Initialize the model
        model = TextEmbeddingModel.from_pretrained("gemini-embedding-001")
        
        # Get embeddings
        embeddings = model.get_embeddings([text])
        
        if embeddings and len(embeddings) > 0:
            # Return the values from the first embedding
            return embeddings[0].values
        else:
            print(f"Failed to generate embedding for text: {text[:50]}...")
            return None
    except Exception as e:
        print(f"Error generating embedding: {str(e)}")
        return None

# === INGEST SCRIPT ===
def insert_documents_from_json(filepath: str):
    """
    Insert documents from a JSON file into MongoDB Atlas with embeddings
    
    Args:
        filepath: Path to the JSON file containing documents
    """
    try:
        print(f"Loading data from {filepath}")
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        examples = data.get("examples", [])
        print(f"Found {len(examples)} documents to process")

        for i, example in enumerate(examples):
            doc_id = example.get("id")
            content = example.get("content")

            if not content:
                print(f"Skipping document {doc_id} - no content")
                continue

            print(f"Processing document {i+1}/{len(examples)}: {doc_id}")
            
            # Check if document already exists in collection
            existing_doc = collection.find_one({"id": doc_id})
            if existing_doc:
                print(f"Document {doc_id} already exists, skipping")
                continue
                
            # Generate embedding
            embedding = get_embedding(content)
            if embedding is None:
                print(f"Skipping document {doc_id} - failed to generate embedding")
                continue

            # Prepare document for MongoDB
            mongo_doc = {
                "id": doc_id,
                "content": content,
                "embedding": embedding,
                "annotations": example.get("annotations", []),
                "metadata": example.get("metadata", {})
            }

            # Insert document
            result = collection.insert_one(mongo_doc)
            print(f"Inserted document ID: {doc_id} (MongoDB _id: {result.inserted_id})")
            
            # Add a small delay to avoid rate limiting
            time.sleep(0.5)
            
        print(f"Completed processing {len(examples)} documents")
        
    except Exception as e:
        print(f"Error processing documents: {str(e)}")

# === QUERY FUNCTION ===
def semantic_search(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Perform semantic search using embeddings
    
    Args:
        query: The search query
        limit: Maximum number of results to return
        
    Returns:
        List of matching documents
    """
    try:
        # Generate embedding for the query
        query_embedding = get_embedding(query)
        if not query_embedding:
            return []
            
        # Perform vector search using $vectorSearch (MongoDB Atlas Vector Search)
        # Note: You need to set up a vector search index in MongoDB Atlas first
        results = collection.aggregate([
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "queryVector": query_embedding,
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
                    "annotations": 1,
                    "metadata": 1
                }
            }
        ])
        
        return list(results)
        
    except Exception as e:
        print(f"Error during semantic search: {str(e)}")
        return []

# === RUN ===
if __name__ == "__main__":
    json_file_path = "Corona2.json"
    insert_documents_from_json(json_file_path)