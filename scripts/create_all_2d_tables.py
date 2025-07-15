#!/usr/bin/env python3
"""
Script to create all 2D CSV files for tax rates, GDP per capita, and GDP per capita growth rates.

This script combines the functionality of:
1. create_tax_rate_2d_csvs.py - Creates 2D CSV files for each tax rate type
2. gdp_per_capita.py - Computes GDP per capita by dividing GDP by population
3. gdp_per_capita_growth_rates.py - Computes GDP per capita growth rates

The script processes data in the correct order to ensure dependencies are met.
All output files are stored in results/year_country/ directory structure.
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path

def create_2d_tax_rate_csvs():
    """Create 2D CSV files for each tax rate type."""
    
    print("\n" + "="*60)
    print("STEP 1: Creating 2D CSV files for tax rate types")
    print("="*60)
    
    # Read the labeled tax revenues data
    input_file = "data/labeled/tax_revenues_labeled.csv"
    output_dir = "results/year_country"
    
    print(f"Reading data from {input_file}...")
    df = pd.read_csv(input_file)
    
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Get unique tax rate types
    tax_rate_types = df['STANDARD_REVENUE'].unique()
    print(f"Found {len(tax_rate_types)} tax rate types:")
    for i, tax_type in enumerate(tax_rate_types, 1):
        print(f"  {i}. {tax_type}")
    
    # Process each tax rate type
    for tax_type in tax_rate_types:
        print(f"\nProcessing: {tax_type}")
        
        # Filter data for this tax rate type
        tax_data = df[df['STANDARD_REVENUE'] == tax_type].copy()
        
        if tax_data.empty:
            print(f"  No data found for {tax_type}")
            continue
        
        # Create pivot table: years as rows, countries as columns
        pivot_table = tax_data.pivot_table(
            index='TIME_PERIOD',
            columns='REF_AREA',
            values='value',
            aggfunc='first'  # Take first value if duplicates exist
        )
        
        # Sort by year
        pivot_table = pivot_table.sort_index()
        
        # Create filename (sanitize the tax type name)
        safe_tax_type = tax_type.replace(' ', '_').replace(',', '').replace('(', '').replace(')', '').replace('&', 'and')
        filename = f"{safe_tax_type}.csv"
        filepath = os.path.join(output_dir, filename)
        
        # Save to CSV
        pivot_table.to_csv(filepath)
        
        print(f"  Created: {filepath}")
        print(f"  Shape: {pivot_table.shape} (years: {len(pivot_table)}, countries: {len(pivot_table.columns)})")
        print(f"  Year range: {pivot_table.index.min()} - {pivot_table.index.max()}")
        print(f"  Countries: {len(pivot_table.columns)}")
        
        # Show some statistics
        print(f"  Data coverage: {pivot_table.notna().sum().sum()} / {pivot_table.size} cells ({pivot_table.notna().sum().sum() / pivot_table.size * 100:.1f}%)")
        
        # Show top 5 countries by average tax rate
        country_means = pivot_table.mean().sort_values(ascending=False)
        print(f"  Top 5 countries by average rate:")
        for i, (country, mean_rate) in enumerate(country_means.head().items(), 1):
            print(f"    {i}. {country}: {mean_rate:.2f}%")
    
    print(f"\nAll 2D CSV files created in: {output_dir}")

def compute_gdp_per_capita():
    """
    Compute GDP per capita by dividing GDP by population for matching time periods and countries.
    """
    print("\n" + "="*60)
    print("STEP 2: Computing GDP per capita")
    print("="*60)
    
    # Define file paths
    data_dir = Path("data/labeled")
    results_dir = Path("results/year_country")
    gdp_file = data_dir / "gdp_labeled.csv"
    population_file = data_dir / "population_labeled.csv"
    output_file = results_dir / "gdp_per_capita.csv"
    
    # Check if files exist
    if not gdp_file.exists():
        raise FileNotFoundError(f"GDP file not found: {gdp_file}")
    if not population_file.exists():
        raise FileNotFoundError(f"Population file not found: {population_file}")
    
    # Ensure results directory exists
    results_dir.mkdir(parents=True, exist_ok=True)
    
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
    
    # Pivot the data to create a 2D format with years as rows and countries as columns
    print("Creating 2D format with years as rows and countries as columns...")
    pivot_df = result_df.pivot(index='TIME_PERIOD', columns='REF_AREA', values='value')
    
    # Reset index to make TIME_PERIOD a regular column
    pivot_df = pivot_df.reset_index()
    
    # Save the result
    print(f"Saving GDP per capita data to {output_file}...")
    pivot_df.to_csv(output_file, index=False)

    # Print summary statistics
    print("\nSummary of GDP per capita computation:")
    print(f"Total records: {len(result_df)}")
    print(f"Time period range: {result_df['TIME_PERIOD'].min()} - {result_df['TIME_PERIOD'].max()}")
    print(f"Number of countries: {result_df['REF_AREA'].nunique()}")
    print(f"GDP per capita range: {result_df['value'].min():.2f} - {result_df['value'].max():.2f}")
    print(f"2D format shape: {pivot_df.shape} (rows: time periods, columns: countries + 1)")
    
    # Show some sample data
    print("\nSample GDP per capita data (2D format):")
    print(pivot_df.head(10))
    
    return pivot_df

def compute_gdp_per_capita_growth_rates():
    """
    Compute GDP per capita growth rates by calculating year-over-year percentage changes.
    """
    print("\n" + "="*60)
    print("STEP 3: Computing GDP per capita growth rates")
    print("="*60)
    
    # Define file paths
    results_dir = Path("results/year_country")
    input_file = results_dir / "gdp_per_capita.csv"
    output_file = results_dir / "gdp_per_capita_growth_rates.csv"
    
    # Check if input file exists
    if not input_file.exists():
        raise FileNotFoundError(f"GDP per capita file not found: {input_file}")
    
    # Ensure results directory exists
    results_dir.mkdir(parents=True, exist_ok=True)
    
    # Read the GDP per capita data
    print("Reading GDP per capita data...")
    gdp_per_capita_df = pd.read_csv(input_file)
    print(f"GDP per capita data shape: {gdp_per_capita_df.shape}")
    
    # Set TIME_PERIOD as index for easier calculations
    gdp_per_capita_df = gdp_per_capita_df.set_index('TIME_PERIOD')
    
    # Get list of countries (all columns except TIME_PERIOD)
    countries = [col for col in gdp_per_capita_df.columns]
    
    # Calculate year-over-year growth rates
    print("Computing year-over-year growth rates...")
    growth_rates_df = gdp_per_capita_df.pct_change() * 100
    
    # Reset index to make TIME_PERIOD a regular column
    growth_rates_df = growth_rates_df.reset_index()
    
    # Save the result
    print(f"Saving GDP per capita growth rates to {output_file}...")
    growth_rates_df.to_csv(output_file, index=False)
    
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



def create_all_2d_tables():
    """
    Main function to create all 2D tables in the correct order.
    """
    print("Starting creation of all 2D tables...")
    print("This will create:")
    print("1. Tax rate 2D CSV files (one for each tax type)")
    print("2. GDP per capita 2D CSV file")
    print("3. GDP per capita growth rates 2D CSV file")
    print("All files will be stored in results/year_country/ directory structure")
    
    try:
        # Step 1: Create tax rate 2D CSV files
        create_2d_tax_rate_csvs()
        
        # Step 2: Compute GDP per capita
        gdp_per_capita_df = compute_gdp_per_capita()
        
        # Step 3: Compute GDP per capita growth rates
        growth_rates_df = compute_gdp_per_capita_growth_rates()
        
        print("\n" + "="*60)
        print("ALL 2D TABLES CREATED SUCCESSFULLY!")
        print("="*60)
        print("\nSummary of created files:")
        print("1. Tax rate files: results/year_country/")
        print("2. GDP per capita: results/year_country/gdp_per_capita.csv")
        print("3. GDP per capita growth rates: results/year_country/gdp_per_capita_growth_rates.csv")
        
        return True
        
    except Exception as e:
        print(f"\nError creating 2D tables: {e}")
        raise

if __name__ == "__main__":
    create_all_2d_tables() 