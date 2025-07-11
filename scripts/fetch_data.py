#!/usr/bin/env python3
"""
Example: Collecting OECD Tax Data

This script demonstrates how to collect and process OECD tax data
for tax policy analysis.

Data Sources:
- Revenue Statistics: https://stats.oecd.org/index.aspx?DataSetCode=REV
- Taxing Wages: https://stats.oecd.org/index.aspx?DataSetCode=TAXWAGE
- Tax Structures: https://stats.oecd.org/index.aspx?DataSetCode=TAX_STRUCT
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import pandas as pd
import numpy as np
from data_collection.oecd_data_collector import OECDDataCollector
from data_collection.tax_data_processor import TaxDataProcessor


def collect_basic_data():
    """Collect basic OECD tax data for a few countries."""
    print("OECD Tax Data Collection Example")
    print("=" * 40)
    
    # Initialize collector
    collector = OECDDataCollector()
    
    # Define countries and years
    countries = ['USA', 'GBR', 'DEU', 'FRA', 'JPN']
    years = list(range(2018, 2024))
    
    print(f"Collecting data for: {', '.join(countries)}")
    print(f"Time period: {years[0]} - {years[-1]}")
    
    # Collect data
    print("\n1. Collecting revenue statistics...")
    revenue_data = collector.get_revenue_statistics(countries, years)
    print(f"   Retrieved {len(revenue_data)} revenue records")
    
    print("\n2. Collecting tax rates...")
    tax_rates_data = collector.get_tax_rates(countries, years)
    print(f"   Retrieved {len(tax_rates_data)} tax rate records")
    
    print("\n3. Collecting tax structures...")
    tax_structures_data = collector.get_tax_structures(countries, years)
    print(f"   Retrieved {len(tax_structures_data)} tax structure records")
    
    # Combine all data
    data = {
        'revenue_statistics': revenue_data,
        'tax_rates': tax_rates_data,
        'tax_structures': tax_structures_data
    }
    
    return data


def process_data(data):
    """Process and clean the collected data."""
    print("\n3. Processing and cleaning data...")
    
    # Initialize processor
    processor = TaxDataProcessor()
    
    # Validate data
    validation_results = processor.validate_data(data)
    print("   Validation results:")
    for dataset, is_valid in validation_results.items():
        status = "✓ PASS" if is_valid else "✗ FAIL"
        print(f"     {dataset}: {status}")
    
    # Clean data
    cleaned_data = processor.clean_data(data)
    print(f"   Cleaned {len(cleaned_data)} datasets")
    
    # Create analysis-ready dataset
    analysis_data = processor.create_analysis_ready_dataset(cleaned_data)
    print(f"   Created analysis-ready dataset with {len(analysis_data)} records")
    
    return cleaned_data, analysis_data





def save_data(data, analysis_data):
    """Save the collected and processed data."""
    print("\n4. Saving data...")
    
    # Create output directories
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    
    # Save raw data to data/raw folder
    for dataset_name, df in data.items():
        if not df.empty:
            filename = f"data/raw/{dataset_name}.csv"
            df.to_csv(filename, index=False)
            print(f"   Saved raw {dataset_name} to {filename}")
    
    # Save analysis-ready data to data/processed folder
    if not analysis_data.empty:
        filename = "data/processed/analysis_ready_data.csv"
        analysis_data.to_csv(filename, index=False)
        print(f"   Saved analysis-ready data to {filename}")
    
    print("   Data saved successfully!")


def main():
    """Main function to demonstrate data collection."""
    try:
        # Collect data
        data = collect_basic_data()
        
        # Process data
        cleaned_data, analysis_data = process_data(data)
        
        # Save data
        save_data(data, analysis_data)
        
        print("\n✓ Tax data collection and processing completed successfully!")
        print(f"\nTo analyze the collected data, run:")
        print(f"python scripts/analysis.py --type oecd --data-file data/processed/analysis_ready_data.csv")
        
        return data, analysis_data
        
    except Exception as e:
        print(f"\n✗ Error during data collection: {e}")
        return None, None


if __name__ == "__main__":
    main() 