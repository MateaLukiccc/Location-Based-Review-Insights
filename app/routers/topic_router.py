from fastapi import APIRouter, HTTPException, Depends
import numpy as np
import chromadb
from app.dependencies import get_db_collection, get_topic_model, get_sentiment_model, get_cache_db
from app.utils.chromadb_utils import get_all_entries
from app.utils.topic_utils import get_positive_negative_comments
from redis import Redis
import json
from app.config import settings

router = APIRouter(
    prefix="/topics",
    tags=["Topic Analysis"]
)

@router.get("/analyze")
async def analyze_reviews(collection_name: str = settings.COLLECTION_NAME, redis_client: Redis = Depends(get_cache_db), collection: chromadb.Collection = Depends(get_db_collection), model = Depends(get_topic_model), sentiment_analyzer = Depends(get_sentiment_model)):
    cache_key = f"analysis:{collection_name}"
    if cached_results := redis_client.get(cache_key):
        return json.loads(cached_results.decode('utf-8'))
    
    if not (review_texts := get_all_entries(collection)):
        raise HTTPException(status_code=404, detail="No reviews found in ChromaDB.")

    _, doc_topic_dist = model.fit_transform(review_texts)
    topic_results = []
    for topic_idx in range(len(model.get_topic_weights())):
        topic_words = model.get_topic(topic_idx=topic_idx)
        new_topic_words = tuple()
        for word, num in topic_words:
            new_topic_words = new_topic_words + (word, float(num))
        topic_words = new_topic_words

        topic_documents = [review_texts[i] for i, dist in enumerate(doc_topic_dist) if np.argmax(dist) == topic_idx]
        positive_percentage, negative_percentage, positive_comments, negative_comments = get_positive_negative_comments(topic_documents, sentiment_analyzer)
        
        sentiment_analysis_summary = {
            "positive_percentage": f"{float(positive_percentage):.2f}%",
            "negative_percentage": f"{float(negative_percentage):.2f}%"
        }

        topic_results.append({
            "topic_id":topic_idx,
            "topic_words":topic_words,
            "sentiment_analysis":sentiment_analysis_summary,
            "positive_samples":positive_comments,
            "negative_samples":negative_comments
        })
        
    redis_client.setex(cache_key, 3600, json.dumps(topic_results))
    return topic_results