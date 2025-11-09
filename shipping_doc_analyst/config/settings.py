"""Application configuration management."""
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenAI Configuration
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4", env="OPENAI_MODEL")
    openai_embedding_model: str = Field(
        default="text-embedding-3-large", 
        env="OPENAI_EMBEDDING_MODEL"
    )
    
    # Google Drive Configuration
    google_drive_credentials_path: str | None = Field(
        default=None,
        env="GOOGLE_DRIVE_CREDENTIALS_PATH"
    )
    google_drive_input_folder_id: str | None = Field(
        default=None,
        env="GOOGLE_DRIVE_INPUT_FOLDER_ID"
    )
    google_drive_output_folder_id: str | None = Field(
        default=None,
        env="GOOGLE_DRIVE_OUTPUT_FOLDER_ID"
    )
    
    # FAISS Configuration
    faiss_index_path: Path = Field(
        default=Path("./data/faiss_index"),
        env="FAISS_INDEX_PATH"
    )
    faiss_index_type: str = Field(default="IndexFlatIP", env="FAISS_INDEX_TYPE")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: str | None = Field(default="./logs/app.log", env="LOG_FILE")
    
    # Processing Configuration
    batch_size: int = Field(default=10, env="BATCH_SIZE")
    max_workers: int = Field(default=4, env="MAX_WORKERS")
    processing_timeout: int = Field(default=120, env="PROCESSING_TIMEOUT")
    
    # Evaluation Configuration
    confidence_threshold: float = Field(default=0.7, env="CONFIDENCE_THRESHOLD")
    similarity_threshold: float = Field(default=0.8, env="SIMILARITY_THRESHOLD")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# Global settings instance
settings = Settings()
