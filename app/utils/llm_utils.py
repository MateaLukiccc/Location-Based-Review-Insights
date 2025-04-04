from groq import Groq
from app.config import settings
from app.constants.prompts import get_summarize_reviews_prompt, system_summarize_prompt

def critique_reviews(text, keyword: str):
    client = Groq(
        api_key=settings.GROQ_API_KEY,
    )
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_summarize_prompt
            },
            {
                "role": "user",
                "content": get_summarize_reviews_prompt(keyword, text),
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content