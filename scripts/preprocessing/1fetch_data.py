#!/usr/bin/env python3
"""
Fetch Real OECD Data from SDMX-ML API

This script fetches data from three OECD tables using their SDMX-ML API endpoints,
parses the XML responses with pandasdmx, converts them to pandas DataFrames,
saves them as CSV files for further analysis, downloads structure queries
for labeling purposes, and creates mapping files for data labeling.
"""

import os
import requests
import pandasdmx
import time
import xml.etree.ElementTree as ET
import json
from pathlib import Path

# Ensure the data/raw directory exists
os.makedirs("data/raw", exist_ok=True)

# Set up headers to mimic a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/vnd.sdmx.genericdata+xml; charset=utf-8; version=2.1',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# Structure query URLs for each dataset
STRUCTURE_URLS = {
    'tax_revenues': 'https://sdmx.oecd.org/public/rest/dataflow/OECD.CTP.TPS/DSD_REV_COMP_GLOBAL@DF_RSGLOBAL/2.1?references=all',
    'gdp': 'https://sdmx.oecd.org/public/rest/dataflow/OECD.SDD.NAD/DSD_NAMAIN10@DF_TABLE1/2.0?references=all',
    'population': 'https://sdmx.oecd.org/public/rest/dataflow/OECD.SDD.NAD/DSD_NAMAIN10@DF_TABLE3/2.0?references=all'
}

# Headers for structure queries
structure_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/vnd.sdmx.structure+xml; charset=utf-8; version=2.1',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

def download_structure_query(dataset_name, url):
    """Download structure query for a specific dataset"""
    print(f"Downloading structure query for {dataset_name}...")
    
    try:
        response = requests.get(url, headers=structure_headers)
        response.raise_for_status()
        
        # Save the structure file in data/raw subfolder
        structure_file = Path(f"data/raw/{dataset_name}_structure.xml")
        with open(structure_file, "wb") as f:
            f.write(response.content)
        
        print(f"  Saved to: {structure_file}")
        return structure_file
        
    except Exception as e:
        print(f"  Error downloading structure query for {dataset_name}: {e}")
        return None

def download_all_structure_queries():
    """Download structure queries for all datasets"""
    print("\n" + "=" * 60)
    print("Downloading Structure Queries for Labeling")
    print("=" * 60)
    
    for dataset_name, url in STRUCTURE_URLS.items():
        download_structure_query(dataset_name, url)
        time.sleep(1)  # Small delay between requests
    
    print("Structure queries download completed!")

# Download structure queries for labeling
download_all_structure_queries()

# Data queries for each dataset

# --- First Table: Tax Revenues 1990-2023
print("Fetching Table 1: Tax Revenues...")
url1 = "https://sdmx.oecd.org/public/rest/data/OECD.CTP.TPS,DSD_REV_COMP_GLOBAL@DF_RSGLOBAL,2.1/..S13.T_5000+T_4000+T_2000+T_1000+_T..PT_B1GQ.A?startPeriod=1990&endPeriod=2023&dimensionAtObservation=AllDimensions"
response1 = requests.get(url1, headers=headers)
response1.raise_for_status()
with open("data/raw/tax_revenues_data.xml", "wb") as f:
    f.write(response1.content)
msg1 = pandasdmx.read_sdmx("data/raw/tax_revenues_data.xml")
df1 = msg1.to_pandas()
df1.to_csv("data/raw/tax_revenues_raw.csv")
print("Saved as data/raw/tax_revenues_raw.csv")
print(df1.head())

# Add delay between requests to avoid rate limiting
time.sleep(2)

# --- Second Table: National Accounts GDP per capita and PPP ---
print("Fetching Table 2: GDPs...")
url2 = "https://sdmx.oecd.org/public/rest/data/OECD.SDD.NAD,DSD_NAMAIN10@DF_TABLE1,2.0/A..S1..B1GQ._Z._Z._Z.USD_PPP.V.N.T0102?startPeriod=1990&endPeriod=2023&dimensionAtObservation=AllDimensions"
response2 = requests.get(url2, headers=headers)
response2.raise_for_status()
with open("data/raw/gdp_data.xml", "wb") as f:
    f.write(response2.content)
msg2 = pandasdmx.read_sdmx("data/raw/gdp_data.xml")
df2 = msg2.to_pandas()
df2.to_csv("data/raw/gdp_raw.csv")
print("Saved as data/raw/gdp_raw.csv")
print(df2.head())

# Add delay between requests to avoid rate limiting
time.sleep(2)

# --- Third Table: Population Statistics ---
print("Fetching Table 3: Population...")
url3 = "https://sdmx.oecd.org/public/rest/data/OECD.SDD.NAD,DSD_NAMAIN10@DF_TABLE3,2.0/A..S1.S1.POP.._Z..PS...?startPeriod=1990&endPeriod=2023&dimensionAtObservation=AllDimensions"
response3 = requests.get(url3, headers=headers)
response3.raise_for_status()
with open("data/raw/population_data.xml", "wb") as f:
    f.write(response3.content)
msg3 = pandasdmx.read_sdmx("data/raw/population_data.xml")
df3 = msg3.to_pandas()
df3.to_csv("data/raw/population_raw.csv")
print("Saved as data/raw/population_raw.csv")
print(df3.head())

print("All data collection completed successfully!")

# Create mapping files for data labeling
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
    """Get fallback mappings for missing codelists from 3label_data.py"""
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
    
    fallback_mappings['MEASURE'] = measure_mappings
    fallback_mappings['COUNTERPART_SECTOR'] = counterpart_sector_mappings
    fallback_mappings['ACTIVITY'] = activity_mappings
    fallback_mappings['EXPENDITURE'] = expenditure_mappings
    fallback_mappings['PRICE_BASE'] = price_mappings
    
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

# Create mapping files
create_mapping_files()

print("\n" + "=" * 60)
print("Complete Data Collection Process Finished!")
print("=" * 60)
print("Files generated:")
print("- Data CSV files: data/raw/tax_revenues_raw.csv, data/raw/gdp_raw.csv, data/raw/population_raw.csv")
print("- Data XML files: data/raw/tax_revenues_data.xml, data/raw/gdp_data.xml, data/raw/population_data.xml")
print("- Structure XML files: data/raw/tax_revenues_structure.xml, data/raw/gdp_structure.xml, data/raw/population_structure.xml")
print("- Mapping JSON files: data/labeled/tax_revenues_mappings.json, data/labeled/gdp_mappings.json, data/labeled/population_mappings.json")
print("\nNext step: Run 2filter_data.py to filter and clean the data")
print("=" * 60) 