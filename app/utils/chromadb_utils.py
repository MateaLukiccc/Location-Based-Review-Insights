from chromadb import Client, Settings
from chromadb.utils import embedding_functions
import pandas as pd
from typing import List
from app.config import settings

def get_chroma_client():
    return Client(Settings(persist_directory="./chroma_db"))

def get_collection(client, collection_name, embedding_function_name = "all-mpnet-base-v2"):
    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=embedding_function_name)
    return client.get_collection(name=collection_name, embedding_function=embedding_function)

def populate_collection_dataframe(collection, path_to_dataframe: str, id_col: str, document_col: str, additional_cols: List[str], embedding_function_name = "all-mpnet-base-v2"):
    df = pd.read_csv(path_to_dataframe, usecols=[id_col, document_col, *additional_cols])
    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=embedding_function_name)
    collection = get_chroma_client().get_or_create_collection(settings.COLLECTION_NAME, embedding_function=embedding_function)
    
    ids = df[id_col].astype(str).tolist() 
    documents = df[document_col].tolist()
    metadatas = df[additional_cols].to_dict(orient='records')
    
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )
    
