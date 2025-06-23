from fastapi import APIRouter, HTTPException, Depends
from app.utils.chromadb_utils import get_entries_by_distance, get_entries, get_all_entries
import chromadb
from app.dependencies import get_db_collection

router = APIRouter(
    prefix="/chroma",
    tags=["VecorDB"]
)

@router.get("/documents/{keyword}/")
async def get_words(keyword: str, limit: int=5, collection: chromadb.Collection = Depends(get_db_collection)):
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
async def get_words_distance(keyword: str, distance_bound: float=1.1, collection: chromadb.Collection = Depends(get_db_collection)):
    return get_entries_by_distance(collection, keyword, distance_bound)

@router.get("/documents/count")
async def get_entry_count(collection: chromadb.Collection = Depends(get_db_collection)):
    try:
        count = collection.count()
        return {"count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def fetch_all_reviews(collection: chromadb.Collection = Depends(get_db_collection)):
    try:
        results = get_all_entries(collection)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching reviews from ChromaDB: {e}")