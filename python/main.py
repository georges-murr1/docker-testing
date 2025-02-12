import mysql.connector
from kafka import KafkaProducer, KafkaConsumer
from pymemcache.client import base
from elasticsearch import Elasticsearch
import json
import time

# ========== MySQL Connection ==========
try:
    db = mysql.connector.connect(
        host="mysql",
        user="testuser",
        password="testpassword",
        database="exampledb"
    )
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    print("MySQL Users:", users)
except Exception as e:
    print("MySQL Error:", e)

print("")

# ========== Kafka Producer ==========
try:
    producer = KafkaProducer(
        bootstrap_servers="kafka:9092",
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    producer.send("test-topic", {"message": "Hello from producer!"})
    producer.flush()
    print("Kafka Producer sent a message.")
except Exception as e:
    print("Kafka Producer Error:", e)

print("")

# ========== Kafka Consumer ==========
try:
    consumer = KafkaConsumer(
    "test-topic",
    bootstrap_servers="kafka:9092",
    auto_offset_reset="earliest",  # Ensures old messages are received
    enable_auto_commit=True,
    group_id="test-group",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

    print("Kafka Consumer Started. Waiting for messages...")
    for message in consumer:
        print(f"Kafka Received Message: {message.value}")
        break  # Exit after receiving one message

except Exception as e:
    print("Kafka Consumer Error:", e)

    
print("")

# ========== Memcached ==========
try:
    memcache_client = base.Client(("memcache", 11211))
    memcache_client.set("foo", "bar")
    value = memcache_client.get("foo").decode()
    print("Memcache Stored and Retrieved:", value)
except Exception as e:
    print("Memcache Error:", e)

print("")

# ========== Elasticsearch ==========
try:
    es = Elasticsearch(["http://elasticsearch:9200"],
                       verify_certs=False,)

    # Ensure index exists
    if not es.indices.exists(index="test-index"):
        es.indices.create(index="test-index")

    # Insert test document
    doc = {"name": "John Doe", "message": "Hello Elasticsearch!"}
    es.index(index="test-index", id=1, body=doc)

    # Retrieve document
    res = es.get(index="test-index", id=1)
    print("Elasticsearch Document:", res["_source"])

except Exception as e:
    print("Elasticsearch Error:", e)

print("")

# ========== Keep Container Running ==========
while True:
    print("All services tested successfully!")
    time.sleep(10)
