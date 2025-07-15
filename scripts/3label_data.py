#!/usr/bin/env python3
"""
OECD Data Labeling Script

This script creates mapping files from OECD structure XML files and applies 
label mappings to filtered data CSV files in data/filtered/.

This script:
1. Creates mapping files from structure XML files (moved from 1fetch_data.py)
2. Loads the mapping files
3. Applies label mappings to filtered data CSV files
4. Saves labeled versions to data/labeled/

Note: Structure XML files should be created first using 1fetch_data.py
"""

import json
import os
import pandas as pd
import xml.etree.ElementTree as ET
from pathlib import Path
import re

# ============================================================================
# MAPPING GENERATION FUNCTIONS (moved from 1fetch_data.py)
# ============================================================================

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

def get_fallback_mappings():
    """Get fallback mappings for missing codelists"""
    fallback_mappings = {}
    
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
        'V': 'Current prices',
        'L': 'Laspeyres'
    }
    
    # UNIT_MEASURE mappings - including codes from dataset_configs.md
    unit_measure_mappings = {
        'PS': 'Persons',
        'USD_PPP': 'US dollars, PPP converted',
        'PT_B1GQ': 'Percentage of GDP'
    }
    
    # SECTOR mappings - including codes from dataset_configs.md
    sector_mappings = {
        'S1': 'Total economy',
        'S13': 'General government'
    }
    
    # TABLE_IDENTIFIER mappings - including codes from dataset_configs.md
    table_identifier_mappings = {
        'T0110': 'Table 0110 - Population and employment',
        'T0102': 'Table 0102 - GDP identity from the expenditure side'
    }
    
    # CTRY_SPECIFIC_REVENUE mappings - including codes from dataset_configs.md
    ctry_specific_revenue_mappings = {
        '_T': 'Total'
    }
    
    # FREQ mappings - including codes from dataset_configs.md
    freq_mappings = {
        'A': 'Annual'
    }
    
    # TRANSFORMATION mappings - including codes from dataset_configs.md
    transformation_mappings = {
        'N': 'Non transformed data'
    }
    
    # INSTR_ASSET mappings - including codes from dataset_configs.md
    instr_asset_mappings = {
        '_Z': 'Not applicable'
    }
    
    # TRANSACTION mappings - including codes from dataset_configs.md
    transaction_mappings = {
        'POP': 'Total population',
        'B1GQ': 'Gross domestic product'
    }
    
    fallback_mappings['MEASURE'] = measure_mappings
    fallback_mappings['COUNTERPART_SECTOR'] = counterpart_sector_mappings
    fallback_mappings['ACTIVITY'] = activity_mappings
    fallback_mappings['EXPENDITURE'] = expenditure_mappings
    fallback_mappings['PRICE_BASE'] = price_mappings
    fallback_mappings['UNIT_MEASURE'] = unit_measure_mappings
    fallback_mappings['SECTOR'] = sector_mappings
    fallback_mappings['TABLE_IDENTIFIER'] = table_identifier_mappings
    fallback_mappings['CTRY_SPECIFIC_REVENUE'] = ctry_specific_revenue_mappings
    fallback_mappings['FREQ'] = freq_mappings
    fallback_mappings['TRANSFORMATION'] = transformation_mappings
    fallback_mappings['INSTR_ASSET'] = instr_asset_mappings
    fallback_mappings['TRANSACTION'] = transaction_mappings
    
    return fallback_mappings

def extract_dataset_codelists(structure_file, dataset_name):
    """Extract relevant codelists for a specific dataset"""
    print(f"Extracting codelists for {dataset_name}...")
    
    # Define which codelists are relevant for each dataset
    dataset_codelists = {
        'tax_revenues': [
            'CL_AREA', 'CL_STANDARD_REVENUE', 'CL_CTRY_SPECIFIC_REVENUE', 
            'CL_UNIT_MEASURE', 'CL_FREQ', 'CL_SECTOR', 'CL_MEASURE'
        ],
        'gdp': [
            'CL_AREA', 'CL_SECTOR', 'CL_COUNTERPART_SECTOR', 'CL_INSTR_ASSET',
            'CL_EXPENDITURE', 'CL_UNIT_MEASURE', 'CL_TRANSFORMATION', 
            'CL_TABLEID', 'CL_FREQ', 'CL_TRANSACTION', 'CL_ACTIVITY', 'CL_PRICE_BASE'
        ],
        'population': [
            'CL_AREA', 'CL_UNIT_MEASURE', 'CL_TRANSFORMATION', 'CL_ADJUSTMENT',
            'CL_SEX', 'CL_AGE', 'CL_FREQ', 'CL_SECTOR', 'CL_COUNTERPART_SECTOR', 
            'CL_TRANSACTION', 'CL_INSTR_ASSET', 'CL_ACTIVITY', 'CL_EXPENDITURE', 
            'CL_PRICE_BASE', 'CL_TABLEID'
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
        'TABLEID': 'TABLE_IDENTIFIER',
        'TRANSACTION': 'TRANSACTION',
        'ADJUSTMENT': 'ADJUSTMENT',
        'SEX': 'SEX',
        'AGE': 'AGE',
        'MEASURE': 'MEASURE',
        'ACTIVITY': 'ACTIVITY',
        'PRICE_BASE': 'PRICE_BASE'
    }
    
    # Get fallback mappings for missing codelists
    fallback_mappings = get_fallback_mappings()
    
    codelists = {}
    relevant_codelists = dataset_codelists.get(dataset_name, [])
    
    for codelist_id in relevant_codelists:
        codes = extract_codelist_from_xml(structure_file, codelist_id)
        
        # Convert codelist ID to mapping name
        mapping_name = codelist_id.replace('CL_', '')
        # Map to the actual column name used in CSV files
        column_name = codelist_to_column_mapping.get(mapping_name, mapping_name)
        
        # If no codes found in XML, use fallback mappings
        if not codes and column_name in fallback_mappings:
            print(f"    Using fallback mappings for {column_name}")
            codes = fallback_mappings[column_name]
        
        # Add/override special mappings for Population and GDP
        if dataset_name in ('population', 'gdp'):
            # Always ensure _Z is present
            if '_Z' not in codes:
                codes['_Z'] = 'Not applicable'
            # Always ensure S1 is present
            if 'S1' not in codes:
                codes['S1'] = 'Total economy'
            # Always ensure V is present
            if 'V' not in codes:
                codes['V'] = 'Current prices'
        
        if codes:
            codelists[column_name] = codes
    
    return codelists

def create_mapping_files():
    """Create mapping files for all datasets"""
    print("\n" + "=" * 60)
    print("Creating Mapping Files for Data Labeling")
    print("=" * 60)
    
    # Ensure data/labeled directory exists
    Path("data/labeled").mkdir(parents=True, exist_ok=True)
    
    # Define the datasets and their structure files
    datasets = {
        'tax_revenues': 'data/raw/tax_revenues_structure.xml',
        'gdp': 'data/raw/gdp_structure.xml',
        'population': 'data/raw/population_structure.xml'
    }
    
    # Create mapping files for each dataset
    for dataset_name, structure_file_path in datasets.items():
        print(f"\n{'='*20} {dataset_name.upper()} {'='*20}")
        
        structure_file = Path(structure_file_path)
        
        if structure_file.exists():
            # Extract codelists for this dataset
            codelists = extract_dataset_codelists(structure_file, dataset_name)
            
            # Save individual dataset mappings to data/labeled
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
            print(f"  Skipping mapping creation for {dataset_name}")
    
    print(f"\nAll mapping files saved to data/labeled/")

# ============================================================================
# LABELING FUNCTIONS FOR 2D DATA STRUCTURE
# ============================================================================

def extract_country_code_from_column(column_name):
    """Extract country code from column name"""
    # For the new tax revenues structure: column names are just country codes (ARG, AUS, etc.)
    # For GDP and population: pattern is just COUNTRYCODE
    return column_name

def apply_country_labels_to_columns(df, country_mappings):
    """Apply country name labels to DataFrame column headers"""
    df_labeled = df.copy()
    
    # Create new column names mapping
    new_columns = {}
    
    for col in df.columns:
        if col in ['TIME_PERIOD', 'STANDARD_REVENUE']:
            new_columns[col] = col  # Keep time period and standard revenue as is
        else:
            # Extract country code from column name
            country_code = extract_country_code_from_column(col)
            
            # Get country name from mappings
            if country_code in country_mappings:
                country_name = country_mappings[country_code]
                new_columns[col] = country_name
                print(f"    {col} -> {country_name}")
            else:
                # Keep original if no mapping found
                new_columns[col] = col
                print(f"    {col} -> (no mapping found)")
    
    # Rename columns
    df_labeled.columns = [new_columns[col] for col in df.columns]
    
    return df_labeled

def apply_revenue_category_labels(df, revenue_mappings):
    """Apply revenue category labels to STANDARD_REVENUE column values"""
    df_labeled = df.copy()
    
    if 'STANDARD_REVENUE' in df.columns and revenue_mappings:
        # Create a mapping for the revenue categories
        revenue_labels = {}
        for code, label in revenue_mappings.items():
            revenue_labels[code] = label
        
        # Replace the original STANDARD_REVENUE column values with labels
        df_labeled['STANDARD_REVENUE'] = df_labeled['STANDARD_REVENUE'].map(revenue_labels)
        
        # Show some examples of the transformation
        print("  Sample revenue category transformations:")
        unique_revenues = df['STANDARD_REVENUE'].unique()[:5]  # First 5 unique values from original
        for revenue in unique_revenues:
            if revenue in revenue_labels:
                print(f"    {revenue} -> {revenue_labels[revenue]}")
            else:
                print(f"    {revenue} -> (no mapping found)")
    
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
            print(f"  Mapping files should be created automatically by this script")
            print(f"  Please ensure structure XML files exist in data/raw/")
            return False
        
        # Apply country name labels to column headers
        if 'REF_AREA' in mappings_to_use:
            print(f"  Applying country name labels to column headers...")
            df_labeled = apply_country_labels_to_columns(df, mappings_to_use['REF_AREA'])
        else:
            print(f"  No REF_AREA mappings found, keeping original column names")
            df_labeled = df
        
        # Apply revenue category labels to STANDARD_REVENUE column values
        if 'STANDARD_REVENUE' in mappings_to_use:
            print(f"  Applying revenue category labels to STANDARD_REVENUE column...")
            df_labeled = apply_revenue_category_labels(df_labeled, mappings_to_use['STANDARD_REVENUE'])
        else:
            print(f"  No STANDARD_REVENUE mappings found, skipping revenue category labeling")
        
        # Save the labeled version
        df_labeled.to_csv(output_file, index=False)
        print(f"  Saved labeled version to: {output_file}")
        
        # Show some examples of the transformation
        print("  Sample column transformations:")
        original_cols = df.columns[:5]  # First 5 columns
        for col in original_cols:
            if col not in ['TIME_PERIOD', 'STANDARD_REVENUE']:
                country_code = extract_country_code_from_column(col)
                if 'REF_AREA' in mappings_to_use and country_code in mappings_to_use['REF_AREA']:
                    print(f"    {col} -> {mappings_to_use['REF_AREA'][country_code]}")
                else:
                    print(f"    {col} -> (no mapping found)")
        
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
        print("Note: This script will create mapping files automatically")
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

def apply_labels_to_dataset_configs_csv():
    """Apply label mappings to the dataset_configs.csv file"""
    print("\n" + "=" * 60)
    print("Applying Labels to Dataset Configurations CSV")
    print("=" * 60)
    
    config_file = Path("data/dataset_configs.csv")
    if not config_file.exists():
        print(f"Dataset configs file not found: {config_file}")
        print("Skipping dataset configs CSV processing")
        return
    
    print(f"Processing: {config_file}")
    
    try:
        # Read the CSV file
        df = pd.read_csv(config_file)
        print(f"  Original shape: {df.shape}")
        print(f"  Columns: {list(df.columns)}")
        
        # Load all mapping files
        mappings = {}
        for dataset in ['tax_revenues', 'gdp', 'population']:
            mapping_file = Path(f"data/labeled/{dataset}_mappings.json")
            if mapping_file.exists():
                with open(mapping_file, 'r') as f:
                    mappings[dataset] = json.load(f)
                print(f"  Loaded mappings for {dataset}")
            else:
                print(f"  Warning: Mapping file not found for {dataset}")
        
        # Create a new column for labels
        df['Label'] = ''
        
        # Apply mappings to each row
        for idx, row in df.iterrows():
            dataset = row['Dataset']
            column = row['Deleted_Column']
            value = row['Single_Unique_Value']
            
            # Map dataset name to mapping key
            dataset_mapping_key = {
                'Population': 'population',
                'GDP': 'gdp', 
                'Tax Revenues': 'tax_revenues'
            }.get(dataset)
            
            if dataset_mapping_key and dataset_mapping_key in mappings:
                dataset_mappings = mappings[dataset_mapping_key]
                if column in dataset_mappings and value in dataset_mappings[column]:
                    df.at[idx, 'Label'] = dataset_mappings[column][value]
                    print(f"    {dataset} - {column}: {value} -> {dataset_mappings[column][value]}")
                else:
                    print(f"    {dataset} - {column}: {value} -> (no mapping found)")
            else:
                print(f"    {dataset} - {column}: {value} -> (no dataset mapping found)")
        
        # Overwrite the original CSV file
        df.to_csv(config_file, index=False)
        print(f"  Overwrote labeled version to: {config_file}")
        
        # Show summary of the transformation
        print(f"\n  Summary:")
        print(f"    Total rows: {len(df)}")
        print(f"    Rows with labels: {len(df[df['Label'] != ''])}")
        print(f"    Rows without labels: {len(df[df['Label'] == ''])}")
        
        return True
        
    except Exception as e:
        print(f"  Error processing dataset configs CSV: {e}")
        return False

def main():
    """Main function to perform labeling process"""
    print("=" * 80)
    print("OECD Data Labeling Process")
    print("=" * 80)
    
    # First, create mapping files from structure XML files
    create_mapping_files()
    
    # Then apply labels to filtered CSV files
    apply_labels_to_csv_files()
    
    # Apply labels to dataset_configs.csv
    apply_labels_to_dataset_configs_csv()
    
    # Final summary
    print("\n" + "=" * 80)
    print("Labeling Process Finished!")
    print("=" * 80)
    print("\nFiles generated:")
    print("- Mapping JSON files in data/labeled/")
    print("- Labeled CSV files in data/labeled/")
    print("- Labeled dataset_configs_labeled.csv in data/")
    print("\nNext steps:")
    print("1. Review the labeled CSV files")
    print("2. Use the labeled data for analysis")
    print("3. Check the mapping files for any missing codes")
    print("4. Review the labeled dataset_configs_labeled.csv file")
    print("=" * 80)

if __name__ == "__main__":
    main() 