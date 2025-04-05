from app.config import settings
from app.constants.prompts import get_summarize_reviews_prompt, system_summarize_prompt
from google import genai
from google.genai import types

def critique_reviews(text, keyword: str):
    client = genai.Client(
        api_key=settings.GEMINI_API_KEY,
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[
            types.Content(
                parts=[
                    {"text": system_summarize_prompt},
                    {"text": get_summarize_reviews_prompt(keyword, text)}
                ],
                role="user"
            )
        ]
    )
    return response.text