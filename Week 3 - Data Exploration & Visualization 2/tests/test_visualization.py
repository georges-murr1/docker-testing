import os
import shutil
import pandas as pd
from src.visualization import plot_alert_frequency, plot_top_alerts

def create_dummy_data():
    data = {
        'timestamp': pd.date_range(start='2025-02-20', periods=5, freq='h'),
        'alert_type': ['Test', 'Test', 'Warning', 'Critical', 'Test'],
        'severity': ['Low', 'Low', 'High', 'Critical', 'Low'],
        'message': ['a', 'b', 'c', 'd', 'e']
    }
    return pd.DataFrame(data)

def test_plot_alert_frequency():
    df = create_dummy_data()
    # Remove output directory if it exists
    output_dir = "output"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    
    # Generate the plot
    plot_alert_frequency(df)
    
    # Check if the alert frequency plot was saved
    filepath = os.path.join(output_dir, "alert_frequency.png")
    assert os.path.exists(filepath), "Alert frequency plot was not created."

def test_plot_top_alerts():
    df = create_dummy_data()
    # Remove output directory if it exists
    output_dir = "output"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    
    # Generate the plot
    plot_top_alerts(df)
    
    # Check if the top alerts plot was saved
    filepath = os.path.join(output_dir, "top_alerts.png")
    assert os.path.exists(filepath), "Top alerts plot was not created."
