#!/usr/bin/env python3
"""
Script to find countries present in all 3 datasets and filter data accordingly.
This script:
1. Reads the unique values CSV files to get country lists from each dataset
2. Finds the intersection of countries across all 3 datasets
3. Filters the labeled data to keep only countries present in all datasets
4. Saves the filtered data back to the labeled directory
"""

import pandas as pd
import os
from pathlib import Path

def load_unique_countries(file_path, country_column='REF_AREA'):
    """Load unique countries from a unique values CSV file."""
    try:
        df = pd.read_csv(file_path)
        # Get unique countries, excluding empty values
        countries = df[country_column].dropna().unique().tolist()
        # Remove any empty strings
        countries = [country for country in countries if country.strip()]
        return set(countries)
    except Exception as e:
        print(f"Error loading countries from {file_path}: {e}")
        return set()

def filter_dataset_by_countries(input_file, output_file, common_countries, country_column='REF_AREA'):
    """Filter a dataset to keep only rows for countries in the common_countries set."""
    try:
        print(f"Filtering {input_file}...")
        df = pd.read_csv(input_file)
        
        # Get initial count
        initial_count = len(df)
        
        # Filter by countries
        df_filtered = df[df[country_column].isin(common_countries)]
        
        # Get final count
        final_count = len(df_filtered)
        
        # Save filtered data
        df_filtered.to_csv(output_file, index=False)
        
        print(f"  Kept {final_count} rows out of {initial_count} (removed {initial_count - final_count})")
        return True
        
    except Exception as e:
        print(f"Error filtering {input_file}: {e}")
        return False

def main():
    # Define paths
    processed_dir = Path("data/processed")
    labeled_dir = Path("data/labeled")
    
    # Files to process
    unique_files = {
        'gdp': processed_dir / "gdp_unique_values.csv",
        'labor_force': processed_dir / "labor_force_unique_values.csv", 
        'tax_revenues': processed_dir / "tax_revenues_unique_values.csv"
    }
    
    labeled_files = {
        'gdp': labeled_dir / "gdp_labeled.csv",
        'labor_force': labeled_dir / "labor_force_labeled.csv",
        'tax_revenues': labeled_dir / "tax_revenues_labeled.csv"
    }
    
    print("Loading unique countries from each dataset...")
    
    # Load countries from each dataset
    countries_by_dataset = {}
    for dataset_name, file_path in unique_files.items():
        countries = load_unique_countries(file_path)
        countries_by_dataset[dataset_name] = countries
        print(f"{dataset_name}: {len(countries)} unique countries")
    
    # Find intersection of all countries
    common_countries = set.intersection(*countries_by_dataset.values())
    
    print(f"\nCountries present in ALL 3 datasets: {len(common_countries)}")
    print("Common countries:")
    for country in sorted(common_countries):
        print(f"  - {country}")
    
    # Show countries that will be removed from each dataset
    print("\nCountries that will be removed from each dataset:")
    for dataset_name, countries in countries_by_dataset.items():
        removed_countries = countries - common_countries
        if removed_countries:
            print(f"\n{dataset_name} (removing {len(removed_countries)} countries):")
            for country in sorted(removed_countries):
                print(f"  - {country}")
        else:
            print(f"\n{dataset_name}: No countries to remove")
    
    # Confirm with user
    response = input(f"\nProceed with filtering? This will remove data for {sum(len(countries - common_countries) for countries in countries_by_dataset.values())} countries total. (y/N): ")
    if response.lower() != 'y':
        print("Operation cancelled.")
        return
    
    print("\nFiltering labeled datasets...")
    
    # Filter each labeled dataset
    success_count = 0
    for dataset_name, input_file in labeled_files.items():
        if input_file.exists():
            output_file = input_file  # Overwrite the original file
            if filter_dataset_by_countries(input_file, output_file, common_countries):
                success_count += 1
        else:
            print(f"Warning: {input_file} not found, skipping...")
    
    print(f"\nSuccessfully filtered {success_count} out of {len(labeled_files)} datasets.")
    print("Filtering complete!")

if __name__ == "__main__":
    main() 