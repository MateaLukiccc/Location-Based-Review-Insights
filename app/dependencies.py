import chromadb
from app.utils.chromadb_utils import get_chroma_client, get_collection
from app.config import settings


def get_db_collection() -> chromadb.Collection:
    client = get_chroma_client()
    collection = get_collection(client, settings.COLLECTION_NAME)
    if collection is None:
        raise RuntimeError(f"ChromaDB collection '{settings.COLLECTION_NAME}' not found.")
    return collection