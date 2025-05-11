from dataclasses import dataclass
from pathlib import Path


@dataclass
class DataIngestion:
    GOOGLE_EMBEDDING_MODEL_NAME:str
    HUGGINGFACE_EMBEDDING_MODEL_NAME:str
    DATA_DIR_PATH:Path
    DATA_FILE_PATH:str
    MONGODB_DATABASE_NAME:str
    MONGODB_COLLECTION_NAME:str
    ASTRADB_KEYSPACE_NAME:str
    ASTRADB_COLLECTION_NAME:str
    ASTRADB_K_VALUE:int
    ASTRADB_ENDPOINT:str
    ASTRADB_TOKEN:str
    MONGODB_URI:str
    GROQ_API_KEY:str
    GOOGLE_API_KEY:str
    HF_TOKEN:str


