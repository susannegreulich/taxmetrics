#!/usr/bin/env python3
"""
Script to create all 2D CSV files for tax rates, GDP per capita, and GDP per capita growth rates.

This script processes the labeled data which is already in 2D format:
1. GDP per capita - Divides GDP by population for each country
2. Tax rate types - Separates different tax types from the tax revenues data
3. GDP per capita growth rates - Computes year-over-year growth rates

All output files are stored in results/year_country/ directory structure.
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path

def separate_tax_types():
    """Separate different tax types from the tax revenues data."""
    
    print("\n" + "="*60)
    print("STEP 1: Separating tax rate types from tax revenues data")
    print("="*60)
    
    # Read the labeled tax revenues data
    input_file = "data/labeled/tax_revenues_labeled.csv"
    output_dir = "results/year_country"
    
    print(f"Reading data from {input_file}...")
    df = pd.read_csv(input_file)
    
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    print(f"Data shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    # Get unique tax types from the STANDARD_REVENUE column
    tax_types = df['STANDARD_REVENUE'].unique()
    
    print(f"Found {len(tax_types)} tax rate types:")
    for i, tax_type in enumerate(tax_types, 1):
        print(f"  {i}. {tax_type}")
    
    # Get country columns (all columns except TIME_PERIOD and STANDARD_REVENUE)
    country_columns = [col for col in df.columns if col not in ['TIME_PERIOD', 'STANDARD_REVENUE']]
    print(f"Number of countries: {len(country_columns)}")
    
    # Process each tax rate type
    for tax_type in tax_types:
        print(f"\nProcessing: {tax_type}")
        
        # Filter data for this tax type
        tax_data = df[df['STANDARD_REVENUE'] == tax_type].copy()
        
        if tax_data.empty:
            print(f"  No data found for {tax_type}")
            continue
        
        # Drop the STANDARD_REVENUE column since we're separating by tax type
        tax_data = tax_data.drop('STANDARD_REVENUE', axis=1)
        
        # Set TIME_PERIOD as index for easier processing
        tax_data = tax_data.set_index('TIME_PERIOD')
        
        # Sort by year
        tax_data = tax_data.sort_index()
        
        # Sort columns alphabetically (TIME_PERIOD will be first when we reset index)
        tax_data = tax_data.reindex(sorted(tax_data.columns), axis=1)
        
        # Create filename (sanitize the tax type name)
        safe_tax_type = tax_type.replace(' ', '_').replace(',', '').replace('(', '').replace(')', '').replace('&', 'and').replace('__', '_')
        filename = f"{safe_tax_type}.csv"
        filepath = os.path.join(output_dir, filename)
        
        # Reset index to make TIME_PERIOD a regular column
        tax_data = tax_data.reset_index()
        
        # Save to CSV
        tax_data.to_csv(filepath, index=False)
        
        print(f"  Created: {filepath}")
        print(f"  Shape: {tax_data.shape} (years: {len(tax_data)}, countries: {len(tax_data.columns)-1})")
        print(f"  Year range: {tax_data['TIME_PERIOD'].min()} - {tax_data['TIME_PERIOD'].max()}")
        print(f"  Countries: {len(tax_data.columns)-1}")
        
        # Show some statistics
        numeric_data = tax_data.drop('TIME_PERIOD', axis=1)
        print(f"  Data coverage: {numeric_data.notna().sum().sum()} / {numeric_data.size} cells ({numeric_data.notna().sum().sum() / numeric_data.size * 100:.1f}%)")
        
        # Show top 5 countries by average tax rate
        country_means = numeric_data.mean().sort_values(ascending=False)
        print(f"  Top 5 countries by average rate:")
        for i, (country, mean_rate) in enumerate(country_means.head().items(), 1):
            print(f"    {i}. {country}: {mean_rate:.2f}%")
    
    print(f"\nAll tax rate files created in: {output_dir}")

def compute_gdp_per_capita():
    """
    Compute GDP per capita by dividing GDP by population for each country.
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
    
    # Set TIME_PERIOD as index for both datasets
    gdp_df = gdp_df.set_index('TIME_PERIOD')
    population_df = population_df.set_index('TIME_PERIOD')
    
    # Get common countries (columns that exist in both datasets)
    gdp_countries = set(gdp_df.columns)
    population_countries = set(population_df.columns)
    common_countries = gdp_countries.intersection(population_countries)
    
    print(f"Common countries between GDP and population: {len(common_countries)}")
    
    # Compute GDP per capita for common countries
    print("Computing GDP per capita...")
    gdp_per_capita_df = pd.DataFrame(index=gdp_df.index)
    
    for country in common_countries:
        # GDP data is in millions, Population data is in thousands
        # So 1mio/1000 = 1000, multiply by 1000 to get GDP/capita in unit of ONE USD PPP
        gdp_per_capita_df[country] = (gdp_df[country] / population_df[country]) * 1000
    
    # Sort by year
    gdp_per_capita_df = gdp_per_capita_df.sort_index()
    
    # Sort columns alphabetically
    gdp_per_capita_df = gdp_per_capita_df.reindex(sorted(gdp_per_capita_df.columns), axis=1)
    
    # Reset index to make TIME_PERIOD a regular column
    gdp_per_capita_df = gdp_per_capita_df.reset_index()
    
    # Save the result
    print(f"Saving GDP per capita data to {output_file}...")
    gdp_per_capita_df.to_csv(output_file, index=False)

    # Print summary statistics
    print("\nSummary of GDP per capita computation:")
    print(f"Total time periods: {len(gdp_per_capita_df)}")
    print(f"Time period range: {gdp_per_capita_df['TIME_PERIOD'].min()} - {gdp_per_capita_df['TIME_PERIOD'].max()}")
    print(f"Number of countries: {len(common_countries)}")
    
    # Calculate overall statistics (excluding NaN values)
    numeric_data = gdp_per_capita_df.drop('TIME_PERIOD', axis=1)
    all_values = numeric_data.values.flatten()
    valid_values = all_values[~np.isnan(all_values)]
    
    print(f"GDP per capita range: {valid_values.min():.2f} - {valid_values.max():.2f}")
    print(f"Average GDP per capita: {valid_values.mean():.2f}")
    print(f"Median GDP per capita: {np.median(valid_values):.2f}")
    print(f"Standard deviation: {valid_values.std():.2f}")
    
    # Show some sample data
    print("\nSample GDP per capita data:")
    print(gdp_per_capita_df.head(10))
    
    # Show countries with highest and lowest average GDP per capita
    print("\nCountries with highest average GDP per capita:")
    avg_gdp_by_country = numeric_data.mean().sort_values(ascending=False)
    print(avg_gdp_by_country.head(10))
    
    print("\nCountries with lowest average GDP per capita:")
    print(avg_gdp_by_country.tail(10))
    
    return gdp_per_capita_df

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
    
    # Sort columns alphabetically
    growth_rates_df = growth_rates_df.reindex(sorted(growth_rates_df.columns), axis=1)
    
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
        # Step 1: Separate tax rate types
        separate_tax_types()
        
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