from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict
from fastopic import FASTopic
from topmost.preprocess import Preprocess
import numpy as np
from transformers import pipeline
import chromadb
from app.dependencies import get_db_collection
from app.utils.chromadb_utils import get_all_entries

#TODO: put models and preprocess in dependencies and get routes to be smaller use utils for topics

router = APIRouter(
    prefix="/topics",
    tags=["Topic Analysis"]
)

preprocess = Preprocess()
model = FASTopic(4, preprocess) 
sentiment_analyzer = pipeline("sentiment-analysis")

@router.post("/analyze")
async def analyze_reviews(collection: chromadb.Collection = Depends(get_db_collection)):
    """Performs topic analysis and sentiment analysis on all reviews in ChromaDB."""
    review_texts = get_all_entries(collection)
    if not review_texts:
        raise HTTPException(status_code=404, detail="No reviews found in ChromaDB.")

    # Fit the topic model
    top_words, doc_topic_dist = model.fit_transform(review_texts)

    topic_results = []
    for topic_idx in range(len(model.get_topic_weights())):
        # topic_name = f"Topic {topic_idx}"  # Consider more descriptive naming
        topic_words = model.get_topic(topic_idx=topic_idx)
        new_topic_words = tuple()
        for word, num in topic_words:
            new_topic_words = new_topic_words + (word, float(num))
        topic_words = new_topic_words

        topic_documents = [review_texts[i] for i, dist in enumerate(doc_topic_dist) if np.argmax(dist) == topic_idx]

        positive_comments = []
        negative_comments = []
        sentiments = []

        for doc in topic_documents:
            sentiment = sentiment_analyzer(doc[:512])[0]
            sentiments.append(sentiment['label'])
            if sentiment['label'] == 'POSITIVE' and len(positive_comments) < 3:
                positive_comments.append(doc)
            elif sentiment['label'] == 'NEGATIVE' and len(negative_comments) < 3:
                negative_comments.append(doc)

        positive_percentage = sentiments.count('POSITIVE') / len(sentiments) * 100 if sentiments else 0
        negative_percentage = sentiments.count('NEGATIVE') / len(sentiments) * 100 if sentiments else 0

        sentiment_analysis_summary = {
            "positive_percentage": f"{float(positive_percentage):.2f}%",
            "negative_percentage": f"{float(negative_percentage):.2f}%",
            "neutral_percentage": f"{float(100 - positive_percentage - negative_percentage):.2f}%" if sentiments else "0.00%"
        }

        topic_results.append({
            "topic_id":topic_idx,
            "topic_words":topic_words,
            "sentiment_analysis":sentiment_analysis_summary,
            "positive_samples":positive_comments,
            "negative_samples":negative_comments
        })
    return topic_results