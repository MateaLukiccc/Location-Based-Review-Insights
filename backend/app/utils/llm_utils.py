from app.config import settings
from app.constants.prompts import get_summarize_reviews_prompt, system_summarize_prompt, structure_reviews, system_negative_prompt, system_positive_prompt, system_topics_prompt
from google import genai
from google.genai import types
from typing import List
from pydantic import BaseModel


class TopicName(BaseModel):
    name_of_topic: str

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

def generate_positive_summary(reviews: str):
    client = genai.Client(
        api_key=settings.GEMINI_API_KEY,
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[
            types.Content(
                parts=[
                    {"text": system_positive_prompt},
                    {"text": structure_reviews(reviews)}
                ],
                role="user"
            )
        ]
    )
    return response.text

def generate_negative_summary(reviews: str):
    client = genai.Client(
        api_key=settings.GEMINI_API_KEY,
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[
            types.Content(
                parts=[
                    {"text": system_negative_prompt},
                    {"text": structure_reviews(reviews)}
                ],
                role="user"
            )
        ]
    )
    return response.text


def generate_topic_summary(topic_words: List[str]):
    client = genai.Client(
        api_key=settings.GEMINI_API_KEY,
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[
            types.Content(
                parts=[
                    {"text": system_topics_prompt},
                    {"text": structure_reviews(topic_words)}
                ],
                role="user"
            )
        ],
        config={
        "response_mime_type": "application/json",
        "response_schema": TopicName,
        }
    )
    return response.text