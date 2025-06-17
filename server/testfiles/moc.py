import os
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Get MongoDB connection string from environment variables
MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME")
COLLECTION_NAME = os.environ.get("COLLECTION_NAME")

def test_mongodb_connection():
    """
    Test MongoDB connection by inserting a test document
    """
    # Validate environment variables
    if not MONGODB_URI:
        print("ERROR: MONGODB_URI environment variable is not set")
        return False
    
    if not DB_NAME:
        print("WARNING: DB_NAME environment variable is not set, using 'test' as default")
        db_name = "test"
    else:
        db_name = DB_NAME
        
    if not COLLECTION_NAME:
        print("WARNING: COLLECTION_NAME environment variable is not set, using 'test_connection' as default")
        collection_name = "test_connection"
    else:
        collection_name = COLLECTION_NAME
    
    try:
        # Connect to MongoDB
        print(f"Attempting to connect to MongoDB with URI: {MONGODB_URI[:20]}...")
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        
        # Test the connection
        client.admin.command('ping')
        print("Connection successful! Server is available.")
        
        # Get database and collection
        db = client[db_name]
        collection = db[collection_name]
        
        # Create a test document
        test_doc = {
            "test_id": "connection_test",
            "message": "This is a test document to verify MongoDB connection",
            "timestamp": datetime.now(),
            "temporary": True
        }
        
        # Insert the test document
        result = collection.insert_one(test_doc)
        
        print(f"Test document inserted with ID: {result.inserted_id}")
        print(f"Database: {db_name}, Collection: {collection_name}")
        
        # Verify insertion by retrieving the document
        retrieved_doc = collection.find_one({"test_id": "connection_test"})
        if retrieved_doc:
            print("Document successfully retrieved from MongoDB!")
            print(f"Retrieved document: {retrieved_doc}")
            
            # Optional: Delete the test document
            if input("Do you want to delete the test document? (y/n): ").lower() == 'y':
                collection.delete_one({"test_id": "connection_test"})
                print("Test document deleted.")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Failed to connect to MongoDB: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== MongoDB Connection Test ===")
    test_mongodb_connection()