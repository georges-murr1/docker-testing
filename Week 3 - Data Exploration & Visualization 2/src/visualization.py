import os
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib

def plot_alert_frequency(data):
    """
    Plots the frequency of alerts over time.
    """
    plt.figure(figsize=(10, 6))
    # Use lowercase 'h' for hourly frequency
    frequency = data.set_index('timestamp').resample('h').size()
    frequency.plot(kind='line', marker='o')
    plt.title('Alert Frequency Over Time')
    plt.xlabel('Time')
    plt.ylabel('Number of Alerts')
    plt.tight_layout()
    
    # Ensure the output directory exists
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save the plot
    plt.savefig(os.path.join(output_dir, "alert_frequency.png"))
    
    # Only display the plot if using an interactive backend
    if matplotlib.get_backend().lower() != 'agg':
        plt.show()
    plt.close()

def plot_top_alerts(data):
    """
    Plots the top alert types based on their frequency.
    """
    plt.figure(figsize=(10, 6))
    # Count occurrences of each alert type
    alert_counts = data['alert_type'].value_counts().reset_index()
    alert_counts.columns = ['alert_type', 'count']
    
    # Assign alert_type to hue to satisfy seaborn's requirements
    ax = sns.barplot(x='alert_type', y='count', data=alert_counts, hue='alert_type', palette='viridis', dodge=False)
    legend = ax.get_legend()
    if legend is not None:
        legend.remove()  # Remove redundant legend if it exists
    
    plt.title('Top Alert Types')
    plt.xlabel('Alert Type')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Ensure the output directory exists
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save the plot
    plt.savefig(os.path.join(output_dir, "top_alerts.png"))
    
    # Only display the plot if using an interactive backend
    if matplotlib.get_backend().lower() != 'agg':
        plt.show()
    plt.close()
