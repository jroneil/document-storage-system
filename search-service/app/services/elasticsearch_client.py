from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

load_dotenv()

# Construct the full Elasticsearch URL
es_protocol = os.getenv("ELASTICSEARCH_PROTOCOL", "http")
es_host = os.getenv("ELASTICSEARCH_HOST", "localhost")
es_port = os.getenv("ELASTICSEARCH_PORT", "9200")
es_url = f"{es_protocol}://{es_host}:{es_port}"

es = Elasticsearch([es_url])

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
