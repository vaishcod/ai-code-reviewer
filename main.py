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
print("API KEY:", OPENROUTER_API_KEY)

@app.post("/review")
def review_code(data: CodeInput):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://ai-code-reviewer-2-pufo.onrender.com",
                "X-Title": "AI Code Reviewer"
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {"role": "user", "content": data.code}
                ]
            }
        )

        print("STATUS:", response.status_code)
        print("RAW RESPONSE:", response.text)

        return response.json()

    except Exception as e:
        print("EXCEPTION:", str(e))
        return {"error": str(e)}

# ✅ Test API key
@app.get("/test-key")
def test_key():
    return {"key": str(OPENROUTER_API_KEY)}