from customer_support.components.data_ingestion import DataIngestionComponents
from customer_support.configuration import (
    DataIngestionConfig
)
from customer_support.logger import logging
from dataclasses import dataclass


@dataclass 
class DataIngestionPipeline:

    def run(self) -> None:
        """runs the full pipeline of training

        Returns:
            dict: output of all initialized objects as a single dict 
        """
        logging.info("In DataIngestionPipeline")

        # data ingestion
        data_ingestion=DataIngestionComponents(DataIngestionConfig)
        data_ingestion.main()
        
        logging.info("Out DataIngestionPipeline")
    

