"""
Product data generator module.

This module contains functions for generating synthetic product data.
"""

import pandas as pd
import random
import os
from config import APPLE_VARIETIES, SHELF_LIVES, GRADES, UNITS_OF_MEASURE, DATA_DIR, get_output_path
from data_utils import save_csv_data

def generate_apple_product_data(num_records=100):
    """Generates synthetic data for an apple product table.

    Args:
        num_records (int): The number of records to generate.

    Returns:
        pandas.DataFrame: A DataFrame containing the synthetic data.
    """
    # Validate inputs
    if not isinstance(num_records, int) or num_records <= 0:
        raise ValueError("num_records must be a positive integer")
    
    data = []
    for i in range(num_records):
        sku_id = f"APP{i:04d}"  # APP0000, APP0001, ...
        variety = random.choice(APPLE_VARIETIES)
        name = f"{variety} Apple"
        shelf_life = random.choice(SHELF_LIVES)
        grade = random.choice(GRADES)
        unit_of_measure = random.choice(UNITS_OF_MEASURE)

        data.append({
            "SKUID": sku_id,
            "Name": name,
            "ShelfLife": shelf_life,
            "Grade": grade,
            "UnitOfMeasure": unit_of_measure,
        })

    return pd.DataFrame(data)

def save_product_data(df, filename="product_master.csv"):
    """Save product data to a CSV file.
    
    Args:
        df (pandas.DataFrame): Product data to save
        filename (str): Name of the output file
        
    Returns:
        bool: True if saving was successful, False otherwise
    """
    output_path = get_output_path(filename)
    return save_csv_data(df, output_path, "Error saving product data")

if __name__ == "__main__":
    # When run as a script, generate and save product data
    apple_data = generate_apple_product_data(45)
    print(apple_data)
    
    # Save to CSV file
    save_product_data(apple_data)
