from fastapi import APIRouter, HTTPException
from app.utils.chromadb_utils import get_collection, get_chroma_client, populate_collection_dataframe, get_entries_by_distance, get_entries, get_entries_high, get_entries_low
from app.config import settings
from app.utils.llm_utils import critique_reviews

populate_collection_dataframe(settings.COLLECTION_NAME, settings.DATA_PATH, settings.ID_COLUMN, settings.DOCUMENT_COL, [settings.ADDITIONAL_COL])

router = APIRouter(
    prefix="/chroma",
    tags=["VecorDB"]
)

chroma_client = get_chroma_client()
collection = get_collection(chroma_client, settings.COLLECTION_NAME)

@router.get("/documents/{keyword}/")
async def get_words(keyword: str, limit: int=5):
    try:
        results = get_entries(collection, keyword, limit)
        if not results["ids"]:
            raise HTTPException(status_code=404, detail="Item not found")
        return {
            "id": results["ids"][0],
            "text": results["documents"][0],
            "metadata": results["metadatas"][0]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/documents/distance/{keyword}")
async def get_words_distance(keyword: str, distance_bound: float=1.1):
    return get_entries_by_distance(collection, keyword, distance_bound)

@router.get("/documents/count")
async def get_entry_count():
    try:
        count = collection.count()
        return {"count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.get("/documents/summary")
def get_summary(keyword: str, distance_bound: float=1.1):
    relevant_reviews = get_entries_by_distance(collection, keyword, distance_bound)
    if not relevant_reviews:
        return "There are no reviews for this keyword"
    return critique_reviews(relevant_reviews.get("documents", []), keyword)

@router.get("/documents/good_summary")
def get_good_summary():
    # TODO: add summarizer
    return get_good_summary.get("documents", [])

@router.get("/documents/bad_summary")
def get_bad_summary():
    # TODO: add summarizer
    return get_bad_summary.get("documents", [])