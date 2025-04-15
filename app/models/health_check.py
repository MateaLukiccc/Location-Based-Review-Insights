from pydantic import BaseModel

class HealthCheck(BaseModel):
    health: str = "OK"