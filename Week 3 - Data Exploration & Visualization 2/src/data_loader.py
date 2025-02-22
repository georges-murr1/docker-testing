import pandas as pd

def load_data(filepath):
    """
    Loads CSV data from the given filepath and parses the 'timestamp' column.

    Parameters:
        filepath (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Data loaded into a DataFrame.
    """
    try:
        df = pd.read_csv(filepath, parse_dates=['timestamp'])
        # You can add additional preprocessing here if needed.
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None
