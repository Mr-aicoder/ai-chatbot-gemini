import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def ask_groq(prompt: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "GROQ_API_KEY is missing. Add it to your .env file."
    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content or "No response generated."
    except Exception as exc:
        return f"Groq API error: {exc}"


def get_response(prompt: str) -> str:
    return ask_groq(prompt)
