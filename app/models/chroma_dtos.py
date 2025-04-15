from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class Item(BaseModel):
    id: str
    text: str
    metadata: Dict[str, Any] = {}

class AddItems(BaseModel):
    items: List[Item]

class UpdateItem(BaseModel):
    id: str
    text: str
    metadata: Dict[str, Any] = {}

class Query(BaseModel):
    query_texts: List[str]
    n_results: int = 5
    where: Optional[Dict[str, Any]] = None