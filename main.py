from customer_support.pipeline.training_pipeline import TrainingPipeline
from customer_support.configuration import DataIngestionConfig



if __name__ == "__main__":
    training_pipeline = TrainingPipeline()
    training_outputs = training_pipeline.run()
    retriever = training_outputs["retriever"]
    query = "Can you tell me the low budget headphone?"
    k=DataIngestionConfig.ASTRADB_K_VALUE
    results=retriever.invoke(query, k=k)
    for res in results:
        print("="*50)
        print(res)
        print("="*50)


