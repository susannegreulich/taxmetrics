#!/usr/bin/env python3
"""
Script to create 2D CSV files for each tax rate type from tax_revenues_labeled.csv.

This script reads the tax revenues data and creates separate 2D CSV files for each
tax rate type, with years as rows and countries as columns.
"""

import pandas as pd
import os
from pathlib import Path

def create_2d_tax_rate_csvs():
    """Create 2D CSV files for each tax rate type."""
    
    # Read the labeled tax revenues data
    input_file = "data/labeled/tax_revenues_labeled.csv"
    output_dir = "results/tax_rate_2d_csvs"
    
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
    
    # Create a summary file
    create_summary_file(df, output_dir)

def create_summary_file(df, output_dir):
    """Create a summary file with information about all tax rate types."""
    
    summary_data = []
    
    for tax_type in df['STANDARD_REVENUE'].unique():
        tax_data = df[df['STANDARD_REVENUE'] == tax_type]
        
        summary_data.append({
            'Tax Rate Type': tax_type,
            'Total Records': len(tax_data),
            'Countries': tax_data['REF_AREA'].nunique(),
            'Years': tax_data['TIME_PERIOD'].nunique(),
            'Year Range': f"{tax_data['TIME_PERIOD'].min()} - {tax_data['TIME_PERIOD'].max()}",
            'Average Rate': f"{tax_data['value'].mean():.2f}%",
            'Min Rate': f"{tax_data['value'].min():.2f}%",
            'Max Rate': f"{tax_data['value'].max():.2f}%",
            'Data Coverage': f"{tax_data['value'].notna().sum() / len(tax_data) * 100:.1f}%"
        })
    
    summary_df = pd.DataFrame(summary_data)
    summary_file = os.path.join(output_dir, "summary_statistics.csv")
    summary_df.to_csv(summary_file, index=False)
    
    print(f"Summary statistics saved to: {summary_file}")

if __name__ == "__main__":
    create_2d_tax_rate_csvs() 