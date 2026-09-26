from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import FileResponse
import os
import google.generativeai as genai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini setup - Free da chellam!
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

class Question(BaseModel):
    question: str

@app.get("/")
async def read_index():
    return FileResponse('index.html')

@app.post("/ask")
async def ask_question(q: Question):
    if not model:
        return {"answer": "API Key set pannala da chellam, Render la GEMINI_API_KEY check pannu!"}
    try:
        response = model.generate_content(q.question)
        return {"answer": response.text}
    except Exception as e:
        return {"answer": f"Error da: {str(e)}"}
