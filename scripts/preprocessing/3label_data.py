#!/usr/bin/env python3
"""
OECD Data Labeling Script

This script applies label mappings to filtered data CSV files in data/filtered/.
The mapping files should be created first by running 1fetch_data.py.

This script:
1. Loads the mapping files created by 1fetch_data.py
2. Applies label mappings to filtered data CSV files
3. Saves labeled versions to data/labeled/

Note: Mapping files should be created first using 1fetch_data.py
"""

import json
import os
import pandas as pd
from pathlib import Path

def apply_label_mappings(df, mappings):
    """Apply label mappings to DataFrame columns"""
    df_labeled = df.copy()
    
    # Apply mappings to columns
    for col in df_labeled.columns:
        if col in mappings:
            print(f"    Applying labels to {col}")
            df_labeled[col] = df_labeled[col].map(mappings[col]).fillna(df_labeled[col])
    
    return df_labeled

def process_csv_file(input_file, output_file):
    """Process a single CSV file and apply label mappings"""
    print(f"Processing: {input_file}")
    
    try:
        # Read the CSV file
        df = pd.read_csv(input_file)
        print(f"  Original shape: {df.shape}")
        print(f"  Columns: {list(df.columns)}")
        
        # Determine which mappings to use based on filename
        filename = input_file.name.lower()
        if 'tax' in filename:
            mapping_file = Path("data/labeled/tax_revenues_mappings.json")
            dataset_name = 'tax_revenues'
        elif 'gdp' in filename:
            mapping_file = Path("data/labeled/gdp_mappings.json")
            dataset_name = 'gdp'
        elif 'population' in filename:
            mapping_file = Path("data/labeled/population_mappings.json")
            dataset_name = 'population'
        else:
            print(f"  Unknown dataset type, skipping: {filename}")
            return False
        
        # Load dataset-specific mappings
        if mapping_file.exists():
            with open(mapping_file, 'r') as f:
                mappings_to_use = json.load(f)
            print(f"  Loaded mappings for dataset: {dataset_name}")
        else:
            print(f"  Mapping file not found: {mapping_file}")
            print(f"  Please run 1fetch_data.py first to create mapping files")
            return False
        
        # Apply label mappings
        df_labeled = apply_label_mappings(df, mappings_to_use)
        
        # Save the labeled version
        df_labeled.to_csv(output_file, index=False)
        print(f"  Saved labeled version to: {output_file}")
        
        # Show some examples of the transformation
        print("  Sample transformations:")
        for col in df.columns:
            if col in mappings_to_use and col in ['REF_AREA', 'STANDARD_REVENUE', 'UNIT_MEASURE', 'FREQ', 'SECTOR', 'CTRY_SPECIFIC_REVENUE', 'COUNTERPART_SECTOR', 'SEX', 'AGE']:
                # Show a few examples of the transformation
                original_values = df[col].unique()[:3]  # First 3 unique values
                for val in original_values:
                    if val in mappings_to_use[col]:
                        print(f"    {col}: {val} -> {mappings_to_use[col][val]}")
                    else:
                        print(f"    {col}: {val} -> (no mapping found)")
                break  # Just show one column as example
        
        return True
        
    except Exception as e:
        print(f"  Error processing {input_file}: {e}")
        return False

def apply_labels_to_csv_files():
    """Apply label mappings to all CSV files"""
    print("\n" + "=" * 60)
    print("Applying Official OECD Labels to CSV Files")
    print("=" * 60)
    
    # Define the data directory (looking in data/filtered for input files)
    data_dir = Path("data/filtered")
    if not data_dir.exists():
        print(f"Error: Data directory {data_dir} does not exist")
        print("Please run 2filter_data.py first to create filtered data files")
        return
    
    # Find all CSV files in the data/filtered directory
    csv_files = list(data_dir.glob("*.csv"))
    print(f"\nFound {len(csv_files)} CSV files to process:")
    for file in csv_files:
        print(f"  - {file.name}")
    
    # Process each CSV file
    successful = 0
    failed = 0
    
    for csv_file in csv_files:
        # Skip files that are already labeled
        if "_labeled" in csv_file.name:
            print(f"Skipping already labeled file: {csv_file.name}")
            continue
            
        # Create output filename in the data/labeled directory
        # Remove "_filtered" from the stem if present, then add "_labeled"
        stem = csv_file.stem
        if stem.endswith("_filtered"):
            stem = stem[:-9]  # Remove "_filtered" suffix
        output_file = Path("data/labeled") / f"{stem}_labeled.csv"
        
        # Process the file
        if process_csv_file(csv_file, output_file):
            successful += 1
        else:
            failed += 1
        
        print()  # Add spacing between files
    
    # Summary
    print("=" * 60)
    print("Processing Complete!")
    print(f"Successfully processed: {successful} files")
    print(f"Failed: {failed} files")
    print("=" * 60)
    
    # List all generated files
    print("\nGenerated labeled files:")
    for file in Path("data/labeled").glob("*_labeled.csv"):
        size = file.stat().st_size
        print(f"  {file.name} ({size:,} bytes)")

def main():
    """Main function to perform labeling process"""
    print("=" * 80)
    print("OECD Data Labeling Process")
    print("=" * 80)
    
    # Apply labels to filtered CSV files
    apply_labels_to_csv_files()
    
    # Final summary
    print("\n" + "=" * 80)
    print("Labeling Process Finished!")
    print("=" * 80)
    print("\nFiles generated:")
    print("- Labeled CSV files in data/labeled/")
    print("\nNext steps:")
    print("1. Review the labeled CSV files")
    print("2. Use the labeled data for analysis")
    print("3. Check the mapping files for any missing codes")
    print("=" * 80)

if __name__ == "__main__":
    main() 