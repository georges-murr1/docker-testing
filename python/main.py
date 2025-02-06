import mysql.connector
from kafka import KafkaProducer, KafkaConsumer
import memcache
from elasticsearch import Elasticsearch
import json
import time

# Connect to MySQL
def fetch_mysql_data():
    conn = mysql.connector.connect(host='mysql', user='user', password='password', database='testdb')
    cursor = conn.cursor()
    cursor.execute("SELECT 'Hello from MySQL' AS message")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0]

# Connect to Kafka
def kafka_test():
    producer = KafkaProducer(bootstrap_servers='kafka:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    producer.send('test_topic', {'message': 'Hello Kafka'})
    producer.flush()
    
    consumer = KafkaConsumer('test_topic', bootstrap_servers='kafka:9092', auto_offset_reset='earliest', value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    time.sleep(2)  # Allow Kafka to process the message
    for msg in consumer:
        return msg.value['message']

# Connect to Memcache
def memcache_test():
    mc = memcache.Client(['memcache:11211'], debug=True)
    mc.set('test_key', 'Hello Memcache')
    return mc.get('test_key')

# Connect to Elasticsearch
def elasticsearch_test():
    es = Elasticsearch(['http://elasticsearch:9200'])
    es.index(index='test_index', document={'message': 'Hello Elasticsearch'})
    es.indices.refresh(index='test_index')
    res = es.get(index='test_index', id=1)
    return res['_source']['message']

if __name__ == "__main__":
    print("MySQL:", fetch_mysql_data())
    print("Kafka:", kafka_test())
    print("Memcache:", memcache_test())
    print("Elasticsearch:", elasticsearch_test())
