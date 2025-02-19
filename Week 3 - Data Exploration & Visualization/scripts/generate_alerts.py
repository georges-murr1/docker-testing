import os
import json
import random
import mysql.connector
from faker import Faker
from confluent_kafka import Producer
from datetime import datetime, timezone
from elasticsearch import Elasticsearch

# Initialize Faker
fake = Faker()

# Alert Types & Severity Levels
ALERT_TYPES = ["Network Intrusion", "Malware", "Unauthorized Access", "Data Breach", "DDoS Attack"]
SEVERITY_LEVELS = ["Low", "Medium", "High", "Critical"]

# Load configurations from environment variables
MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "mysql"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "example"),
    "database": os.getenv("MYSQL_DATABASE", "alert_db"),
}

KAFKA_CONFIG = {
    "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"),
    "security.protocol": "PLAINTEXT",
}

ES_CONFIG = {
    "hosts": os.getenv("ELASTICSEARCH_HOST", "http://elasticsearch:9200")
}

KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "test-topic")
ES_INDEX = os.getenv("ES_INDEX", "alert_logs")


# Generate Synthetic Alert Data
def generate_alert():
    return {
        "alert_id": fake.uuid4(),
        "alert_type": random.choice(ALERT_TYPES),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "severity": random.choice(SEVERITY_LEVELS),
        "source_ip": fake.ipv4(),
        "destination_ip": fake.ipv4(),
        "description": fake.sentence(),
    }


# Ensure 'alerts' table exists before inserting data
def ensure_table_exists():
    """Ensures the 'alerts' table exists in MySQL before inserting data."""
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS alerts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            alert_id VARCHAR(255) NOT NULL,
            alert_type VARCHAR(100) NOT NULL,
            timestamp DATETIME NOT NULL,
            severity VARCHAR(50) NOT NULL,
            source_ip VARCHAR(100) NOT NULL,
            destination_ip VARCHAR(100) NOT NULL,
            description TEXT NOT NULL
        ) ENGINE=InnoDB;
        """

        cursor.execute(create_table_query)
        conn.commit()
        cursor.close()
        conn.close()
        print("Checked: 'alerts' table exists or created successfully.")

    except mysql.connector.Error as e:
        print(f"MySQL Error while creating table: {e}")


# Insert alerts into MySQL database
def insert_into_mysql(alert):
    """Inserts a generated alert into MySQL."""
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO alerts (alert_id, alert_type, timestamp, severity, source_ip, destination_ip, description)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            alert["alert_id"], alert["alert_type"], alert["timestamp"],
            alert["severity"], alert["source_ip"], alert["destination_ip"],
            alert["description"]
        )
        cursor.execute(insert_query, values)

        conn.commit()
        cursor.close()
        conn.close()
        print(f"Inserted into MySQL: {alert}")

    except mysql.connector.Error as e:
        print(f"MySQL Error: {e}")


# Publish to Kafka
def publish_to_kafka(alert):
    """Publishes an alert to a Kafka topic."""
    try:
        producer = Producer(KAFKA_CONFIG)
        producer.produce(KAFKA_TOPIC, json.dumps(alert).encode('utf-8'))
        producer.flush()
        print(f"Published to Kafka: {alert}")

    except Exception as e:
        print(f"Kafka Error: {e}")


# Store in Elasticsearch
def store_in_elasticsearch(alert):
    """Stores an alert in Elasticsearch."""
    try:
        es = Elasticsearch(**ES_CONFIG)
        es.index(index=ES_INDEX, body=alert)
        print(f"Stored in Elasticsearch: {alert}")

    except Exception as e:
        print(f"Elasticsearch Error: {e}")


# Main Execution
def main():
    """Main function to generate alerts and process them."""
    ensure_table_exists()  # Ensure the MySQL table exists before inserting data

    for _ in range(10):  # Generate 10 alerts
        alert = generate_alert()
        insert_into_mysql(alert)
        publish_to_kafka(alert)
        store_in_elasticsearch(alert)


if __name__ == "__main__":
    main()
