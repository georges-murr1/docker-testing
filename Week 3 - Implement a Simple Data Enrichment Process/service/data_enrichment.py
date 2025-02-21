from kafka import KafkaConsumer, KafkaProducer
import pymysql
from pymemcache.client.base import Client as MemcacheClient
from elasticsearch import Elasticsearch
import json
import hashlib
import logging
import time

# Configurations
KAFKA_BROKER = ["kafka:9092"]  # Use a list for better failover handling
INPUT_TOPIC = "raw_alerts"
OUTPUT_TOPIC = "enriched_alerts"

MYSQL_CONFIG = {
    "host": "mysql",
    "user": "root",
    "password": "password",
    "database": "alert_db",
    "cursorclass": pymysql.cursors.DictCursor,  # Ensures MySQL returns dictionaries
}

MEMCACHE_HOST = "memcached"
MEMCACHE_PORT = 11211

ELASTICSEARCH_HOST = "http://elasticsearch:9200"
ELASTICSEARCH_INDEX = "alerts"

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# **Ensure Elasticsearch is Ready Before Continuing**
logging.info("Connecting to Elasticsearch...")
while True:
    try:
        es = Elasticsearch([ELASTICSEARCH_HOST])
        if es.ping():
            logging.info("Elasticsearch is ready!")
            break
        else:
            logging.warning("Elasticsearch not ready. Retrying...")
    except Exception as e:
        logging.warning(f"Elasticsearch connection error: {e}")
    time.sleep(5)  # Retry every 5 seconds

# **Ensure Kafka is Ready Before Starting Consumer & Producer**
logging.info("Initializing Kafka Consumer & Producer...")

while True:
    try:
        consumer = KafkaConsumer(
            INPUT_TOPIC,
            bootstrap_servers=KAFKA_BROKER,
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
            auto_offset_reset="earliest",  # Prevent missing messages
            enable_auto_commit=True,  # Ensures offsets are committed
            api_version=(0, 10),
        )
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            api_version=(0, 10),
        )
        logging.info("Kafka Consumer & Producer initialized successfully.")
        break
    except Exception as e:
        logging.warning(f"Kafka connection error: {e}. Retrying in 5s...")
    time.sleep(5)

# **MySQL Connection with Retry Logic**
def get_mysql_connection():
    retries = 5
    for attempt in range(retries):
        try:
            conn = pymysql.connect(**MYSQL_CONFIG)
            logging.info("Connected to MySQL.")
            return conn
        except Exception as e:
            logging.warning(f"MySQL connection failed: {e}. Retrying in 5s ({attempt+1}/{retries})...")
            time.sleep(5)
    logging.error("MySQL connection failed after multiple attempts.")
    return None

# **Memcache Client with Error Handling**
try:
    memcache_client = MemcacheClient((MEMCACHE_HOST, MEMCACHE_PORT))
    logging.info("Connected to Memcache.")
except Exception as e:
    logging.error(f"Failed to connect to Memcache: {e}")

# **Helper Functions**
def compute_alert_hash(alert):
    return hashlib.sha256(json.dumps(alert, sort_keys=True).encode()).hexdigest()

def compute_risk_score(alert, past_alerts):
    severity = alert.get("severity", 1)
    return min(10, severity + (len(past_alerts) // 5))

# **Retrieve past alerts from MySQL**
def fetch_past_alerts(alert):
    conn = get_mysql_connection()
    if not conn:
        logging.warning("Skipping MySQL lookup due to connection failure.")
        return []

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM alert_history WHERE source = %s ORDER BY timestamp DESC LIMIT 10",
                (alert.get("source", "unknown"),)
            )
            return cursor.fetchall()
    except Exception as e:
        logging.error(f"Error fetching past alerts: {e}")
        return []
    finally:
        conn.close()

# **Fetch cached data from Memcache**
def fetch_cached_data(alert):
    try:
        cached_data = memcache_client.get(f"alert:{alert.get('source', 'unknown')}")
        return json.loads(cached_data) if cached_data else {}
    except Exception as e:
        logging.error(f"Memcache fetch failed: {e}")
        return {}

# **Store in Elasticsearch**
def store_in_elasticsearch(alert):
    try:
        es.index(index=ELASTICSEARCH_INDEX, body=alert)
        logging.info(f"Stored alert in Elasticsearch: {alert}")
    except Exception as e:
        logging.error(f"Failed to store alert in Elasticsearch: {e}")

# **Process Kafka messages**
def process_message(alert):
    logging.info(f"🔍 Processing alert: {alert}")

    past_alerts = fetch_past_alerts(alert)
    cached_data = fetch_cached_data(alert)

    alert["hash"] = compute_alert_hash(alert)
    alert["risk_score"] = compute_risk_score(alert, past_alerts)
    alert["cached_info"] = cached_data

    store_in_elasticsearch(alert)

    try:
        producer.send(OUTPUT_TOPIC, alert)
        logging.info(f"Enriched alert sent to Kafka: {alert}")
    except Exception as e:
        logging.error(f"Failed to send message to Kafka: {e}")

# **Main Kafka Consumer Loop**
def consume_messages():
    logging.info("Starting Kafka Consumer...")
    for message in consumer:
        try:
            process_message(message.value)
        except Exception as e:
            logging.error(f"Failed to process message: {e}")

# **Run the Consumer Process**
if __name__ == "__main__":
    logging.info("🛠️ Waiting for services to be ready...")
    time.sleep(10)  # Allow services time to start
    consume_messages()
