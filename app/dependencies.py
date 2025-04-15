import chromadb
from app.utils.chromadb_utils import get_chroma_client, get_collection
from app.utils.redis_utils import get_redis_client
from app.utils.models_utils import get_fastopic_model, get_distilbert_sentiment
from app.config import settings

def get_db_collection() -> chromadb.Collection:
    client = get_chroma_client()
    collection = get_collection(client, settings.COLLECTION_NAME)
    if collection is None:
        raise RuntimeError(f"ChromaDB collection '{settings.COLLECTION_NAME}' not found.")
    return collection

def get_cache_db():
    return get_redis_client()

def get_topic_model(num_topics: int = 4):
    return get_fastopic_model(num_topics)

def get_sentiment_model():
    return get_distilbert_sentiment()



    