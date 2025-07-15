#!/usr/bin/env python3
"""
Script to analyze missing values across CSV datasets in the year_country folder.
Creates a summary table with countries as rows and datasets as columns, showing missing value counts.
The results show that only 32 countries have zero missing values. So the analysis would be
more clean using ONLY these countries. For now I've chosen to use all data. 
Also generates descriptive statistics for all CSV files across all countries and years.
"""

import pandas as pd
import os
import glob
from pathlib import Path

def get_descriptive_stats():
    """Generate descriptive statistics for all CSV files across all countries and years."""
    
    data_folder = Path("results/over_time")
    
    # Define the specific CSV files to analyze (excluding output files)
    target_files = [
        "gdp_per_capita.csv",
        "gdp_per_capita_growth_rates.csv", 
        "Total_tax_revenue.csv",
        "Taxes_on_income_profits_and_capital_gains_of_individuals_and_corporations.csv",
        "Taxes_on_goods_and_services.csv",
        "Taxes_on_property.csv",
        "Social_security_contributions_SSC.csv"
    ]
    
    # Define units for each dataset
    units_mapping = {
        "gdp_per_capita.csv": "PPP-adjusted USD",
        "gdp_per_capita_growth_rates.csv": "%",
        "Total_tax_revenue.csv": "%",
        "Taxes_on_income_profits_and_capital_gains_of_individuals_and_corporations.csv": "%",
        "Taxes_on_goods_and_services.csv": "%",
        "Taxes_on_property.csv": "%",
        "Social_security_contributions_SSC.csv": "%"
    }
    
    csv_files = [f for f in data_folder.glob("*.csv") if f.name in target_files]
    
    descriptive_stats = {}
    units_data = {}
    
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        
        # Set TIME_PERIOD as index for easier analysis
        df.set_index('TIME_PERIOD', inplace=True)
        
        # Flatten all values across countries and years (excluding the index)
        all_values = df.to_numpy().flatten()
        # Remove NaN values
        all_values = all_values[~pd.isna(all_values)]
        
        # Calculate statistics across all countries and years
        stats = {
            'min': all_values.min(),
            'mean': all_values.mean(),
            'median': pd.Series(all_values).median(),
            'max': all_values.max(),
            'std': all_values.std()
        }
        
        # Store statistics with dataset name as key
        dataset_name = csv_file.stem.replace('_', ' ').title()
        descriptive_stats[dataset_name] = stats
        
        # Store units for this dataset
        units_data[dataset_name] = units_mapping[csv_file.name]
    
    return descriptive_stats, units_data

def save_descriptive_stats():
    """Save descriptive statistics for all CSV files to a separate file."""
    
    descriptive_stats, units_data = get_descriptive_stats()
    data_folder = Path("results/over_time")
    
    # Create a DataFrame with datasets as rows and statistics as columns
    stats_df = pd.DataFrame(descriptive_stats).T
    
    # Sort rows alphabetically by dataset name
    stats_df = stats_df.sort_index()
    
    # Create units Series and align with stats_df
    units_series = pd.Series(units_data)
    units_series = units_series.reindex(stats_df.index)  # Align with sorted stats_df
    
    # Add units as a new column after the index
    stats_df.insert(0, 'Units', units_series)
    
    # Set index name to 'Dataset' so the first column is labeled
    stats_df.index.name = 'Dataset'
    
    # Save the results
    output_file = data_folder / "descriptive_stats.csv"
    stats_df.to_csv(output_file)
    
    return output_file

def analyze_missing_values():
    """Analyze missing values across CSV files in the over_time folder."""
    
    # Path to the over_time folder
    data_folder = Path("results/over_time")
    
    # Define the specific CSV files to analyze for missing values
    target_files = [
        "gdp_per_capita.csv",
        "gdp_per_capita_growth_rates.csv", 
        "Total_tax_revenue.csv",
        "Taxes_on_income_profits_and_capital_gains_of_individuals_and_corporations.csv",
        "Taxes_on_goods_and_services.csv",
        "Taxes_on_property.csv",
        "Social_security_contributions_SSC.csv"
    ]
    csv_files = [f for f in data_folder.glob("*.csv") if f.name in target_files]
    
    # Dictionary to store missing value counts for each dataset
    missing_data = {}
    
    for csv_file in csv_files:
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
    
    # Add "Country" to the first row and first column
    missing_df.index.name = "Country"
    
    # Sort by total missing values (descending) and then by country name
    missing_df['Total_Missing'] = missing_df.sum(axis=1)
    missing_df = missing_df.sort_values(['Total_Missing'], ascending=[False])
    
    # Remove the Total_Missing column for the final output
    final_df = missing_df.drop('Total_Missing', axis=1)
    
    # Add a summary row at the bottom
    summary_row = pd.DataFrame([final_df.sum()], index=['TOTAL_MISSING'])
    final_df = pd.concat([final_df, summary_row])
    
    # Add summary statistics as additional rows
    total_datasets = len(csv_files)
    total_countries = len(final_df) - 1  # Exclude the TOTAL_MISSING row
    total_missing_values = final_df.loc['TOTAL_MISSING'].sum()
    
    # Add summary statistics rows
    stats_data = {
        'Summary_Statistics': ['Total Datasets Analyzed', 'Total Countries', 'Total Missing Values Across All Datasets']
    }
    for col in final_df.columns:
        stats_data[col] = [total_datasets, total_countries, total_missing_values]
    
    stats_df = pd.DataFrame(stats_data)
    stats_df.set_index('Summary_Statistics', inplace=True)
    
    # Add top 10 countries with most missing values
    top_missing = missing_df.head(10)
    top_countries_data = {}
    
    # Create one row per country using existing dataset columns
    for i, country in enumerate(top_missing.index):
        total = top_missing.loc[country, 'Total_Missing']
        row_name = f"Top_{i+1}_Country"
        
        # Create a row with the country name in the first dataset column and missing count in the second
        row_data = {}
        for col in final_df.columns:
            if col == final_df.columns[0]:  # First dataset column
                row_data[col] = country
            elif col == final_df.columns[1]:  # Second dataset column  
                row_data[col] = total
            else:
                row_data[col] = ""
        
        top_countries_data[row_name] = row_data
    
    top_countries_df = pd.DataFrame(top_countries_data).T
    
    # Add header row for top countries section
    header_data = {}
    for col in final_df.columns:
        if col == final_df.columns[0]:  # First dataset column
            header_data[col] = "Countries with most missing values"
        else:
            header_data[col] = ""
    
    header_df = pd.DataFrame([header_data], index=['Top_Countries_Header'])
    
    # Combine all dataframes
    final_df = pd.concat([final_df, stats_df, header_df, top_countries_df])
    
    # Save the results in the same folder
    output_file = data_folder / "missing_values.csv"
    final_df.to_csv(output_file)
    
    return final_df

if __name__ == "__main__":
    # Generate and save descriptive statistics first
    stats_file = save_descriptive_stats()
    
    # Then analyze missing values
    missing_analysis = analyze_missing_values() 