#!/usr/bin/env python3
"""
Process OECD CSV files downloaded manually from OECD Data Explorer

This script loads CSV files that you download manually from the OECD Data Explorer,
cleans and standardizes them, and saves them in a consistent format for analysis.

Instructions:
1. Go to each OECD table in your browser
2. Click "Download" → "CSV" 
3. Save the files in the data/raw/ directory
4. Run this script to process them
"""

import os
import pandas as pd
import glob

# Ensure the data directory exists
os.makedirs("data", exist_ok=True)
os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

def process_csv_file(file_path, output_name):
    """Process a CSV file and save it in a standardized format"""
    print(f"Processing {file_path}...")
    
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Print basic info
        print(f"  Shape: {df.shape}")
        print(f"  Columns: {list(df.columns)}")
        print(f"  First few rows:")
        print(df.head())
        
        # Save to processed directory
        output_path = f"data/processed/{output_name}.csv"
        df.to_csv(output_path, index=False)
        print(f"  Saved as {output_path}")
        
        return df
        
    except Exception as e:
        print(f"  Error processing {file_path}: {e}")
        return None

def main():
    print("OECD CSV Data Processor")
    print("=" * 50)
    
    # Look for CSV files in the raw directory
    csv_files = glob.glob("data/raw/*.csv")
    
    if not csv_files:
        print("No CSV files found in data/raw/")
        print("\nTo use this script:")
        print("1. Download CSV files from OECD Data Explorer")
        print("2. Save them in data/raw/ directory")
        print("3. Run this script again")
        return
    
    print(f"Found {len(csv_files)} CSV file(s):")
    for i, file_path in enumerate(csv_files, 1):
        filename = os.path.basename(file_path)
        print(f"  {i}. {filename}")
    
    print("\nProcessing files...")
    
    # Process each file
    for i, file_path in enumerate(csv_files, 1):
        filename = os.path.basename(file_path)
        name_without_ext = os.path.splitext(filename)[0]
        
        # Create a standardized name
        if "tax" in filename.lower() or "revenue" in filename.lower():
            output_name = f"oecd_tax_data_{i}"
        elif "gdp" in filename.lower() or "national" in filename.lower():
            output_name = f"oecd_gdp_data_{i}"
        elif "labor" in filename.lower() or "population" in filename.lower():
            output_name = f"oecd_labor_data_{i}"
        else:
            output_name = f"oecd_data_{i}"
        
        df = process_csv_file(file_path, output_name)
        
        if df is not None:
            print(f"  ✓ Successfully processed {filename}")
        else:
            print(f"  ✗ Failed to process {filename}")
        
        print()
    
    print("Processing complete!")
    print("\nProcessed files are saved in data/processed/")
    print("You can now use these files for your analysis.")

if __name__ == "__main__":
    main() 