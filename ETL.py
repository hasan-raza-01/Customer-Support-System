from customer_support.exception import CustomException
from customer_support.utils import load_yaml
import sys
import pymongo
from typing import ClassVar
import pandas as pd
import json
import os
import certifi
from dotenv import load_dotenv
from dataclasses import dataclass
import yaml


# loading environment variable
load_dotenv()
uri = os.getenv("MONGODB_URI")

# connecting safely
ca = certifi.where()

# load yaml file
database=load_yaml("config/config.yaml")["DATA_INGESTION"]["MONGODB_DATABASE_NAME"]
collection=load_yaml("config/config.yaml")["DATA_INGESTION"]["MONGODB_DATABASE_NAME"]

@dataclass
class ExtractTransformLoad:
    __Client: ClassVar = pymongo.MongoClient(uri)
    __Database: ClassVar = __Client[database]
    __Collection: ClassVar = __Database[collection]

    def csv_to_json(self, path:str)-> list:
        """Converts csv file into a list of json

        Args:
            path (str): path of CSV file where data is available.

        Returns:
            list: list of json for the whole file.
        """
        try:
            self.data = pd.read_csv(path)
            records = list(json.loads(self.data.T.to_json()).values())
            return records
        except Exception as e:
            raise CustomException(e, sys)
        
    def push_to_db(self, records:list, collection:list)-> int:
        """pushes all records into collection of database

        Args:
            records (list): list of json
            collection (id): mongoclient database collection full id

        Returns:
            int: lenght of records
        """
        try:
            self.records = records
            self.collection = collection
            self.collection.insert_many(self.records)
            return len(records)
        except Exception as e:
            raise CustomException(e, sys)
        
    def save_schema(self)->None:
        """saves the schema data
        """
        try:
            path = "schema"
            os.makedirs(path, exist_ok=True)

            schema = dict()
            columns_with_dtype = dict()
            numerical_columns = list()

            for col in self.data.columns:
                columns_with_dtype[col] = str(self.data[col].dtype)
                if self.data[col].dtype!="O":
                    numerical_columns.append(col)

            schema["columns"] = columns_with_dtype
            schema["numerical_columns"] = numerical_columns

            with open(os.path.join(path, "schema.yaml"), "w") as file:
                yaml.safe_dump(schema, file)
        except Exception as e:
            raise CustomException(e, sys)
        
    def main(self)-> int:
        """Runs the full ETL process
        """
        path = "D:/MyDatasets/CustomerSupportSystem/flipkart_product_review.csv"
        collection = ExtractTransformLoad.__Collection
        records = self.csv_to_json(path)
        records_len = self.push_to_db(records, collection)
        self.save_schema()
        return records_len
        


if __name__=="__main__":
    ETL_obj = ExtractTransformLoad()
    print(ETL_obj.main(), "records inserted to mongodb") # length of records inserted
