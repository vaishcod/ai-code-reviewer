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

# ✅ Home route (VERY IMPORTANT)
@app.get("/")
def home():
    return {"message": "Backend running 🚀"}

# ✅ Input model
class CodeInput(BaseModel):
    code: str

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# ✅ Review route
@app.post("/review")
def review_code(data: CodeInput):
    code = data.code

    prompt = f"""
You are an expert code reviewer.

Analyze the following code and give:
1. Mistakes
2. Improvements
3. Security issues
4. Performance suggestions
5. Final score out of 10

Code:
{code}
"""

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
                    {"role": "user", "content": prompt}
                ]
            }
        )

        result = response.json()
        review = result["choices"][0]["message"]["content"]

        return {"review": review}

    except Exception as e:
        return {"review": f"❌ Error: {str(e)}"}


@app.get("/test-key")
def test_key():
    return {"key": str(OPENROUTER_API_KEY)}