import os
from elasticsearch import Elasticsearch

def get_es_client():
    host = os.environ.get("ES_HOST", "localhost")
    return Elasticsearch([f"http://{host}:9200"])

def create_index(client, index_name="alerts"):
    """Create the Elasticsearch index if it does not exist."""
    if not client.indices.exists(index=index_name):
        client.indices.create(index=index_name, body={
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": {
                "properties": {
                    "timestamp": {"type": "date"},
                    "alert_type": {"type": "keyword"},
                    "severity": {"type": "keyword"},
                    "message": {"type": "text"}
                }
            }
        })
        print(f"Created index: {index_name}")
    else:
        print(f"Index '{index_name}' already exists.")

def insert_dummy_data(client, index_name="alerts"):
    """Insert dummy alert data to ensure the index is not empty."""
    sample_data = [
        {"timestamp": "2025-02-20T10:15:00", "alert_type": "Critical", "severity": "High", "message": "Unauthorized access detected"},
        {"timestamp": "2025-02-20T10:20:00", "alert_type": "Warning", "severity": "Medium", "message": "Suspicious login attempt"},
        {"timestamp": "2025-02-20T10:30:00", "alert_type": "Info", "severity": "Low", "message": "System scan completed"}
    ]
    
    for doc in sample_data:
        client.index(index=index_name, body=doc)

    print("Inserted dummy alert data.")

def test_es_queries():
    client = get_es_client()

    # Ensure the "alerts" index exists
    create_index(client, "alerts")

    # Insert sample data (only if necessary)
    insert_dummy_data(client, "alerts")

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
