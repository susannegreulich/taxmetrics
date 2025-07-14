#!/usr/bin/env python3
"""
Script to find common countries across all three datasets (population, GDP, tax revenues).
Reads the raw CSV files directly to extract unique countries from each dataset and finds the intersection.
Also filters the raw data files to keep only data for common countries.
Removes columns with only one unique value and saves the single unique values to a markdown file. As these single
unique values were not values of interest, but merely the configurations for the data chosen. 
The unique values are replaced with their labels using the mapping files before saving to the markdown report.
"""

import pandas as pd
import os
import json
from pathlib import Path

def load_mappings(dataset_name):
    """
    Load the mapping file for a given dataset.
    
    Args:
        dataset_name (str): Name of the dataset (population, gdp, or tax_revenues)
    
    Returns:
        dict: Dictionary containing the mappings for the dataset
    """
    mapping_file = Path(f"data/labeled/{dataset_name}_mappings.json")
    
    if not mapping_file.exists():
        print(f"Warning: Mapping file not found: {mapping_file}")
        return {}
    
    try:
        with open(mapping_file, 'r', encoding='utf-8') as f:
            mappings = json.load(f)
        return mappings
    except Exception as e:
        print(f"Error loading mapping file {mapping_file}: {e}")
        return {}

def get_label_for_value(column_name, value, mappings):
    """
    Get the label for a given value in a specific column using the mappings.
    
    Args:
        column_name (str): Name of the column
        value: The value to look up
        mappings (dict): Dictionary containing the mappings
    
    Returns:
        str: The label for the value, or the original value if no mapping found
    """
    if column_name in mappings and str(value) in mappings[column_name]:
        return mappings[column_name][str(value)]
    return str(value)

def find_common_countries():
    """
    Find countries that appear in all three datasets (population, GDP, tax revenues).
    Reads the raw CSV files directly to extract unique countries.
    
    Returns:
        list: List of common country codes
    """
    # Define file paths for raw data files
    data_dir = Path("data/raw")
    population_file = data_dir / "population_raw.csv"
    gdp_file = data_dir / "gdp_raw.csv"
    tax_revenues_file = data_dir / "tax_revenues_raw.csv"
    
    # Check if files exist
    for file_path in [population_file, gdp_file, tax_revenues_file]:
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
    
    print("Reading raw data files to find unique countries...")
    
    # Read raw data files and extract unique countries
    try:
        # Population dataset
        print("Reading population data...")
        population_df = pd.read_csv(population_file)
        population_countries = set(population_df['REF_AREA'].dropna().unique())
        print(f"Found {len(population_countries)} unique countries in population dataset")
        
        # GDP dataset
        print("Reading GDP data...")
        gdp_df = pd.read_csv(gdp_file)
        gdp_countries = set(gdp_df['REF_AREA'].dropna().unique())
        print(f"Found {len(gdp_countries)} unique countries in GDP dataset")
        
        # Tax revenues dataset
        print("Reading tax revenues data...")
        tax_revenues_df = pd.read_csv(tax_revenues_file)
        tax_revenues_countries = set(tax_revenues_df['REF_AREA'].dropna().unique())
        print(f"Found {len(tax_revenues_countries)} unique countries in tax revenues dataset")
        
    except Exception as e:
        print(f"Error reading raw data files: {e}")
        return []
    
    # Find common countries (intersection of all three sets)
    common_countries = population_countries.intersection(gdp_countries).intersection(tax_revenues_countries)
    
    # Convert to sorted list
    common_countries_list = sorted(list(common_countries))
    
    print(f"\nResults:")
    print(f"Total common countries: {len(common_countries_list)}")
    print(f"Common countries: {common_countries_list}")
    
    return common_countries_list

def filter_raw_data_files(common_countries):
    """
    Filter raw data files to keep only data for countries in the common countries list.
    Creates filtered versions of the original CSV files.
    
    Args:
        common_countries (list): List of country codes to keep
    """
    data_dir = Path("data/raw")
    filtered_dir = Path("data/filtered")
    
    # Create filtered directory if it doesn't exist
    filtered_dir.mkdir(parents=True, exist_ok=True)
    
    # Define the raw data files to filter
    raw_files = [
        ("population_raw.csv", "population_filtered.csv"),
        ("gdp_raw.csv", "gdp_filtered.csv"),
        ("tax_revenues_raw.csv", "tax_revenues_filtered.csv")
    ]
    
    print("\nFiltering raw data files...")
    print("=" * 40)
    
    for raw_file, filtered_file in raw_files:
        raw_path = data_dir / raw_file
        filtered_path = filtered_dir / filtered_file
        
        if not raw_path.exists():
            print(f"Warning: Raw file not found: {raw_path}")
            continue
        
        try:
            print(f"Processing {raw_file}...")
            
            # Read the raw data
            df = pd.read_csv(raw_path)
            original_count = len(df)
            
            # Filter to keep only common countries
            df_filtered = df[df['REF_AREA'].isin(common_countries)]
            filtered_count = len(df_filtered)
            
            # Save filtered data
            df_filtered.to_csv(filtered_path, index=False)
            
            removed_count = original_count - filtered_count
            print(f"  Original records: {original_count}")
            print(f"  Filtered records: {filtered_count}")
            print(f"  Removed records: {removed_count}")
            print(f"  Saved to: {filtered_path}")
            
        except Exception as e:
            print(f"Error processing {raw_file}: {e}")

def remove_single_value_columns(common_countries):
    """
    Remove columns that have only one unique value across all datasets.
    Save the single unique values to a markdown file for reference.
    Replace identifiers with their labels using the mapping files.
    
    Args:
        common_countries (list): List of country codes to keep
    """
    raw_dir = Path("data/raw")
    filtered_dir = Path("data/filtered")
    summary_dir = Path("data/summary")
    
    # Create summary directory if it doesn't exist
    summary_dir.mkdir(parents=True, exist_ok=True)
    
    # Define the raw data files to process (to get original column structure)
    raw_files = [
        ("population_raw.csv", "population_filtered.csv", "Population", "population"),
        ("gdp_raw.csv", "gdp_filtered.csv", "GDP", "gdp"),
        ("tax_revenues_raw.csv", "tax_revenues_filtered.csv", "Tax Revenues", "tax_revenues")
    ]
    
    dataset_configs = {}
    
    print("\nRemoving columns with single unique values...")
    print("=" * 50)
    
    for raw_file, filtered_file, dataset_name, mapping_key in raw_files:
        raw_path = raw_dir / raw_file
        filtered_path = filtered_dir / filtered_file
        
        if not raw_path.exists():
            print(f"Warning: Raw file not found: {raw_path}")
            continue
        
        if not filtered_path.exists():
            print(f"Warning: Filtered file not found: {filtered_path}")
            continue
        
        try:
            print(f"Processing {raw_file}...")
            
            # Load mappings for this dataset
            mappings = load_mappings(mapping_key)
            
            # Read the raw data to determine which columns have single values
            df_raw = pd.read_csv(raw_path)
            original_columns = list(df_raw.columns)
            original_count = len(df_raw.columns)
            
            # Find columns with only one unique value in the raw data
            single_value_columns = {}
            columns_to_keep = []
            
            for column in df_raw.columns:
                unique_values = df_raw[column].dropna().unique()
                if len(unique_values) == 1:
                    value = unique_values[0]
                    # Get the label for this value using mappings
                    label = get_label_for_value(column, value, mappings)
                    single_value_columns[column] = label
                else:
                    columns_to_keep.append(column)
            
            # Read the filtered data and remove single value columns
            df_filtered = pd.read_csv(filtered_path)
            df_cleaned = df_filtered[columns_to_keep]
            
            # Save cleaned data (overwrite the filtered file)
            df_cleaned.to_csv(filtered_path, index=False)
            
            # Store config for this dataset
            dataset_configs[dataset_name] = {
                'single_value_columns': single_value_columns,
                'columns_kept': columns_to_keep,
                'original_columns': original_columns
            }
            
            removed_count = original_count - len(columns_to_keep)
            print(f"  Original columns: {original_count}")
            print(f"  Columns kept: {len(columns_to_keep)}")
            print(f"  Columns removed: {removed_count}")
            print(f"  Single value columns: {list(single_value_columns.keys())}")
            
        except Exception as e:
            print(f"Error processing {raw_file}: {e}")
    
    # Save dataset configs to markdown file
    save_dataset_configs(dataset_configs)

def save_dataset_configs(dataset_configs):
    """
    Save the dataset configurations to a markdown file.
    
    Args:
        dataset_configs (dict): Dictionary containing configs for each dataset
    """
    summary_dir = Path("data/summary")
    config_file = summary_dir / "dataset_configs.md"
    
    print(f"\nSaving dataset configurations to: {config_file}")
    
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write("# Dataset Configurations\n\n")
        f.write("This file contains information about columns that were removed from each dataset because they had only one unique value.\n")
        f.write("**Note:** The unique values shown below are the human-readable labels (not the original identifiers).\n\n")
        
        for dataset_name, config in dataset_configs.items():
            f.write(f"## {dataset_name} Dataset\n\n")
            
            # Single value columns
            if config['single_value_columns']:
                f.write("### Removed Columns (Single Unique Value)\n\n")
                
                # Find the maximum length of column names and values for consistent formatting
                max_column_length = max(len(str(col)) for col in config['single_value_columns'].keys())
                max_value_length = max(len(str(val)) for val in config['single_value_columns'].values())
                
                # Ensure minimum widths for readability
                max_column_length = max(max_column_length, 6)  # "Column" is 6 chars
                max_value_length = max(max_value_length, 15)   # "Unique Value" is 15 chars
                
                # Create header
                header = f"| {'Column':<{max_column_length}} | {'Unique Value (Label)':<{max_value_length}} |"
                f.write(header + "\n")
                
                # Create separator
                separator = f"|{'-' * (max_column_length + 2)}|{'-' * (max_value_length + 2)}|"
                f.write(separator + "\n")
                
                # Create data rows
                for column, value in config['single_value_columns'].items():
                    row = f"| {str(column):<{max_column_length}} | {str(value):<{max_value_length}} |"
                    f.write(row + "\n")
                f.write("\n")
            else:
                f.write("**No columns were removed (all columns had multiple unique values).**\n\n")
            
            # Columns kept
            f.write("### Columns Kept\n\n")
            f.write(f"Total columns kept: {len(config['columns_kept'])}\n\n")
            f.write("```\n")
            for column in config['columns_kept']:
                f.write(f"{column}\n")
            f.write("```\n\n")
            
            # Summary
            f.write("### Summary\n\n")
            f.write(f"- Original columns: {len(config['original_columns'])}\n")
            f.write(f"- Columns kept: {len(config['columns_kept'])}\n")
            f.write(f"- Columns removed: {len(config['single_value_columns'])}\n\n")
            
            f.write("---\n\n")
    
    print(f"Dataset configurations saved to: {config_file}")

def main():
    """Main function to execute the script."""
    print("Finding common countries across all three datasets...")
    print("=" * 60)
    
    # Find common countries
    common_countries = find_common_countries()
    
    if common_countries:
        # Filter raw data files to keep only common countries
        filter_raw_data_files(common_countries)
        
        # Remove columns with single unique values
        remove_single_value_columns(common_countries)
    else:
        print("No common countries found or error occurred.")

if __name__ == "__main__":
    main() 