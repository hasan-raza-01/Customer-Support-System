from customer_support.components.data_ingestion import DataIngestionComponents
from customer_support.configuration import DataIngestionConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from customer_support.exception import CustomException 
from langchain_core.prompts import ChatPromptTemplate
from customer_support.entity import Retrieval
from customer_support.logger import logging 
from langchain_groq import ChatGroq
from dataclasses import dataclass 
import sys



@dataclass 
class RetrievalComponents:
    __retrieval_config:Retrieval

    def get_retriever(self) -> None:
        try:
            logging.info("In get_retriever")
            self.data_ingestion_components=DataIngestionComponents(DataIngestionConfig)
            self.retriever=self.data_ingestion_components.get_vector_store().as_retriever()

            logging.info("Out get_retriever")
        except Exception as e:
            logging.exception(e)
            raise CustomException(e, sys)
        
    def get_LLM(self):
        """loads large language model either gemini_pro or deepseek_r1
        """
        try:
            logging.info("In get_LLM")
            try:
                self.model_name=self.__retrieval_config.GEMINI_PRO_NAME
                self.llm=ChatGoogleGenerativeAI(model=self.model_name)
                logging.info(f"{self.model_name} loaded")
            except:
                self.model_name=self.__retrieval_config.DEEPSEEK_R1_NAME
                self.llm=ChatGroq(model=self.model_name)
                logging.info(f"{self.model_name} loaded")

            logging.info("Out get_LLM")
        except Exception as e:
            logging.exception(e)
            raise CustomException(e, sys)
        
    def get_chain(self):
        """create the chain
        """
        try:
            logging.info("In get_chain")
            self.prompt=ChatPromptTemplate.from_template(self.__retrieval_config.PROMPT_TEMPLATES["product_bot"])
            self.chain=(
                {"context": self.retriever, "question": RunnablePassthrough()}
                | self.prompt
                | self.llm
                | StrOutputParser()
            )
            logging.info("Out get_chain")
        except Exception as e:
            logging.exception(e)
            raise CustomException(e, sys)
        
    def invoke(self, query:str) -> str:
        """invokes the chain

        Args:
            query (str): user query

        Returns:
            str: output as string
        """
        try:
            logging.info("In invoke")
            result=self.chain.invoke(query)
            logging.info("Out invoke")
            return result
        except Exception as e:
            logging.exception(e)
            raise CustomException(e, sys)
        
    def main(self) -> None:
        self.get_retriever()
        self.get_LLM()
        self.get_chain()


