from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

load_dotenv()

es = Elasticsearch(os.getenv("ELASTICSEARCH_HOST"))

def index_document(document_id: str, metadata: dict):
    try:
        es.index(index="documents", id=document_id, body=metadata)
        return True
    except Exception as e:
        raise Exception(f"Failed to index document: {str(e)}")

def search_documents(query: str):
    try:
        result = es.search(index="documents", body={"query": {"match": {"_all": query}}})
        return result["hits"]["hits"]
    except Exception as e:
        raise Exception(f"Failed to search documents: {str(e)}")