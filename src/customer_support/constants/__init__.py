from customer_support.utils import load_yaml
from dataclasses import dataclass
from dotenv import load_dotenv
import os


load_dotenv()
CONFIG=load_yaml("config/config.yaml")

@dataclass
class DataIngestionConstants:
    GOOGLE_EMBEDDING_MODEL_NAME=CONFIG.MODELS.EMBEDDING.GOOGLE
    HUGGINGFACE_EMBEDDING_MODEL_NAME=CONFIG.MODELS.EMBEDDING.HUGGINGFACE
    DATA_DIR_NAME=CONFIG.DATA_INGESTION.DATA_DIR_NAME
    DATA_FILE_NAME=CONFIG.DATA_INGESTION.DATA_FILE_NAME
    MONGODB_DATABASE_NAME=CONFIG.DATA_INGESTION.MONGODB_DATABASE_NAME
    MONGODB_COLLECTION_NAME=CONFIG.DATA_INGESTION.MONGODB_COLLECTION_NAME
    ASTRADB_KEYSPACE_NAME=CONFIG.DATA_INGESTION.ASTRADB_KEYSPACE_NAME
    ASTRADB_COLLECTION_NAME=CONFIG.DATA_INGESTION.ASTRADB_COLLECTION_NAME
    ASTRADB_K_VALUE=int(CONFIG.DATA_INGESTION.ASTRADB_K_VALUE)
    ASTRADB_ENDPOINT=os.getenv("ASTRADB_ENDPOINT")
    ASTRADB_TOKEN=os.getenv("ASTRADB_TOKEN")
    MONGODB_URI=os.getenv("MONGODB_URI")
    GROQ_API_KEY=os.getenv("GROQ_API_KEY")
    GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
    HF_TOKEN=os.getenv("HF_TOKEN")


@dataclass
class RetrievalConstants:
    GEMINI_PRO_NAME=CONFIG.MODELS.REASONER.GEMINI_PRO
    DEEPSEEK_R1_NAME=CONFIG.MODELS.REASONER.DEEPSEEK_R1
    PROMPT_TEMPLATES = {
        "product_bot": """
        You are an expert EcommerceBot specialized in product recommendations and handling customer queries.
        Analyze the provided product titles, ratings, and reviews to provide accurate, helpful responses.
        Stay relevant to the context, and keep your answers concise and informative.

        CONTEXT:
        {context}

        QUESTION: {question}

        YOUR ANSWER:
        """
    }


