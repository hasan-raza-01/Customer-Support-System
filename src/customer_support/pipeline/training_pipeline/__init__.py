from customer_support.components.data_ingestion import DataIngestionComponents
from customer_support.configuration import (
    DataIngestionConfig
)
from customer_support.logger import logging
from dataclasses import dataclass


@dataclass 
class TrainingPipeline:

    def run(self)->dict:
        """runs the full pipeline of training

        Returns:
            dict: output of all initialized objects as a single dict 
        """
        logging.info("In TrainingPipeline")

        # data ingestion
        data_ingestion=DataIngestionComponents(DataIngestionConfig)
        data_ingestion.main()
        retriever = data_ingestion.get_vector_store().as_retriever()


        logging.info("Out TrainingPipeline")
        return {
            "retriever":retriever
        }
    

