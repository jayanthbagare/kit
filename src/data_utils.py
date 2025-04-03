"""
Utility functions for data loading, processing and validation.

This module contains helper functions for loading data from CSV files,
validating data quality, and processing data for the supply chain simulation.
"""

import os
import pandas as pd
from io import StringIO
from datetime import datetime
from dateutil.relativedelta import relativedelta

def load_csv_data(file_path, error_message=None):
    """Load data from a CSV file with error handling.
    
    Args:
        file_path (str): Path to the CSV file
        error_message (str, optional): Custom error message if loading fails
        
    Returns:
        pandas.DataFrame: Loaded data or None if loading fails
    """
    try:
        if not os.path.exists(file_path):
            print(f"Warning: File {file_path} does not exist.")
            return None
            
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        if error_message:
            print(f"{error_message}: {e}")
        else:
            print(f"Error loading {file_path}: {e}")
        return None

def save_csv_data(df, file_path, error_message=None):
    """Save DataFrame to a CSV file with error handling.
    
    Args:
        df (pandas.DataFrame): DataFrame to save
        file_path (str): Path to save the CSV file
        error_message (str, optional): Custom error message if saving fails
        
    Returns:
        bool: True if saving was successful, False otherwise
    """
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        df.to_csv(file_path, index=False)
        print(f"Data successfully saved to: {os.path.abspath(file_path)}")
        return True
    except Exception as e:
        if error_message:
            print(f"{error_message}: {e}")
        else:
            print(f"Error saving data to {file_path}: {e}")
        return False

def validate_dataframe(df, required_columns, name="DataFrame"):
    """Validate that a DataFrame contains required columns and is not empty.
    
    Args:
        df (pandas.DataFrame): DataFrame to validate
        required_columns (list): List of column names that should be present
        name (str, optional): Name of the DataFrame for error messages
        
    Returns:
        bool: True if DataFrame is valid, False otherwise
    """
    if df is None:
        print(f"Error: {name} is None.")
        return False
        
    if df.empty:
        print(f"Error: {name} is empty.")
        return False
        
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Error: {name} is missing required columns: {missing_columns}")
        return False
        
    return True

def load_from_string(csv_string):
    """Load a DataFrame from a CSV string.
    
    Args:
        csv_string (str): CSV data as a string
        
    Returns:
        pandas.DataFrame: Loaded data
    """
    return pd.read_csv(StringIO(csv_string))
