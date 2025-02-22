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
    
    # Generate graphs
    plot_alert_frequency(data)
    plot_top_alerts(data)

    # test_es_queries()
    
    # Ask the user if they want to run Elasticsearch queries
    run_es = input("Do you want to run Elasticsearch queries? (Y/n): ").strip().lower()
    if run_es == 'y' or run_es == '':
        test_es_queries()
    else:
        print("Skipping Elasticsearch queries.")

if __name__ == "__main__":
    main()
