#!/usr/bin/env python3
"""
Script to extract unique values for each variable in OECD datasets and output as CSV files.
Each column represents a dimension/variable, and each row contains one unique value from that dimension.
"""

import pandas as pd
import os
from pathlib import Path
from typing import Dict, List, Any

def create_unique_values_csv(file_path: str, output_file: str):
    """
    Create a CSV file with unique values for each variable, with each column representing a dimension.
    
    Args:
        file_path: Path to the input CSV file
        output_file: Output CSV file path
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Get all columns except the value column
        dimension_columns = [col for col in df.columns if col.upper() != 'VALUE']
        
        # Create a dictionary to store unique values for each dimension
        unique_values_dict = {}
        
        for column in dimension_columns:
            unique_values = sorted(df[column].unique().tolist())
            unique_values_dict[column] = unique_values
        
        # Find the maximum number of unique values across all dimensions
        max_unique_count = max(len(values) for values in unique_values_dict.values())
        
        # Create a dataframe where each column is a dimension and rows contain unique values
        # Pad shorter columns with empty strings
        csv_data = {}
        for column, values in unique_values_dict.items():
            # Pad the list to match the maximum length
            padded_values = values + [''] * (max_unique_count - len(values))
            csv_data[column] = padded_values
        
        unique_df = pd.DataFrame(csv_data)
        
        # Save to CSV
        unique_df.to_csv(output_file, index=False)
        
        print(f"Unique values CSV saved to: {output_file}")
        print(f"  - {max_unique_count:,} rows (maximum unique values across all dimensions)")
        print(f"  - Columns: {', '.join(dimension_columns)}")
        
        # Print summary of unique values per dimension
        for column, values in unique_values_dict.items():
            print(f"  - {column}: {len(values):,} unique values")
            
    except Exception as e:
        print(f"ERROR processing {file_path}: {str(e)}")

def main():
    """Main function to process all datasets."""
    # Define data directory and files
    data_dir = Path("data/raw")
    
    # List of datasets to process
    datasets = [
        ("tax_revenues.csv", "Tax Revenues"),
        ("gdp.csv", "GDP"), 
        ("labor_force.csv", "Labor Force")
    ]
    
    print("OECD Dataset Unique Values Extraction")
    print("=" * 50)
    print("This script extracts unique values for each variable in the raw OECD datasets")
    print("and outputs them as CSV files with each column representing a dimension.")
    print()
    
    # Create output directory
    os.makedirs("data/raw", exist_ok=True)
    
    for filename, dataset_name in datasets:
        file_path = data_dir / filename
        
        if not file_path.exists():
            print(f"WARNING: File {file_path} not found, skipping...")
            continue
        
        print(f"Processing {dataset_name}...")
        
        # Create output filename
        base_name = filename.replace('.csv', '')
        output_csv = f"data/raw/{base_name}_unique_values.csv"
        
        create_unique_values_csv(str(file_path), output_csv)
        print()
    
    print("All CSV files created in: data/raw/")

if __name__ == "__main__":
    main() 