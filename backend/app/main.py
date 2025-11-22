from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import chatbot

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chatbot.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Chatbot API!"} 