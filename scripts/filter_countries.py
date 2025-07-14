#!/usr/bin/env python3
"""
Script to find common countries across all three datasets (population, GDP, tax revenues).
Reads the raw CSV files directly to extract unique countries from each dataset and finds the intersection.
Also filters the raw data files to keep only data for common countries.
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
    processed_dir = Path("data/processed")
    
    # Create processed directory if it doesn't exist
    processed_dir.mkdir(parents=True, exist_ok=True)
    
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
        filtered_path = processed_dir / filtered_file
        
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

def main():
    """Main function to execute the script."""
    print("Finding common countries across all three datasets...")
    print("=" * 60)
    
    # Find common countries
    common_countries = find_common_countries()
    
    if common_countries:
        # Filter raw data files to keep only common countries
        filter_raw_data_files(common_countries)
    else:
        print("No common countries found or error occurred.")

if __name__ == "__main__":
    main() 