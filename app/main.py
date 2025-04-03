from fastapi import FastAPI
from models.health_check import HealthCheck

app = FastAPI()

@app.get("/health_check")
def get_health():
    return HealthCheck()
