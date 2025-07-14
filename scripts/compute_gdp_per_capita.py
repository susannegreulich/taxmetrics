#!/usr/bin/env python3
"""
Script to compute GDP per capita by dividing GDP by population from labeled datasets.
"""

import pandas as pd
import os
from pathlib import Path

def compute_gdp_per_capita():
    """
    Compute GDP per capita by dividing GDP by population for matching time periods and countries.
    """
    # Define file paths
    data_dir = Path("data/labeled")
    gdp_file = data_dir / "gdp_labeled.csv"
    population_file = data_dir / "population_labeled.csv"
    output_file = data_dir / "gdp_per_capita.csv"
    
    # Check if files exist
    if not gdp_file.exists():
        raise FileNotFoundError(f"GDP file not found: {gdp_file}")
    if not population_file.exists():
        raise FileNotFoundError(f"Population file not found: {population_file}")
    
    # Read the datasets
    print("Reading GDP data...")
    gdp_df = pd.read_csv(gdp_file)
    print(f"GDP data shape: {gdp_df.shape}")
    
    print("Reading population data...")
    population_df = pd.read_csv(population_file)
    print(f"Population data shape: {population_df.shape}")
    
    # Rename value columns to be more specific
    gdp_df = gdp_df.rename(columns={'value': 'gdp_value'})
    population_df = population_df.rename(columns={'value': 'population_value'})
    
    # Merge the datasets on TIME_PERIOD and REF_AREA
    print("Merging GDP and population data...")
    merged_df = pd.merge(
        gdp_df, 
        population_df, 
        on=['TIME_PERIOD', 'REF_AREA'], 
        how='inner'
    )
    
    print(f"Merged data shape: {merged_df.shape}")
    
    # Compute GDP per capita
    print("Computing GDP per capita...")
    merged_df['gdp_per_capita'] = merged_df['gdp_value'] / merged_df['population_value']
    
    # Create the output dataframe with the required columns
    result_df = merged_df[['TIME_PERIOD', 'REF_AREA', 'gdp_per_capita']].copy()
    result_df = result_df.rename(columns={'gdp_per_capita': 'value'})
    
    # Sort by time period and country for better readability
    result_df = result_df.sort_values(['TIME_PERIOD', 'REF_AREA'])
    
    # Save the result
    print(f"Saving GDP per capita data to {output_file}...")
    result_df.to_csv(output_file, index=False)
    
    # Print summary statistics
    print("\nSummary of GDP per capita computation:")
    print(f"Total records: {len(result_df)}")
    print(f"Time period range: {result_df['TIME_PERIOD'].min()} - {result_df['TIME_PERIOD'].max()}")
    print(f"Number of countries: {result_df['REF_AREA'].nunique()}")
    print(f"GDP per capita range: {result_df['value'].min():.2f} - {result_df['value'].max():.2f}")
    
    # Show some sample data
    print("\nSample GDP per capita data:")
    print(result_df.head(10))
    
    return result_df

if __name__ == "__main__":
    try:
        result = compute_gdp_per_capita()
        print("\nGDP per capita computation completed successfully!")
    except Exception as e:
        print(f"Error computing GDP per capita: {e}")
        raise 