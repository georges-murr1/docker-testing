import pandas as pd
import pytest
from src.data_loader import load_data

def test_load_data_file_exists(tmp_path):
    # Create a temporary CSV file with sample data
    data = "timestamp,alert_type,severity,message\n2025-02-20 10:15:00,Test,Low,Test message"
    file_path = tmp_path / "test.csv"
    file_path.write_text(data)
    
    df = load_data(str(file_path))
    assert df is not None, "Data should be loaded"
    assert not df.empty, "DataFrame should not be empty"
    # Ensure the 'timestamp' column is parsed as datetime
    assert pd.api.types.is_datetime64_any_dtype(df['timestamp']), "Timestamp should be in datetime format"

def test_load_data_invalid_file(tmp_path):
    # Provide a path that does not exist, expecting load_data to return None
    invalid_path = tmp_path / "non_existent.csv"
    df = load_data(str(invalid_path))
    assert df is None, "Should return None for invalid file path"
