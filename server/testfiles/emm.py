import os
import time
import vertexai
from dotenv import load_dotenv

from vertexai.language_models import TextEmbeddingModel

load_dotenv()  # Load environment variables from .env file
project_id = os.getenv("PROJECT_ID")  # Get project id from environment variable
if not project_id:
    raise ValueError("PROJECT_ID environment variable is not set.")

def test_embedding():
    """Simple test for Vertex AI embeddings"""
    print("Testing Vertex AI embedding model...")
    vertexai.init(project="your-project-id", location="us-central1")

    # Initialize the model
    model = TextEmbeddingModel.from_pretrained("gemini-embedding-001")
    
    # Test text
    test_text = "Hello, world! This is a test."
    print(f"Getting embedding for text: '{test_text}'")
    
    # Generate embedding
    embedding = model.get_embeddings([test_text])
    
    # Print results
    embedding_dimension = len(embedding[0].values)
    print(f"Success! Embedding dimension: {embedding_dimension}")
    print(f"First 5 values: {embedding[0].values[:5]}")
    
    return True

if __name__ == "__main__":
    test_embedding()