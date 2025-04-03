from fastapi import FastAPI
from app.models.health_check import HealthCheck
from app.routers import chromadb_router

app = FastAPI()
app.include_router(chromadb_router.router)


@app.get("/health_check")
def get_health():
    return HealthCheck()
