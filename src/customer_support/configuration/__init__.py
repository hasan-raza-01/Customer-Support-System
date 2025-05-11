from customer_support.constants import (
    DataIngestionConstants
)
from dataclasses import dataclass
from pathlib import Path
import os


@dataclass
class DataIngestionConfig:
    GOOGLE_EMBEDDING_MODEL_NAME=DataIngestionConstants.GOOGLE_EMBEDDING_MODEL_NAME
    HUGGINGFACE_EMBEDDING_MODEL_NAME=DataIngestionConstants.HUGGINGFACE_EMBEDDING_MODEL_NAME
    DATA_DIR_PATH=Path(DataIngestionConstants.DATA_DIR_NAME)
    DATA_FILE_PATH=os.path.join(DATA_DIR_PATH, DataIngestionConstants.DATA_FILE_NAME)
    MONGODB_DATABASE_NAME=DataIngestionConstants.MONGODB_DATABASE_NAME
    MONGODB_COLLECTION_NAME=DataIngestionConstants.MONGODB_COLLECTION_NAME
    ASTRADB_KEYSPACE_NAME=DataIngestionConstants.ASTRADB_KEYSPACE_NAME
    ASTRADB_COLLECTION_NAME=DataIngestionConstants.ASTRADB_COLLECTION_NAME
    ASTRADB_K_VALUE=DataIngestionConstants.ASTRADB_K_VALUE
    ASTRADB_ENDPOINT=DataIngestionConstants.ASTRADB_ENDPOINT
    ASTRADB_TOKEN=DataIngestionConstants.ASTRADB_TOKEN
    MONGODB_URI=DataIngestionConstants.MONGODB_URI
    GROQ_API_KEY=DataIngestionConstants.GROQ_API_KEY
    GOOGLE_API_KEY=DataIngestionConstants.GOOGLE_API_KEY
    HF_TOKEN=DataIngestionConstants.HF_TOKEN


