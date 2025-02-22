import os
from elasticsearch import Elasticsearch

def get_es_client():
    host = os.environ.get("ES_HOST", "localhost")
    return Elasticsearch([f"http://{host}:9200"])

def create_index_if_not_exists(client, index_name="alerts"):
    """Create the Elasticsearch index if it does not exist."""
    if not client.indices.exists(index=index_name):
        client.indices.create(index=index_name)
        print(f"Created index: {index_name}")
    else:
        print(f"Index '{index_name}' already exists.")

def test_es_queries():
    client = get_es_client()

    # Ensure the "alerts" index exists before running queries
    create_index_if_not_exists(client, "alerts")

    query = {
        "query": {
            "match": {"alert_type": "Critical"}
        }
    }
    
    try:
        response = client.search(index="alerts", body=query)
        print("Elasticsearch Query Results:", response)
    except Exception as e:
        print("Error querying Elasticsearch:", e)
