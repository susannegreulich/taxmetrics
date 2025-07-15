#!/usr/bin/env python3
"""
Script to analyze missing values across all CSV datasets in the country_over_time folder.
Creates a summary table with countries as rows and datasets as columns, showing missing value counts.
"""

import pandas as pd
import os
import glob
from pathlib import Path

def analyze_missing_values():
    """Analyze missing values across all CSV files in the country_over_time folder."""
    
    # Path to the country_over_time folder
    data_folder = Path("results/country_over_time")
    
    # Get only GDP per capita and Total tax revenue CSV files
    target_files = ["gdp_per_capita.csv", "Total_tax_revenue.csv"]
    csv_files = [f for f in data_folder.glob("*.csv") if f.name in target_files]
    
    # Dictionary to store missing value counts for each dataset
    missing_data = {}
    
    print(f"Analyzing {len(csv_files)} CSV files...")
    
    for csv_file in csv_files:
        print(f"Processing: {csv_file.name}")
        
        # Read the CSV file
        df = pd.read_csv(csv_file)
        
        # Set TIME_PERIOD as index for easier analysis
        df.set_index('TIME_PERIOD', inplace=True)
        
        # Count missing values for each country
        missing_counts = df.isnull().sum()
        
        # Store in dictionary with dataset name as key
        dataset_name = csv_file.stem.replace('_', ' ').title()
        missing_data[dataset_name] = missing_counts
    
    # Create a DataFrame with countries as rows and datasets as columns
    missing_df = pd.DataFrame(missing_data)
    
    # Sort by total missing values (descending) and then by country name
    missing_df['Total_Missing'] = missing_df.sum(axis=1)
    missing_df = missing_df.sort_values(['Total_Missing'], ascending=[False])
    
    # Remove the Total_Missing column for the final output
    final_df = missing_df.drop('Total_Missing', axis=1)
    
    # Add a summary row at the bottom
    summary_row = pd.DataFrame([final_df.sum()], index=['TOTAL_MISSING'])
    final_df = pd.concat([final_df, summary_row])
    
    # Save the results
    output_file = data_folder / "missing_values_summary.csv"
    final_df.to_csv(output_file)
    
    print(f"\nAnalysis complete!")
    print(f"Results saved to: {output_file}")
    
    # Print summary statistics
    print(f"\nSummary:")
    print(f"Total datasets analyzed: {len(csv_files)}")
    print(f"Total countries: {len(final_df) - 1}")  # Exclude the summary row
    print(f"Total missing values across all datasets: {final_df.loc['TOTAL_MISSING'].sum()}")
    
    # Show top 10 countries with most missing values
    print(f"\nTop 10 countries with most missing values:")
    top_missing = missing_df.head(10)
    for country in top_missing.index:
        total = top_missing.loc[country, 'Total_Missing']
        print(f"  {country}: {total} missing values")
    
    return final_df

if __name__ == "__main__":
    analyze_missing_values() 