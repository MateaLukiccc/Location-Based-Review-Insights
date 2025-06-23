from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    COLLECTION_NAME: str = Field(..., env="COLLECTION_NAME")
    DATA_PATH: str = Field(..., env="DATA_PATH")
    ID_COLUMN: str = Field(..., env="ID_COLUMN")
    DOCUMENT_COL: str = Field(..., env="DOCUMENT_COL")
    ADDITIONAL_COL: str = Field(..., env="ADDITIONAL_COL")
    GEMINI_API_KEY: str = Field(..., env="GEMINI_API_KEY")
    REDIS_HOST: str = Field(..., env="REDIS_HOST")
    REDIS_PORT: int = Field(..., env="REDIS_PORT")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_file_encoding="utf-8",
        case_sensitive=True,
        env_nested_delimiter="__",
    )

settings = Settings()