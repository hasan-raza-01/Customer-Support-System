from langchain_google_genai import GoogleGenerativeAIEmbeddings
from customer_support.utils import create_dirs, load_yaml
from langchain_huggingface import HuggingFaceEmbeddings
from customer_support.exception import CustomException
from customer_support.entity import DataIngestion
from langchain_astradb import AstraDBVectorStore
from langchain_core.documents import Document
from customer_support.logger import logging
from customer_support.cloud import S3_Cloud
from dataclasses import dataclass
from pymongo import MongoClient
from box import ConfigBox
import pandas as pd
import os, sys


@dataclass
class DataIngestionComponents:
    __data_ingestion_config:DataIngestion

    @staticmethod
    def collection_to_dataframe(collection)->pd.DataFrame:
        """converts mongodb collection into pandas dataframe

        Args:
            collection (mongodb collection): collection which needs to convert into dataframe

        Returns:
            pandas.DataFrame
        """
        try:
            logging.info("In collection_to_dataframe")

            # collection mongodb collection 
            df = pd.DataFrame(collection.find())
            logging.info("data successfully converted (mongodb collection ===> pandas DataFrame)")

            # converting mongodb collection into pandas dataframe
            df = df.drop("_id", axis = 1)

            logging.info("Out collection_to_dataframe")
            return df
        except Exception as e:
            logging.exception(e)
            raise CustomException(e, sys)
        
    @staticmethod
    def validate_data(data:pd.DataFrame, old_schema:ConfigBox)->bool:
        """validates the data based on provided schema

        Args:
            data (pd.DataFrame): dataframe object for validation
            schema (ConfigBox): configbox object as schema for validation

        Returns:
            bool: True if schema matches else False
        """
        try:
            logging.info("In validate_data")

            # create required vars
            schema = dict()
            columns_with_dtype = dict()
            numerical_columns = list()

            for col in data.columns:
                columns_with_dtype[col] = str(data[col].dtype)
                if data[col].dtype!="O":
                    numerical_columns.append(col)

            schema["columns"] = columns_with_dtype
            schema["numerical_columns"] = numerical_columns

            logging.info("regenerated schema")

            new_schema=ConfigBox(schema)
            status= True if old_schema==new_schema else False
            logging.info(f"validation status:{status}")

            logging.info("Out validate_data")
            return status
        except Exception as e:
            logging.exception(e)
            raise CustomException(e, sys)
        
    def push_to_cloud(self, config, file_path) -> bool:
        try:
            logging.info("In push_to_cloud")

            cloud=S3_Cloud(
                bucket=config.DATA_INGESTION.S3_BUCKET,
                object_name=config.DATA_INGESTION.S3_OBJECT
            )
            status = cloud.upload_file(file_path)
            logging.info(f"status of cloud push {{{status}}}")

            logging.info("Out push_to_cloud")
            return status
        except Exception as e:
            logging.exception(e)
            raise CustomException(e, sys)

    def collect_data(self)->None:
        """collects data from data base and saves locally
        """
        try:
            logging.info("In collect_data")

            # create required dirs
            create_dirs(self.__data_ingestion_config.DATA_DIR_PATH)

            # creating environment variable HUGGINGFACE_API_TOKEN
            os.environ["HUGGINGFACE_API_TOKEN"] = self.__data_ingestion_config.HF_TOKEN
            
            # connecting to mongodb
            MONGODB_URI = self.__data_ingestion_config.MONGODB_URI
            client = MongoClient(MONGODB_URI)
            client.admin.command('ping')
            logging.info("You are successfully connected to MongoDB!")

            database_name = self.__data_ingestion_config.MONGODB_DATABASE_NAME
            collection_name = self.__data_ingestion_config.MONGODB_COLLECTION_NAME
            
            # collection mongodb collection
            collection = client[database_name][collection_name]

            # converting mongodb collection into pandas dataframe
            self.data_frame = self.collection_to_dataframe(collection)
            logging.info(f"collected data from mongodb, DATABASE: {database_name} and COLLECTION: {collection_name}")
            
            # saving data into local file path
            file_path = self.__data_ingestion_config.DATA_FILE_PATH
            self.data_frame.to_csv(file_path, index=False, header=True)
            logging.info(f"Data saved at {file_path}")

            # save data to s3
            config=load_yaml("config/config.yaml")
            self.push_to_cloud(config, file_path)

            logging.info("Out collect_data")
        except Exception as e:
            logging.exception(e)
            raise CustomException(e, sys)
        
    def load_embedding_model(self)->None:
        """loads the embedding model
        """
        try:
            logging.info("In load_embeddings")
            try:
                model_name = self.__data_ingestion_config.GOOGLE_EMBEDDING_MODEL_NAME
                self.embeddings = GoogleGenerativeAIEmbeddings(model=model_name)
            except:
                model_name = self.__data_ingestion_config.HUGGINGFACE_EMBEDDING_MODEL_NAME
                self.embeddings = HuggingFaceEmbeddings(
                    model_name = model_name, 
                    model_kwargs = {"device": "cpu"}, 
                    encode_kwargs = {"normalize_embeddings": True}
                )
            logging.info(f"loaded embedding model {{{model_name}}}")
            logging.info("Out load_embeddings")
        except Exception as e:
            logging.exception(e)
            raise CustomException(e, sys)
        
    def format_data_for_insertion(self)->list[Document]:
        """converts data into required format for insertion in vector store
        """
        try:
            logging.info("In format_data_for_insertion")

            docs = []
            columns = list(self.data_frame.columns)
            columns.remove("review")
            for _, row in self.data_frame.iterrows():
                metadata = {col:row[col] for col in columns}
                doc = Document(page_content=row["review"], metadata=metadata)
                docs.append(doc)
            logging.info(f"total number of records formated {{{len(docs)}}}")
                
            logging.info("Out format_data_for_insertion")
            return docs
        except Exception as e:
            logging.exception(e)
            raise

    def get_vector_store(self)->AstraDBVectorStore:
        """returns dict of astradb config
        """
        try:
            logging.info("In get_vector_store")

            self.load_embedding_model()
            vstore = AstraDBVectorStore(
                collection_name=self.__data_ingestion_config.ASTRADB_COLLECTION_NAME,
                embedding=self.embeddings,
                api_endpoint=self.__data_ingestion_config.ASTRADB_ENDPOINT,
                token=self.__data_ingestion_config.ASTRADB_TOKEN,
                namespace=self.__data_ingestion_config.ASTRADB_KEYSPACE_NAME,
            )
            logging.info("Out get_vector_store")
            return vstore
        except Exception as e:
            logging.exception(e)
            raise
        
    def insert_data(self)->int:
        """Inserts data into vectorstore
        """
        try:
            logging.info("In insert_data")

            # create vector store instance
            self.vector_store = self.get_vector_store()

            # format the data into list of document object
            docs = self.format_data_for_insertion()

            # insert documents into vector store
            total_records_inserted = len(self.vector_store.add_documents(documents = docs))
            logging.info(f"total number of records inserted in vectorstore {{{total_records_inserted}}}")
            
            logging.info("Out insert_data")
            return total_records_inserted
        except Exception as e:
            logging.exception(e)
            raise CustomException(e, sys)
        
    def main(self):
        self.collect_data()
        schema=load_yaml("schema/schema.yaml")
        status=self.validate_data(self.data_frame, schema)
        if status:
            self.insert_data()
        else:
            logging.info(f"collected data and provided schema given {{status:'\{status}'\}}, skipping the upcomming data ingestion.")


