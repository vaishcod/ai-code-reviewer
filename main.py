from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Home
@app.get("/")
def home():
    return {"message": "Backend running 🚀"}

# Input model
class CodeInput(BaseModel):
    code: str

# API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ✅ REVIEW FUNCTION (SEPARATE)
@app.post("/review")
def review_code(data: CodeInput):
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {
                        "role": "user",
                        "content": f"Review this code:\n\n{data.code}"
                    }
                ]
            }
        )

        result = response.json()

        if "choices" in result:
            return {
                "review": result["choices"][0]["message"]["content"]
            }
        else:
            return {
                "error": result
            }

    except Exception as e:
        return {"error": str(e)}

# ✅ MODELS FUNCTION (ALAG)
@app.get("/models")
def get_models():
    return requests.get(
        "https://api.groq.com/openai/v1/models",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}"}
    ).json()