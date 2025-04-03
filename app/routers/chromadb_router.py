from fastapi import APIRouter, HTTPException
from app.utils.chromadb_utils import get_collection, get_chroma_client, populate_collection_dataframe
from app.config import settings

populate_collection_dataframe(settings.COLLECTION_NAME, settings.DATA_PATH, settings.ID_COLUMN, settings.DOCUMENT_COL, [settings.ADDITIONAL_COL])

router = APIRouter(
    prefix="/chroma",
    tags=["VecorDB"]
)

chroma_client = get_chroma_client()
collection = get_collection(chroma_client, settings.COLLECTION_NAME)

@router.get("/documents/{keyword}/")
async def read_item(keyword: str, limit: int=5):
    try:
        results = collection.query(query_texts=[keyword], n_results=limit)
        if not results["ids"]:
            raise HTTPException(status_code=404, detail="Item not found")
        return {
            "id": results["ids"][0],
            "text": results["documents"][0],
            "metadata": results["metadatas"][0]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/entries/count")
async def get_entry_count():
    try:
        count = collection.count()
        return {"count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
