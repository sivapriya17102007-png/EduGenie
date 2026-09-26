from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import FileResponse
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

@app.get("/")
def home():
    if os.path.exists("index.html"):
        return FileResponse("index.html")
    return {"message": "EduGenie Backend Running"}

@app.post("/ask")
def ask_genie(data: Question):
    q = data.question
    answer = f"Un kelvi: '{q}' ku answer: EduGenie AI yosikuthu! (Demo version)"
    return {"answer": answer}
