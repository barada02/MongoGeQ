from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Sample Item",
                "description": "This is a sample item",
                "price": 29.99
            }
        }