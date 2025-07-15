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

def create_summary_markdown_report():
    """
    Create a comprehensive markdown report with summary statistics for all created CSV tables.
    """
    print("\n" + "="*60)
    print("STEP 4: Creating Summary Statistics Markdown Report")
    print("="*60)
    
    output_dir = Path("results/year_country")
    report_file = output_dir / "summary_statistics_report.md"
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize markdown content
    md_content = []
    md_content.append("# 2D Tables Summary Statistics Report")
    md_content.append("")
    md_content.append(f"*Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    md_content.append("")
    md_content.append("## Overview")
    md_content.append("")
    md_content.append("This report provides summary statistics for all 2D CSV tables created by the data processing pipeline.")
    md_content.append("")
    
    # Get all CSV files in the results directory
    csv_files = list(output_dir.glob("*.csv"))
    csv_files.sort()
    
    md_content.append(f"## Files Analyzed ({len(csv_files)} total)")
    md_content.append("")
    for i, file in enumerate(csv_files, 1):
        md_content.append(f"{i}. `{file.name}`")
    md_content.append("")
    
    # Process each CSV file
    for csv_file in csv_files:
        print(f"Analyzing: {csv_file.name}")
        
        try:
            df = pd.read_csv(csv_file)
            
            # Add file section header
            md_content.append(f"## {csv_file.name}")
            md_content.append("")
            
            # Basic file information
            md_content.append("### File Information")
            md_content.append("")
            md_content.append(f"- **File size**: {csv_file.stat().st_size / 1024:.1f} KB")
            md_content.append(f"- **Shape**: {df.shape[0]} rows × {df.shape[1]} columns")
            md_content.append("")
            
            # Time period information (if TIME_PERIOD column exists)
            if 'TIME_PERIOD' in df.columns:
                time_periods = df['TIME_PERIOD'].dropna()
                if len(time_periods) > 0:
                    md_content.append("### Time Period Coverage")
                    md_content.append("")
                    md_content.append(f"- **Year range**: {time_periods.min()} - {time_periods.max()}")
                    md_content.append(f"- **Total years**: {len(time_periods.unique())}")
                    md_content.append("")
            
            # Country information (all columns except TIME_PERIOD)
            country_columns = [col for col in df.columns if col != 'TIME_PERIOD']
            md_content.append("### Geographic Coverage")
            md_content.append("")
            md_content.append(f"- **Number of countries/regions**: {len(country_columns)}")
            md_content.append("")
            
            # Data quality statistics
            md_content.append("### Data Quality")
            md_content.append("")
            
            # Calculate data coverage for each country
            if 'TIME_PERIOD' in df.columns:
                data_coverage = []
                for col in country_columns:
                    coverage = df[col].notna().sum() / len(df) * 100
                    data_coverage.append((col, coverage))
                
                # Sort by coverage
                data_coverage.sort(key=lambda x: x[1], reverse=True)
                
                md_content.append("#### Data Coverage by Country (Top 10)")
                md_content.append("")
                md_content.append("| Country | Coverage (%) |")
                md_content.append("|---------|-------------|")
                for country, coverage in data_coverage[:10]:
                    # Ensure consistent column widths
                    country_col = f"{country:<30}"  # Left-align with 30 chars width
                    coverage_col = f"{coverage:>8.1f}%"  # Right-align with 8 chars width
                    md_content.append(f"| {country_col} | {coverage_col} |")
                md_content.append("")
                
                # Overall statistics
                total_cells = df[country_columns].size
                filled_cells = df[country_columns].notna().sum().sum()
                overall_coverage = filled_cells / total_cells * 100
                
                md_content.append(f"- **Overall data coverage**: {overall_coverage:.1f}% ({filled_cells:,} / {total_cells:,} cells)")
                md_content.append("")
            
            # Statistical summary for numerical data
            md_content.append("### Statistical Summary")
            md_content.append("")
            
            # Get numerical columns (exclude TIME_PERIOD)
            numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if 'TIME_PERIOD' in numerical_cols:
                numerical_cols.remove('TIME_PERIOD')
            
            if numerical_cols:
                # Calculate statistics across all numerical columns
                all_values = df[numerical_cols].values.flatten()
                valid_values = all_values[~np.isnan(all_values)]
                
                if len(valid_values) > 0:
                    md_content.append("| Statistic | Value |")
                    md_content.append("|-----------|-------|")
                    md_content.append(f"| Count | {len(valid_values):>10,} |")
                    md_content.append(f"| Mean | {np.mean(valid_values):>10.2f} |")
                    md_content.append(f"| Median | {np.median(valid_values):>10.2f} |")
                    md_content.append(f"| Std Dev | {np.std(valid_values):>10.2f} |")
                    md_content.append(f"| Min | {np.min(valid_values):>10.2f} |")
                    md_content.append(f"| Max | {np.max(valid_values):>10.2f} |")
                    md_content.append(f"| 25th Percentile | {np.percentile(valid_values, 25):>10.2f} |")
                    md_content.append(f"| 75th Percentile | {np.percentile(valid_values, 75):>10.2f} |")
                    md_content.append("")
                    
                    # Special analysis for specific file types
                    if "gdp_per_capita" in csv_file.name.lower():
                        md_content.append("#### GDP per Capita Analysis")
                        md_content.append("")
                        md_content.append("| Country | Average GDP per Capita |")
                        md_content.append("|---------|----------------------|")
                        country_means = df[country_columns].mean().sort_values(ascending=False)
                        for country, mean_val in country_means.head(10).items():
                            # Ensure consistent column widths
                            country_col = f"{country:<30}"  # Left-align with 30 chars width
                            gdp_col = f"{mean_val:>15.2f}"  # Right-align with 15 chars width
                            md_content.append(f"| {country_col} | {gdp_col} |")
                        md_content.append("")
                        
                    elif "growth_rates" in csv_file.name.lower():
                        md_content.append("#### Growth Rate Analysis")
                        md_content.append("")
                        md_content.append("| Country | Average Growth Rate (%) |")
                        md_content.append("|---------|----------------------|")
                        country_means = df[country_columns].mean().sort_values(ascending=False)
                        for country, mean_val in country_means.head(10).items():
                            # Ensure consistent column widths
                            country_col = f"{country:<30}"  # Left-align with 30 chars width
                            growth_col = f"{mean_val:>15.2f}%"  # Right-align with 15 chars width
                            md_content.append(f"| {country_col} | {growth_col} |")
                        md_content.append("")
                        
                        md_content.append("| Country | Average Growth Rate (%) |")
                        md_content.append("|---------|----------------------|")
                        for country, mean_val in country_means.tail(10).items():
                            # Ensure consistent column widths
                            country_col = f"{country:<30}"  # Left-align with 30 chars width
                            growth_col = f"{mean_val:>15.2f}%"  # Right-align with 15 chars width
                            md_content.append(f"| {country_col} | {growth_col} |")
                        md_content.append("")
                        
                    else:
                        # For tax rate files
                        md_content.append("#### Tax Rate Analysis")
                        md_content.append("")
                        md_content.append("| Country | Average Rate (%) |")
                        md_content.append("|---------|----------------|")
                        country_means = df[country_columns].mean().sort_values(ascending=False)
                        for country, mean_val in country_means.head(10).items():
                            # Ensure consistent column widths
                            country_col = f"{country:<30}"  # Left-align with 30 chars width
                            rate_col = f"{mean_val:>10.2f}%"  # Right-align with 10 chars width
                            md_content.append(f"| {country_col} | {rate_col} |")
                        md_content.append("")
            
            md_content.append("---")
            md_content.append("")
            
        except Exception as e:
            print(f"Error analyzing {csv_file.name}: {e}")
            md_content.append(f"## {csv_file.name}")
            md_content.append("")
            md_content.append(f"*Error reading file: {str(e)}*")
            md_content.append("")
            md_content.append("---")
            md_content.append("")
    
    # Add summary section
    md_content.append("## Summary")
    md_content.append("")
    md_content.append(f"This report covers {len(csv_files)} CSV files containing 2D data tables.")
    md_content.append("All files are stored in the `results/year_country/` directory.")
    md_content.append("")
    md_content.append("### File Types Created:")
    md_content.append("")
    md_content.append("1. **Tax Rate Files**: Individual CSV files for each tax rate type")
    md_content.append("2. **GDP per Capita**: Combined GDP and population data")
    md_content.append("3. **GDP per Capita Growth Rates**: Year-over-year percentage changes")
    md_content.append("")
    
    # Write the markdown file
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_content))
    
    print(f"Summary statistics report saved to: {report_file}")
    return report_file

def create_all_2d_tables():
    """
    Main function to create all 2D tables in the correct order.
    """
    print("Starting creation of all 2D tables...")
    print("This will create:")
    print("1. Tax rate 2D CSV files (one for each tax type)")
    print("2. GDP per capita 2D CSV file")
    print("3. GDP per capita growth rates 2D CSV file")
    print("4. Summary statistics markdown report")
    print("All files will be stored in results/year_country/ directory structure")
    
    try:
        # Step 1: Create tax rate 2D CSV files
        create_2d_tax_rate_csvs()
        
        # Step 2: Compute GDP per capita
        gdp_per_capita_df = compute_gdp_per_capita()
        
        # Step 3: Compute GDP per capita growth rates
        growth_rates_df = compute_gdp_per_capita_growth_rates()
        
        # Step 4: Create summary statistics markdown report
        report_file = create_summary_markdown_report()
        
        print("\n" + "="*60)
        print("ALL 2D TABLES CREATED SUCCESSFULLY!")
        print("="*60)
        print("\nSummary of created files:")
        print("1. Tax rate files: results/year_country/")
        print("2. GDP per capita: results/year_country/gdp_per_capita.csv")
        print("3. GDP per capita growth rates: results/year_country/gdp_per_capita_growth_rates.csv")
        print(f"4. Summary report: {report_file}")
        
        return True
        
    except Exception as e:
        print(f"\nError creating 2D tables: {e}")
        raise

if __name__ == "__main__":
    create_all_2d_tables() 