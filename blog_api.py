# blog_api.py

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from llm.core.generator import generate_blog
from dotenv import load_dotenv
load_dotenv() 
app = FastAPI()

# Optional: Allow requests from frontend (Flask or browser)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TopicRequest(BaseModel):
    topic: str
    breakdown: str = ""

@app.post("/generate_blog")
def create_blog(request: TopicRequest):
    response = generate_blog(topic=request.topic, breakdown=request.breakdown)
    return response  # Already returns dict with blog, image_prompts, image_urls
