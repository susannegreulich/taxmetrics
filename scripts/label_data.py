#!/usr/bin/env python3
"""
Comprehensive OECD Data Labeling Script

This script performs the complete labeling process:
1. Loads structure queries downloaded by fetch_data.py
2. Extracts codelists from the structure files
3. Applies label mappings to filtered data CSV files in data/processed/

This merges the functionality of:
- extract_codelists.py  
- label_data.py

Note: Structure queries should be downloaded first using fetch_data.py
"""

import xml.etree.ElementTree as ET
import json
import os
import pandas as pd
from pathlib import Path

def extract_codelist_from_xml(xml_file, codelist_id):
    """Extract a specific codelist from the XML structure file"""
    print(f"  Extracting codelist: {codelist_id}")
    
    try:
        # Parse the XML file
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Define namespaces
        namespaces = {
            'structure': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure',
            'common': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common',
            'xml': 'http://www.w3.org/XML/1998/namespace'
        }
        
        # Find the codelist
        codelist = root.find(f'.//structure:Codelist[@id="{codelist_id}"]', namespaces)
        
        if codelist is None:
            print(f"    Codelist {codelist_id} not found")
            return {}
        
        # Extract codes and their names
        codes = {}
        for code in codelist.findall('.//structure:Code', namespaces):
            code_id = code.get('id')
            name_elem = code.find('.//common:Name[@xml:lang="en"]', namespaces)
            
            if name_elem is not None:
                codes[code_id] = name_elem.text
            else:
                codes[code_id] = code_id  # Fallback to code ID if no name found
        
        print(f"    Found {len(codes)} codes")
        return codes
        
    except Exception as e:
        print(f"    Error extracting codelist {codelist_id}: {e}")
        return {}

def extract_dataset_codelists(structure_file, dataset_name):
    """Extract relevant codelists for a specific dataset"""
    print(f"Extracting codelists for {dataset_name}...")
    
    # Define which codelists are relevant for each dataset
    dataset_codelists = {
        'tax_revenues': [
            'CL_AREA', 'CL_STANDARD_REVENUE', 'CL_CTRY_SPECIFIC_REVENUE', 
            'CL_UNIT_MEASURE', 'CL_FREQ', 'CL_SECTOR'
        ],
        'gdp': [
            'CL_AREA', 'CL_SECTOR', 'CL_COUNTERPART_SECTOR', 'CL_INSTR_ASSET',
            'CL_EXPENDITURE', 'CL_UNIT_MEASURE', 'CL_TRANSFORMATION', 
            'CL_TABLEID', 'CL_FREQ', 'CL_TRANSACTION'
        ],
        'population': [
            'CL_AREA', 'CL_UNIT_MEASURE', 'CL_TRANSFORMATION', 'CL_ADJUSTMENT',
            'CL_SEX', 'CL_AGE', 'CL_FREQ'
        ]
    }
    
    # Define mapping from codelist names to CSV column names
    codelist_to_column_mapping = {
        'AREA': 'REF_AREA',
        'STANDARD_REVENUE': 'STANDARD_REVENUE',
        'CTRY_SPECIFIC_REVENUE': 'CTRY_SPECIFIC_REVENUE',
        'UNIT_MEASURE': 'UNIT_MEASURE',
        'FREQ': 'FREQ',
        'SECTOR': 'SECTOR',
        'COUNTERPART_SECTOR': 'COUNTERPART_SECTOR',
        'INSTR_ASSET': 'INSTR_ASSET',
        'EXPENDITURE': 'EXPENDITURE',
        'TRANSFORMATION': 'TRANSFORMATION',
        'TABLEID': 'TABLEID',
        'TRANSACTION': 'TRANSACTION',
        'ADJUSTMENT': 'ADJUSTMENT',
        'SEX': 'SEX',
        'AGE': 'AGE'
    }
    
    codelists = {}
    relevant_codelists = dataset_codelists.get(dataset_name, [])
    
    for codelist_id in relevant_codelists:
        codes = extract_codelist_from_xml(structure_file, codelist_id)
        if codes:
            # Convert codelist ID to mapping name
            mapping_name = codelist_id.replace('CL_', '')
            # Map to the actual column name used in CSV files
            column_name = codelist_to_column_mapping.get(mapping_name, mapping_name)
            codelists[column_name] = codes
    
    return codelists

def load_and_extract_all_mappings():
    """Load existing structure files and extract codelists for all datasets"""
    print("=" * 60)
    print("Step 1: Loading Structure Files and Extracting Codelists")
    print("=" * 60)
    
    # Ensure data/labeled directory exists
    Path("data/labeled").mkdir(parents=True, exist_ok=True)
    
    # Define the datasets and their structure files (now in data/raw)
    datasets = {
        'tax_revenues': 'data/raw/tax_revenues_structure.xml',
        'gdp': 'data/raw/gdp_structure.xml',
        'population': 'data/raw/population_structure.xml'
    }
    
    # Load structure files and extract codelists for each dataset
    for dataset_name, structure_file_path in datasets.items():
        print(f"\n{'='*20} {dataset_name.upper()} {'='*20}")
        
        structure_file = Path(structure_file_path)
        
        if structure_file.exists():
            # Extract codelists for this dataset
            codelists = extract_dataset_codelists(structure_file, dataset_name)
            
            # Save individual dataset mappings
            output_file = Path(f"data/labeled/{dataset_name}_mappings.json")
            with open(output_file, 'w') as f:
                json.dump(codelists, f, indent=2)
            print(f"  Saved {dataset_name} mappings to: {output_file}")
            
            # Print summary for this dataset
            print(f"\n  {dataset_name} Summary:")
            for mapping_name, codes in codelists.items():
                print(f"    {mapping_name}: {len(codes)} codes")
        else:
            print(f"  Structure file not found: {structure_file}")
            print(f"  Please run fetch_data.py first to download structure files")
            return None
    
    print(f"\nAll individual dataset mappings saved to data/labeled/")
    return True

def get_comprehensive_label_mappings():
    """Get optimized fallback label mappings for OECD data (only includes necessary mappings)"""
    print("Loading optimized fallback manual mappings...")
    mappings = {}
    
    # MEASURE mappings - only the codes actually used in the data
    measure_mappings = {
        'TAX_REV': 'Tax revenue',
        'LF': 'Labour force'
    }
    
    # COUNTERPART_SECTOR mappings - only the codes actually used in the data
    counterpart_sector_mappings = {
        'S1': 'Total economy'
    }
    
    # ACTIVITY mappings - only the codes actually used in the data
    activity_mappings = {
        '_Z': 'Not applicable',
        '_T': 'Total',
        'A': 'Agriculture, forestry and fishing',
        'BTE': 'Business services',
        'C': 'Manufacturing',
        'F': 'Construction',
        'GTI': 'Goods and services',
        'J': 'Information and communication',
        'K': 'Financial and insurance activities',
        'L': 'Real estate activities',
        'M_N': 'Professional, scientific and technical activities',
        'OTQ': 'Other activities',
        'RTU': 'Real estate, transport and utilities'
    }
    
    # EXPENDITURE mappings - only the codes actually used in the data
    expenditure_mappings = {
        '_Z': 'Not applicable'
    }
    
    # PRICE_BASE mappings - only the codes actually used in the data
    price_mappings = {
        'L': 'Laspeyres'
    }
    
    # Only include mappings that are actually needed
    mappings['MEASURE'] = measure_mappings
    mappings['COUNTERPART_SECTOR'] = counterpart_sector_mappings
    mappings['ACTIVITY'] = activity_mappings
    mappings['EXPENDITURE'] = expenditure_mappings
    mappings['PRICE_BASE'] = price_mappings
    
    return mappings

def apply_label_mappings(df, mappings, fallback_mappings=None):
    """Apply label mappings to DataFrame columns"""
    df_labeled = df.copy()
    
    # Apply mappings to columns
    for col in df_labeled.columns:
        if col in mappings:
            print(f"    Applying labels to {col}")
            df_labeled[col] = df_labeled[col].map(mappings[col]).fillna(df_labeled[col])
        elif fallback_mappings and col in fallback_mappings:
            print(f"    Applying fallback labels to {col}")
            df_labeled[col] = df_labeled[col].map(fallback_mappings[col]).fillna(df_labeled[col])
    
    return df_labeled

def process_csv_file(input_file, output_file, fallback_mappings):
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
            mappings_to_use = fallback_mappings
            dataset_name = 'unknown'
            print(f"  Using fallback mappings for dataset: {dataset_name}")
        
        # Load dataset-specific mappings if available
        if dataset_name != 'unknown':
            if mapping_file.exists():
                with open(mapping_file, 'r') as f:
                    mappings_to_use = json.load(f)
                print(f"  Loaded mappings for dataset: {dataset_name}")
            else:
                print(f"  Mapping file not found: {mapping_file}")
                mappings_to_use = fallback_mappings
        
        # Apply label mappings
        df_labeled = apply_label_mappings(df, mappings_to_use, fallback_mappings)
        
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
    print("Step 2: Applying Official OECD Labels to CSV Files")
    print("=" * 60)
    
    # Load fallback mappings
    fallback_mappings = get_comprehensive_label_mappings()
    
    # Define the data directory (now looking in data/processed for input files)
    data_dir = Path("data/processed")
    if not data_dir.exists():
        print(f"Error: Data directory {data_dir} does not exist")
        return
    
    # Find all CSV files in the data/processed directory
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
        if process_csv_file(csv_file, output_file, fallback_mappings):
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
    """Main function to perform complete labeling process"""
    print("=" * 80)
    print("OECD Data Labeling Pipeline - Complete Process")
    print("=" * 80)
    
    # Step 1: Load structure files and extract codelists
    success = load_and_extract_all_mappings()
    
    if not success:
        print("\nError: Could not load structure files.")
        print("Please run fetch_data.py first to download the required structure files.")
        return
    
    # Step 2: Apply labels to filtered CSV files
    apply_labels_to_csv_files()
    
    # Final summary
    print("\n" + "=" * 80)
    print("Complete Labeling Process Finished!")
    print("=" * 80)
    print("\nFiles generated:")
    print("- Individual mapping JSON files in data/labeled/")
    print("- Labeled CSV files in data/labeled/")
    print("\nNext steps:")
    print("1. Review the labeled CSV files")
    print("2. Use the labeled data for analysis")
    print("3. Check the mapping files for any missing codes")
    print("=" * 80)

if __name__ == "__main__":
    main() 