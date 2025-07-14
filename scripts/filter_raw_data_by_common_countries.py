#!/usr/bin/env python3
"""
Script to find common countries across all 3 raw datasets and filter data accordingly.
This script:
1. Reads the unique values CSV files to get country lists from each dataset
2. Finds the intersection of countries across all 3 datasets
3. Saves the list of common countries to a JSON file
4. Filters the raw CSV data to keep only countries present in all datasets
5. Saves the filtered data to a new directory
"""

import pandas as pd
import json
import os
from pathlib import Path

def load_countries_from_unique_values(file_path):
    """Load unique countries from a unique values CSV file."""
    try:
        df = pd.read_csv(file_path)
        # Get unique countries from REF_AREA column, excluding empty values
        countries = df['REF_AREA'].dropna().unique().tolist()
        # Remove any empty strings and filter out non-country codes
        countries = [country for country in countries if country.strip() and len(country) <= 4]
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

def save_common_countries(common_countries, output_file):
    """Save the list of common countries to a JSON file."""
    try:
        # Convert set to sorted list for JSON serialization
        countries_list = sorted(list(common_countries))
        
        # Create metadata
        metadata = {
            "total_common_countries": len(common_countries),
            "countries": countries_list,
            "description": "Countries present in all 3 datasets (GDP, Labor Force, Tax Revenues)",
            "datasets": ["gdp", "labor_force", "tax_revenues"]
        }
        
        with open(output_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"Saved common countries list to {output_file}")
        return True
        
    except Exception as e:
        print(f"Error saving common countries: {e}")
        return False

def main():
    # Define paths
    raw_dir = Path("data/raw")
    filtered_dir = Path("data/filtered")
    
    # Create filtered directory if it doesn't exist
    filtered_dir.mkdir(exist_ok=True)
    
    # Files to process
    unique_files = {
        'gdp': raw_dir / "gdp_unique_values.csv",
        'labor_force': raw_dir / "labor_force_unique_values.csv", 
        'tax_revenues': raw_dir / "tax_revenues_unique_values.csv"
    }
    
    raw_csv_files = {
        'gdp': raw_dir / "gdp.csv",
        'labor_force': raw_dir / "labor_force.csv",
        'tax_revenues': raw_dir / "tax_revenues.csv"
    }
    
    print("Loading unique countries from each dataset...")
    
    # Load countries from each dataset
    countries_by_dataset = {}
    for dataset_name, file_path in unique_files.items():
        countries = load_countries_from_unique_values(file_path)
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
    
    # Save common countries list
    common_countries_file = filtered_dir / "common_countries.json"
    if save_common_countries(common_countries, common_countries_file):
        print(f"Common countries list saved to {common_countries_file}")
    
    # Confirm with user
    response = input(f"\nProceed with filtering raw data? This will remove data for {sum(len(countries - common_countries) for countries in countries_by_dataset.values())} countries total. (y/N): ")
    if response.lower() != 'y':
        print("Operation cancelled.")
        return
    
    print("\nFiltering raw datasets...")
    
    # Filter each raw dataset
    success_count = 0
    for dataset_name, input_file in raw_csv_files.items():
        if input_file.exists():
            output_file = filtered_dir / f"{dataset_name}_filtered.csv"
            if filter_dataset_by_countries(input_file, output_file, common_countries):
                success_count += 1
        else:
            print(f"Warning: {input_file} not found, skipping...")
    
    print(f"\nSuccessfully filtered {success_count} out of {len(raw_csv_files)} datasets.")
    print(f"Filtered data saved to: {filtered_dir}")
    print("Filtering complete!")
    
    # Show summary
    print(f"\nSummary:")
    print(f"Total unique countries across all datasets: {len(set.union(*countries_by_dataset.values()))}")
    print(f"Countries in common: {len(common_countries)}")
    print(f"Countries excluded: {len(set.union(*countries_by_dataset.values())) - len(common_countries)}")
    print(f"Data reduction: {((len(set.union(*countries_by_dataset.values())) - len(common_countries)) / len(set.union(*countries_by_dataset.values())) * 100):.1f}%")

if __name__ == "__main__":
    main() 