from customer_support.components.data_retrieval import RetrievalComponents
from customer_support.configuration import RetrievalConfig
from customer_support.logger import logging


class RetrievalPipeline:
    def __init__(self) -> None:
        self.retrieval=RetrievalComponents(RetrievalConfig)
        self.retrieval.main()
        
    def run(self, query:str) -> str:
        """invokes the pipeline with given query

        Args:
            query (str): user query to invoke pipeline

        Returns:
            str: string output of chain
        """
        logging.info("In RetrievalPipeline")

        result=self.retrieval.invoke(query)

        logging.info("Out RetrievalPipeline")

        return result


