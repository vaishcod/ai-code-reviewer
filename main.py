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
                "model": "mixtral-8x7b-32768",
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