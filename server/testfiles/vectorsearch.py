import requests
import pymongo
from typing import List, Dict
from dotenv import load_dotenv

import json
import os

load_dotenv()
# === CONFIG ===
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
VECTOR_INDEX_NAME = os.getenv("VECTOR_INDEX_NAME")
EMBEDDING_ENDPOINT = os.getenv("EMBEDDING_ENDPOINT")

# === STEP 1: Get embedding from your endpoint ===
def get_query_embedding(text: str) -> List[float]:
    try:
        response = requests.post(
            EMBEDDING_ENDPOINT,
            json={"content": text},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        embedding = response.json().get("embedding", [])
        if not embedding:
            raise ValueError("Empty embedding returned")
        return embedding
    except Exception as e:
        print(f"[ERROR] Getting embedding: {str(e)}")
        return []

# === STEP 2: Query MongoDB with vector search ===
def semantic_search(query_text: str, limit: int = 5) -> List[Dict]:
    embedding = get_query_embedding(query_text)
    if not embedding:
        print("[ERROR] Cannot search without a valid embedding.")
        return []

    # Connect to MongoDB
    client = pymongo.MongoClient(MONGODB_URI)
    collection = client[DB_NAME][COLLECTION_NAME]

    pipeline = [
        {
            "$vectorSearch": {
                "index": VECTOR_INDEX_NAME,
                "path": "embedding",
                "queryVector": embedding,
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
    ]

    try:
        results = collection.aggregate(pipeline)
        return list(results)
    except Exception as e:
        print(f"[ERROR] MongoDB query failed: {str(e)}")
        return []
    

# === STEP 3: Save results to a file ===

def save_results_to_file(results: List[Dict], filename: str = "test_results.json", directory: str = "test"):
    """
    Save search results to a JSON file in a given directory.

    Args:
        results: The list of result documents.
        filename: Name of the output JSON file.
        directory: Folder where file should be saved.
    """
    try:
        # Create the test directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)

        # Path to file
        file_path = os.path.join(directory, filename)

        # Save to JSON file
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)

        print(f"[✅] Results saved to: {file_path}")
    except Exception as e:
        print(f"[ERROR] Saving results to file: {str(e)}")


# === TEST ===
if __name__ == "__main__":
    query = "headache and fever after medicine"
    docs = semantic_search(query, limit=5)
    print(f"\nTop results for: \"{query}\"\n")
    for doc in docs:
        print(doc)
    
    if docs:
        save_results_to_file(docs)
    else:
        print("[!] No results found.")
