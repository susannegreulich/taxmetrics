#!/usr/bin/env python3
"""
Script to compute country averages over time for GDP per capita growth rates and tax rates.
This script reads CSV files from the results/over_time directory and calculates
the average values for each country across all available time periods.
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path

def load_and_process_csv(file_path):
    """
    Load a CSV file and return a DataFrame with time periods as index and countries as columns.
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        pd.DataFrame: DataFrame with time periods as index and countries as columns
    """
    try:
        df = pd.read_csv(file_path)
        # Set TIME_PERIOD as index
        df.set_index('TIME_PERIOD', inplace=True)
        return df
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def compute_country_averages(df):
    """
    Compute average values for each country across all time periods.
    
    Args:
        df (pd.DataFrame): DataFrame with time periods as index and countries as columns
        
    Returns:
        pd.Series: Series with country names as index and average values as values
    """
    if df is None or df.empty:
        return pd.Series()
    
    # Convert to numeric, replacing non-numeric values with NaN
    numeric_df = df.apply(pd.to_numeric, errors='coerce')
    
    # Compute mean for each country, ignoring NaN values
    averages = numeric_df.mean(axis=0, skipna=True)
    
    # Sort by average value (descending)
    averages = averages.sort_values(ascending=False)
    
    return averages

def main():
    """Main function to compute and display country averages."""
    
    # Define the base directory
    base_dir = Path("results/over_time")
    
    # Define the files to process
    files_to_process = {
        "GDP per capita": "gdp_per_capita.csv",
        "GDP per capita growth rates": "gdp_per_capita_growth_rates.csv",
        "Total tax revenue": "Total_tax_revenue.csv",
        "Taxes on goods and services": "Taxes_on_goods_and_services.csv",
        "Taxes on income, profits, and capital gains": "Taxes_on_income_profits_and_capital_gains_of_individuals_and_corporations.csv",
        "Taxes on property": "Taxes_on_property.csv",
        "Social security contributions (SSC)": "Social_security_contributions_SSC.csv"
    }
    
    # Create output directory
    output_dir = Path("results/averages")
    output_dir.mkdir(exist_ok=True)
    
    # Dictionary to store all results
    all_results = {}
    
    print("Computing country averages over time...")
    print("=" * 60)
    
    # Process each file
    for metric_name, filename in files_to_process.items():
        file_path = base_dir / filename
        
        if not file_path.exists():
            print(f"Warning: File {file_path} not found, skipping...")
            continue
            
        print(f"\nProcessing: {metric_name}")
        print("-" * 40)
        
        # Load and process the data
        df = load_and_process_csv(file_path)
        if df is not None:
            # Compute averages
            averages = compute_country_averages(df)
            
            if not averages.empty:
                # Store results
                all_results[metric_name] = averages
                
                # Display top 10 countries
                print(f"Top 10 countries by average {metric_name}:")
                print(averages.head(10).to_string())
            else:
                print("No valid data found for computing averages.")
        else:
            print(f"Failed to load data from {file_path}")
    
    # Create a summary DataFrame with all metrics
    if all_results:
        print("\n" + "=" * 60)
        print("SUMMARY: All metrics combined")
        print("=" * 60)
        
        # Create a DataFrame with all results
        summary_df = pd.DataFrame(all_results)
        
        # Add "Country" as the name for the index column
        summary_df.index.name = "Country"
        
        # Display summary statistics
        print("\nSummary statistics for all metrics:")
        print(summary_df.describe())
        
        # Save combined results to a single CSV file
        summary_file = output_dir / "all_metrics_country_averages.csv"
        summary_df.to_csv(summary_file)
        print(f"\nAll averages saved to: {summary_file}")
        
        # Display top 10 countries for each metric
        print("\nTop 10 countries for each metric:")
        print("=" * 60)
        
        for metric_name, averages in all_results.items():
            print(f"\n{metric_name}:")
            print("-" * 40)
            print(averages.head(10).to_string())
    
    print(f"\nAll results saved to: {output_dir}")

if __name__ == "__main__":
    main() 