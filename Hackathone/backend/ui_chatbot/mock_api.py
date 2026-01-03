"""
Mock API for chatbot when Qdrant is unavailable
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import random
import time

app = FastAPI()

class ChatRequest(BaseModel):
    query: str
    highlighted_text: Optional[str] = None

class ChatResponse(BaseModel):
    content: str
    response_id: str
    timestamp: str
    generation_time: float
    confidence_score: float

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Mock chat endpoint that returns simulated responses"""
    import uuid
    from datetime import datetime

    # Simulate processing delay
    time.sleep(random.uniform(0.5, 1.5))

    # Mock responses based on query content
    query_lower = request.query.lower()

    if "hello" in query_lower or "hi" in query_lower:
        response_content = "Hello! I'm your Book Assistant. How can I help you with the Physical AI & Humanoid Robotics content today?"
    elif "robot" in query_lower or "ai" in query_lower:
        response_content = "Physical AI and robotics involve creating intelligent systems that can interact with the physical world. This includes perception, reasoning, and action capabilities in robotic systems."
    elif "ros" in query_lower:
        response_content = "ROS (Robot Operating System) is a flexible framework for writing robot software. It provides services designed for a heterogeneous computer cluster such as hardware abstraction, device drivers, libraries, visualizers, message-passing, and package management."
    elif "gazebo" in query_lower or "simulation" in query_lower:
        response_content = "Gazebo is a 3D simulation environment for robotics. It provides realistic physics simulation, high-quality graphics, and convenient programmatic interfaces for creating and rendering complex environments."
    elif "nvidia" in query_lower or "isaac" in query_lower:
        response_content = "NVIDIA Isaac is a robotics platform that provides simulation, navigation, manipulation, and perception capabilities. It leverages NVIDIA's GPU computing for advanced AI in robotics applications."
    elif "vla" in query_lower or "vision" in query_lower:
        response_content = "Vision-Language-Action (VLA) models integrate visual perception, language understanding, and action execution. These models enable robots to understand natural language commands and perform appropriate physical actions."
    else:
        responses = [
            f"I found information about '{request.query}' in the Physical AI & Humanoid Robotics book. This topic covers the integration of perception, reasoning, and action in robotic systems.",
            f"Regarding '{request.query}', the book explains how modern humanoid robots combine multiple AI systems to achieve complex behaviors and tasks.",
            f"The Physical AI & Humanoid Robotics book discusses '{request.query}' as part of the broader framework of embodied intelligence and physical interaction systems.",
            f"Based on the book content, '{request.query}' relates to how robots can perceive their environment, make decisions, and execute physical actions effectively."
        ]
        response_content = random.choice(responses)

    return ChatResponse(
        content=response_content,
        response_id=str(uuid.uuid4()),
        timestamp=datetime.now().isoformat(),
        generation_time=random.uniform(0.2, 1.0),
        confidence_score=random.uniform(0.7, 0.95)
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "mock-chat-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)