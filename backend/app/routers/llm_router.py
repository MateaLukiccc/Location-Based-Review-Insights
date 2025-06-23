from fastapi import APIRouter, Depends
from app.utils.llm_utils import critique_reviews, generate_positive_summary, generate_negative_summary
import chromadb
from app.utils.chromadb_utils import get_entries_by_distance, get_entries_high, get_entries_low
from app.dependencies import get_db_collection

router = APIRouter(
    prefix="/llm",
    tags=["LLM"]
)

@router.get("/summary")
def get_summary(keyword: str, distance_bound: float=1.1, collection: chromadb.Collection = Depends(get_db_collection)):
    relevant_reviews = get_entries_by_distance(collection, keyword, distance_bound)
    if not relevant_reviews:
        return "There are no reviews for this keyword"
    return critique_reviews(relevant_reviews.get("documents", []), keyword)

@router.get("/good_summary")
def get_good_summary(collection: chromadb.Collection = Depends(get_db_collection)):
    reviews = get_entries_high(collection).get("documents", [])
    return generate_positive_summary("\n".join(reviews))

@router.get("/bad_summary")
def get_bad_summary(collection: chromadb.Collection = Depends(get_db_collection)):
    reviews = get_entries_low(collection).get("documents", [])
    return generate_negative_summary("\n".join(reviews))