from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import Item
from .database import items_collection
from bson import ObjectId
import json

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom JSON encoder to handle ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with MongoDB"}

@app.get("/items")
async def get_items():
    items = list(items_collection.find())
    return json.loads(json.dumps(items, cls=JSONEncoder))

@app.post("/items")
async def create_item(item: Item):
    result = items_collection.insert_one(item.dict())
    return {"id": str(result.inserted_id), "item": item}

@app.get("/items/{item_id}")
async def get_item(item_id: str):
    item = items_collection.find_one({"_id": ObjectId(item_id)})
    if item:
        return json.loads(json.dumps(item, cls=JSONEncoder))
    raise HTTPException(status_code=404, detail="Item not found")