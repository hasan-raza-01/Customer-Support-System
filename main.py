from customer_support.pipeline.data_ingestion_pipeline import DataIngestionPipeline
from customer_support.pipeline.retrieval_pipeline import RetrievalPipeline



if __name__ == "__main__":
    # data ingestion
    data_ingestion_pipeline = DataIngestionPipeline()
    data_ingestion_pipeline.run()
    
    # data retrieval
    retrieval_pipeline = RetrievalPipeline()

    # test
    query = "Can you tell me the low budget headphone?"
    result=retrieval_pipeline.run(query)
    print(result)


