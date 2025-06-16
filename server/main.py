from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
from dotenv import load_dotenv
import os

app = FastAPI()



load_dotenv()  

dogapi = os.getenv("dogapi")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    content: str

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Simple API"}

@app.get("/message")
async def get_default_message():
    return {"message": "This is the default message from the server"}

@app.post("/message")
async def create_message(message: Message):
    return {"received": message.content, "status": "Message received successfully!"}

@app.get("/devtest")
async def returnDev():
    return {"message": "Hi this is for dev testing"}

@app.get("/dog-breeds")
async def get_dog_breeds():
    url = dogapi

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch dog breeds"}