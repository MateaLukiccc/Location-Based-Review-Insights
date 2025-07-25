from chromadb import PersistentClient
from chromadb.utils import embedding_functions
import pandas as pd
from typing import List
from app.config import settings
from functools import lru_cache

@lru_cache
def get_chroma_client():
    return PersistentClient(path="./chroma_db")

@lru_cache
def get_collection(client, collection_name, embedding_function_name = "all-mpnet-base-v2"):
    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=embedding_function_name)
    return client.get_collection(name=collection_name, embedding_function=embedding_function)

def populate_collection_dataframe(collection, path_to_dataframe: str, id_col: str, document_col: str, additional_cols: List[str], embedding_function_name = "all-mpnet-base-v2"):
    df = pd.read_csv(path_to_dataframe, usecols=[id_col, document_col, *additional_cols])
    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=embedding_function_name)
    collection = get_chroma_client().get_or_create_collection(settings.COLLECTION_NAME, embedding_function=embedding_function)
    
    if collection.count() == 0:
        ids = df[id_col].astype(str).tolist() 
        documents = df[document_col].tolist()
        metadatas = df[additional_cols].to_dict(orient='records')
        
        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )
    else:
        print(f"Collection '{settings.COLLECTION_NAME}' already contains {collection.count()} items. Skipping population.")
    
    
def get_entries_keyword(collection, keyword):
    results = collection.query(query_texts=[keyword], where_document={"$contains": keyword})
    return results

def get_enties_similarity(collection, keyword, distance_bound):
    results = collection.query(query_texts=[keyword])
    filtered_results = {
        "ids": [],
        "documents": [],
        "metadatas": [],
        "distances": [],
    }

    if results["distances"] and results["ids"]:
        for i, distance in enumerate(results["distances"][0]):
            if distance <= distance_bound:
                filtered_results["ids"].append(results["ids"][0][i])
                filtered_results["documents"].append(results["documents"][0][i])
                filtered_results["metadatas"].append(results["metadatas"][0][i])

    return filtered_results
    
    
def get_entries_by_distance(collection, keyword: str, distance_bound: float=1.1):
    similarity_dict = get_enties_similarity(collection, keyword, distance_bound)
    keyword_dict = get_entries_keyword(collection, keyword)
    similarity_dict["ids"].extend(keyword_dict.get("ids", []))
    similarity_dict["documents"].extend(keyword_dict.get("documents", []))
    similarity_dict["metadatas"].extend(keyword_dict.get("metadatas", []))
    return similarity_dict

def get_entries(collection, keyword: str, limit: int):
    return collection.query(query_texts=[keyword], n_results=limit)

def get_entries_low(collection):
    return collection.get(where={"review_rating": {"$lte": 3}})

def get_entries_high(collection):
    return collection.get(where={"review_rating": {"$gte": 4}})

def get_all_entries(collection):
    results = collection.get(include=["documents"])
    if results and results["documents"]:
        return results["documents"]
    return []
