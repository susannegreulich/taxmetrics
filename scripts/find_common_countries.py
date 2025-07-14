#!/usr/bin/env python3
"""
Script to find common countries across all three datasets (population, GDP, tax revenues).
Uses the unique values CSV files to extract unique countries from each dataset and finds the intersection.
"""

import pandas as pd
import os
from pathlib import Path

def find_common_countries():
    """
    Find countries that appear in all three datasets (population, GDP, tax revenues).
    Uses the unique values CSV files instead of re-reading the original raw data.
    
    Returns:
        list: List of common country codes
    """
    # Define file paths for unique values files
    data_dir = Path("data/raw")
    population_unique_file = data_dir / "population_unique_values.csv"
    gdp_unique_file = data_dir / "gdp_unique_values.csv"
    tax_revenues_unique_file = data_dir / "tax_revenues_unique_values.csv"
    
    # Check if files exist
    for file_path in [population_unique_file, gdp_unique_file, tax_revenues_unique_file]:
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
    
    print("Reading unique values files...")
    
    # Read unique values files and extract unique countries
    try:
        # Population dataset unique values
        print("Reading population unique values...")
        population_df = pd.read_csv(population_unique_file)
        population_countries = set(population_df['REF_AREA'].dropna().unique())
        print(f"Found {len(population_countries)} unique countries in population dataset")
        
        # GDP dataset unique values
        print("Reading GDP unique values...")
        gdp_df = pd.read_csv(gdp_unique_file)
        gdp_countries = set(gdp_df['REF_AREA'].dropna().unique())
        print(f"Found {len(gdp_countries)} unique countries in GDP dataset")
        
        # Tax revenues dataset unique values
        print("Reading tax revenues unique values...")
        tax_revenues_df = pd.read_csv(tax_revenues_unique_file)
        tax_revenues_countries = set(tax_revenues_df['REF_AREA'].dropna().unique())
        print(f"Found {len(tax_revenues_countries)} unique countries in tax revenues dataset")
        
    except Exception as e:
        print(f"Error reading unique values files: {e}")
        return []
    
    # Find common countries (intersection of all three sets)
    common_countries = population_countries.intersection(gdp_countries).intersection(tax_revenues_countries)
    
    # Convert to sorted list
    common_countries_list = sorted(list(common_countries))
    
    print(f"\nResults:")
    print(f"Total common countries: {len(common_countries_list)}")
    print(f"Common countries: {common_countries_list}")
    
    return common_countries_list

def save_common_countries_to_file(countries_list, output_file="data/processed/common_countries.txt"):
    """
    Save the list of common countries to a text file.
    
    Args:
        countries_list (list): List of country codes
        output_file (str): Path to output file
    """
    # Create output directory if it doesn't exist
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save to file
    with open(output_path, 'w') as f:
        for country in countries_list:
            f.write(f"{country}\n")
    
    print(f"\nCommon countries saved to: {output_path}")

def main():
    """Main function to execute the script."""
    print("Finding common countries across all three datasets...")
    print("=" * 60)
    
    # Find common countries
    common_countries = find_common_countries()
    
    if common_countries:
        # Save to file
        save_common_countries_to_file(common_countries)
        
        # Also save as Python list for easy import
        python_list_file = "data/processed/common_countries.py"
        python_list_path = Path(python_list_file)
        python_list_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(python_list_path, 'w') as f:
            f.write("# Common countries across population, GDP, and tax revenues datasets\n")
            f.write("COMMON_COUNTRIES = [\n")
            for country in common_countries:
                f.write(f"    '{country}',\n")
            f.write("]\n")
        
        print(f"Common countries also saved as Python list to: {python_list_path}")
        
    else:
        print("No common countries found or error occurred.")

if __name__ == "__main__":
    main() 