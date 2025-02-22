import os
from data_loader import load_data
from visualization import plot_alert_frequency, plot_top_alerts
from elasticsearch_queries import test_es_queries

def main():
    # Load data from the CSV file
    data = load_data("data/synthetic_alerts.csv")
    
    if data is None:
        print("Data loading failed. Please check the CSV file.")
        return
    
    # Generate and display/save the graphs
    plot_alert_frequency(data)
    plot_top_alerts(data)
    
    # Run Elasticsearch query only if the environment variable RUN_ELASTICSEARCH is set to "true"
    if os.environ.get("RUN_ELASTICSEARCH", "false").lower() == "true":
        test_es_queries()
    else:
        print("Skipping Elasticsearch queries. To run them, set RUN_ELASTICSEARCH=true in your environment.")

if __name__ == "__main__":
    main()
