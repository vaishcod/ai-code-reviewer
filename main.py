from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
import json
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

# ✅ Home
@app.get("/")
def home():
    return FileResponse("index.html")

# ✅ Input
class CodeInput(BaseModel):
    code: str

# ✅ API KEY
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ✅ MAIN REVIEW API
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
                        "content": f"""
You are a senior software engineer.

Analyze the code and return ONLY JSON:

{{
 "score": number (0-10),
 "issues": ["list of issues"],
 "suggestions": ["improvements"],
 "corrected_code": "fixed version"
}}

Code:
{data.code}
"""
                    }
                ]
            }
        )

        result = response.json()

        if "choices" in result:
            ai_text = result["choices"][0]["message"]["content"]

            try:
                parsed = json.loads(ai_text)
                return parsed
            except:
                return {"raw": ai_text}

        else:
            return {"error": result}

    except Exception as e:
        return {"error": str(e)}
