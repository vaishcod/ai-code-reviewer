from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Home route
@app.get("/")
def home():
    return {"message": "Backend running 🚀"}

# ✅ Input model
class CodeInput(BaseModel):
    code: str

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# ✅ DEBUG REVIEW ROUTE
@app.post("/review")
def review_code(data: CodeInput):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {"role": "user", "content": data.code}
                ]
            }
        )

        return {
            "status_code": response.status_code,
            "response": response.text
        }

    except Exception as e:
        return {"error": str(e)}

# ✅ Test API key
@app.get("/test-key")
def test_key():
    return {"key": str(OPENROUTER_API_KEY)}