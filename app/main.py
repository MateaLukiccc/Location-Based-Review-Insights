from fastapi import FastAPI
from app.models.health_check import HealthCheck
from app.routers import chromadb_router, llm_router, topic_router
from app.utils.chromadb_utils import populate_collection_dataframe
from contextlib import asynccontextmanager
from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup...")
    print("Connecting to ChromaDB and populating collection if necessary...")
    try:
        print(f"Attempting to populate collection: {settings.COLLECTION_NAME}")
        populate_collection_dataframe(
            collection=settings.COLLECTION_NAME,
            path_to_dataframe=settings.DATA_PATH,
            id_col=settings.ID_COLUMN,
            document_col=settings.DOCUMENT_COL,
            additional_cols=[settings.ADDITIONAL_COL]
        )
        print(f"Collection '{settings.COLLECTION_NAME}' populated/verified.")

    except Exception as e:
        print(f"FATAL: Failed to initialize ChromaDB during startup: {e}")

    yield
    print("Application shutdown...")

app = FastAPI(
    title="Location-based Insights",
    description="Develop actionable insights using LLM models and ChromaDB",
    version="1.0.0",
    lifespan=lifespan
)
app.include_router(chromadb_router.router)
app.include_router(llm_router.router)
app.include_router(topic_router.router)

@app.get("/health_check")
def get_health():
    return HealthCheck()
