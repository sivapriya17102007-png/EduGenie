import os
import google.generativeai as genai
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

class Question(BaseModel):
    question: str

@app.api_route("/", methods=["GET", "HEAD"])
async def home():
    # index.html irukka path check pannuthu
    if os.path.exists("index.html"):
        return FileResponse("index.html")
    return {"status": "EduGenie is Live!"}

@app.post("/ask")
async def ask(q: Question):
    try:
        response = model.generate_content(q.question)
        return {"answer": response.text}
    except Exception as e:
        return {"answer": f"Error da chellam: {str(e)}"}
