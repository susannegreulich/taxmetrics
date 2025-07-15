#!/usr/bin/env python3
"""
Script to find common countries across all three datasets (population, GDP, tax revenues).
Reads the raw CSV files directly to extract unique countries from each dataset and finds the intersection.
Then filters the raw data files to keep only data for common countries.
Also removes columns/variables with only one unique value and saves the single unique values to a CSV file. As these single
unique values were not values of interest, but merely the configurations for the data chosen. 
Finally, converts the filtered data to 2D format with years as rows and countries as columns.
"""

import pandas as pd
import os
from pathlib import Path

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
    
    Args:
        common_countries (list): List of country codes to keep
    """
    raw_dir = Path("data/raw")
    filtered_dir = Path("data/filtered")
    data_dir = Path("data")
    
    # Create data directory if it doesn't exist
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Define the raw data files to process (to get original column structure)
    raw_files = [
        ("population_raw.csv", "population_filtered.csv", "Population"),
        ("gdp_raw.csv", "gdp_filtered.csv", "GDP"),
        ("tax_revenues_raw.csv", "tax_revenues_filtered.csv", "Tax Revenues")
    ]
    
    dataset_configs = {}
    
    print("\nRemoving columns with single unique values...")
    print("=" * 50)
    
    for raw_file, filtered_file, dataset_name in raw_files:
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
                    single_value_columns[column] = str(value)
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
    Save the dataset configurations to a CSV file.
    
    Args:
        dataset_configs (dict): Dictionary containing configs for each dataset
    """
    data_dir = Path("data")
    config_file = data_dir / "dataset_configs.csv"
    
    print(f"\nSaving dataset configurations to: {config_file}")
    
    # Prepare data for CSV
    csv_data = []
    for dataset_name, config in dataset_configs.items():
        if config['single_value_columns']:
            for column, value in config['single_value_columns'].items():
                csv_data.append({
                    'Dataset': dataset_name,
                    'Deleted_Column': column,
                    'Single_Unique_Value': value
                })
        else:
            # Add a row to indicate no columns were deleted for this dataset
            csv_data.append({
                'Dataset': dataset_name,
                'Deleted_Column': 'None',
                'Single_Unique_Value': 'No columns deleted'
            })
    
    # Create DataFrame and save to CSV
    if csv_data:
        df_config = pd.DataFrame(csv_data)
        df_config.to_csv(config_file, index=False)
        print(f"Dataset configurations saved to: {config_file}")
        print(f"Total rows: {len(df_config)}")
    else:
        print("No configuration data to save.")

def convert_to_2d_format():
    """
    Convert filtered data from long format to 2D format with years as rows and countries as columns.
    Creates new 2D versions of the filtered CSV files.
    For tax revenues, creates a format with TIME_PERIOD, STANDARD_REVENUE, and all REF_AREAs as columns.
    """
    filtered_dir = Path("data/filtered")
    
    # Define the filtered data files to convert (save with original names)
    filtered_files = [
        ("population_filtered.csv", "population_filtered.csv"),
        ("gdp_filtered.csv", "gdp_filtered.csv"),
        ("tax_revenues_filtered.csv", "tax_revenues_filtered.csv")
    ]
    
    print("\nConverting filtered data to 2D format...")
    print("=" * 50)
    
    for filtered_file, output_file in filtered_files:
        filtered_path = filtered_dir / filtered_file
        output_path = filtered_dir / output_file
        
        if not filtered_path.exists():
            print(f"Warning: Filtered file not found: {filtered_path}")
            continue
        
        try:
            print(f"Processing {filtered_file}...")
            
            # Read the filtered data
            df = pd.read_csv(filtered_path)
            
            # Check if we have the expected columns
            if 'TIME_PERIOD' not in df.columns or 'REF_AREA' not in df.columns or 'value' not in df.columns:
                print(f"  Warning: Expected columns not found in {filtered_file}")
                print(f"  Available columns: {list(df.columns)}")
                continue
            
            # For tax revenues, create special format with TIME_PERIOD, STANDARD_REVENUE, and REF_AREAs as columns
            if 'STANDARD_REVENUE' in df.columns:
                # Pivot to get TIME_PERIOD and STANDARD_REVENUE as index, REF_AREA as columns
                df_pivot = df.pivot_table(
                    index=['TIME_PERIOD', 'STANDARD_REVENUE'],
                    columns='REF_AREA',
                    values='value',
                    aggfunc='first'  # Take the first value if there are duplicates
                )
                
                # Reset index to make TIME_PERIOD and STANDARD_REVENUE regular columns
                df_pivot = df_pivot.reset_index()
                
                # Sort by TIME_PERIOD and STANDARD_REVENUE
                df_pivot = df_pivot.sort_values(['TIME_PERIOD', 'STANDARD_REVENUE'])
                
                print(f"  Tax revenues format: TIME_PERIOD, STANDARD_REVENUE, {len([col for col in df_pivot.columns if col not in ['TIME_PERIOD', 'STANDARD_REVENUE']])} countries")
            else:
                # For population and GDP data, simple pivot
                df_pivot = df.pivot_table(
                    index='TIME_PERIOD',
                    columns='REF_AREA',
                    values='value',
                    aggfunc='first'  # Take the first value if there are duplicates
                )
                
                # Reset index to make TIME_PERIOD a regular column
                df_pivot = df_pivot.reset_index()
                
                # Sort by TIME_PERIOD
                df_pivot = df_pivot.sort_values('TIME_PERIOD')
            
            # Save the 2D data (overwriting the original file)
            df_pivot.to_csv(output_path, index=False)
            
            print(f"  Original shape: {df.shape}")
            print(f"  2D shape: {df_pivot.shape}")
            print(f"  Years: {df_pivot['TIME_PERIOD'].min()} to {df_pivot['TIME_PERIOD'].max()}")
            if 'STANDARD_REVENUE' in df_pivot.columns:
                print(f"  Revenue types: {df_pivot['STANDARD_REVENUE'].nunique()}")
            print(f"  Countries: {len([col for col in df_pivot.columns if col not in ['TIME_PERIOD', 'STANDARD_REVENUE']])}")
            print(f"  Saved to: {output_path}")
            
        except Exception as e:
            print(f"Error processing {filtered_file}: {e}")

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
        
        # Convert filtered data to 2D format
        convert_to_2d_format()
    else:
        print("No common countries found or error occurred.")

if __name__ == "__main__":
    main() 