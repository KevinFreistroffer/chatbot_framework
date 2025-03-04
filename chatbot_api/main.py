from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import json
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chatbot_framework.main import Chatbot

app = FastAPI(title="Chatbot API")

def load_data():
    try:
        with open("chatbot_framework/data/training_data.json", "r") as f:
            training_data = json.load(f)
    except FileNotFoundError:
        training_data = []
    
    try:
        with open("chatbot_framework/data/templates.json", "r") as f:
            templates = json.load(f)
    except FileNotFoundError:
        templates = {}
    
    return training_data, templates

training_data, templates = load_data()
chatbot = Chatbot(training_data=training_data, templates=templates)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    intent: str
    confidence: float
    entities: list

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        result = await chatbot.process_message(request.message)
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reset")
async def reset_conversation():
    chatbot.reset_conversation()
    return { "status": "success", "message": "Conversation reset"}
