import os
try:
    from pydantic_settings import BaseSettings
except ImportError:
    try:
        from pydantic import BaseSettings
    except ImportError:
        from pydantic import BaseModel
        class BaseSettings(BaseModel):
            pass

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI-Powered Criminal Network Intelligence System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "sih-secret-key-criminal-network-intelligence-2026-cyber-hub"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    
    # Databases
    USE_POSTGRES: bool = False  # Set to True when PostgreSQL is available
    POSTGRES_URI: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/criminal_intelligence")
    SQLITE_PATH: str = os.path.join(os.path.dirname(__file__), "..", "criminal_intelligence.db")
    
    USE_NEO4J: bool = False  # Set to True when Neo4j instance is running
    NEO4J_URI: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER: str = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "password")

    # Data Path
    DATASET_PATH: str = os.path.join(os.path.dirname(__file__), "..", "datasets", "synthetic_sih_data.json")

    class Config:
        case_sensitive = True

settings = Settings()
