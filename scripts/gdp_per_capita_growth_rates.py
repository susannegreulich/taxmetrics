#!/usr/bin/env python3
"""
Script to compute GDP per capita growth rates from the existing gdp_per_capita.csv file.
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path

def compute_gdp_per_capita_growth_rates():
    """
    Compute GDP per capita growth rates by calculating year-over-year percentage changes.
    """
    # Define file paths
    results_dir = Path("results")
    input_file = results_dir / "gdp_per_capita.csv"
    output_file = results_dir / "gdp_per_capita_growth_rates.csv"
    
    # Check if input file exists
    if not input_file.exists():
        raise FileNotFoundError(f"GDP per capita file not found: {input_file}")
    
    # Ensure results directory exists
    results_dir.mkdir(exist_ok=True)
    
    # Read the GDP per capita data
    print("Reading GDP per capita data...")
    gdp_per_capita_df = pd.read_csv(input_file)
    print(f"GDP per capita data shape: {gdp_per_capita_df.shape}")
    
    # Set TIME_PERIOD as index for easier calculations
    gdp_per_capita_df = gdp_per_capita_df.set_index('TIME_PERIOD')
    
    # Calculate year-over-year growth rates
    print("Computing year-over-year growth rates...")
    growth_rates_df = gdp_per_capita_df.pct_change() * 100
    
    # Reset index to make TIME_PERIOD a regular column
    growth_rates_df = growth_rates_df.reset_index()
    
    # Save the result
    print(f"Saving GDP per capita growth rates to {output_file}...")
    growth_rates_df.to_csv(output_file, index=False)
    
    # Remove Plotly interactive graph generation
    # (Code block removed)
    
    # Calculate summary statistics
    print("\nSummary of GDP per capita growth rates computation:")
    print(f"Total time periods: {len(growth_rates_df)}")
    print(f"Time period range: {growth_rates_df['TIME_PERIOD'].min()} - {growth_rates_df['TIME_PERIOD'].max()}")
    print(f"Number of countries: {len(countries)}")
    
    # Calculate overall statistics (excluding NaN values)
    all_growth_rates = growth_rates_df[countries].values.flatten()
    valid_growth_rates = all_growth_rates[~np.isnan(all_growth_rates)]
    
    print(f"Growth rate range: {valid_growth_rates.min():.2f}% - {valid_growth_rates.max():.2f}%")
    print(f"Average growth rate: {valid_growth_rates.mean():.2f}%")
    print(f"Median growth rate: {np.median(valid_growth_rates):.2f}%")
    print(f"Standard deviation: {valid_growth_rates.std():.2f}%")
    
    # Show some sample data
    print("\nSample GDP per capita growth rates data:")
    print(growth_rates_df.head(10))
    
    # Show countries with highest and lowest average growth rates
    print("\nCountries with highest average growth rates:")
    avg_growth_by_country = growth_rates_df[countries].mean().sort_values(ascending=False)
    print(avg_growth_by_country.head(10))
    
    print("\nCountries with lowest average growth rates:")
    print(avg_growth_by_country.tail(10))
    
    return growth_rates_df

if __name__ == "__main__":
    try:
        result = compute_gdp_per_capita_growth_rates()
        print("\nGDP per capita growth rates computation completed successfully!")
    except Exception as e:
        print(f"Error computing GDP per capita growth rates: {e}")
        raise 