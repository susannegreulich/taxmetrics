#!/usr/bin/env python3
"""
Download structure queries for each OECD dataset and extract codelists.

This script downloads the specific structure queries for each dataset and then
extracts the relevant codelists from each structure file.
"""

import requests
import xml.etree.ElementTree as ET
import json
from pathlib import Path

# Structure query URLs for each dataset (from todos.md)
STRUCTURE_URLS = {
    'tax_revenues': 'https://sdmx.oecd.org/public/rest/dataflow/OECD.CTP.TPS/DSD_REV_COMP_GLOBAL@DF_RSGLOBAL/2.1?references=all',
    'gdp': 'https://sdmx.oecd.org/public/rest/dataflow/OECD.SDD.NAD/DSD_NAMAIN10@DF_TABLE1/2.0?references=all',
    'labor_force': 'https://sdmx.oecd.org/public/rest/dataflow/OECD.SDD.TPS/DSD_LFS@DF_IALFS_LF_Q/1.0?references=all'
}

# Headers to mimic a browser
headers = {
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
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Save the structure file
        structure_file = Path(f"data/{dataset_name}_structure.xml")
        with open(structure_file, "wb") as f:
            f.write(response.content)
        
        print(f"  Saved to: {structure_file}")
        return structure_file
        
    except Exception as e:
        print(f"  Error downloading structure query for {dataset_name}: {e}")
        return None

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
        'labor_force': [
            'CL_AREA', 'CL_UNIT_MEASURE', 'CL_TRANSFORMATION', 'CL_ADJUSTMENT',
            'CL_SEX', 'CL_AGE', 'CL_FREQ'
        ]
    }
    
    codelists = {}
    relevant_codelists = dataset_codelists.get(dataset_name, [])
    
    for codelist_id in relevant_codelists:
        codes = extract_codelist_from_xml(structure_file, codelist_id)
        if codes:
            # Convert codelist ID to mapping name
            mapping_name = codelist_id.replace('CL_', '')
            codelists[mapping_name] = codes
    
    return codelists

def main():
    """Main function to download structure queries and extract codelists"""
    print("=" * 60)
    print("Downloading Structure Queries and Extracting Codelists")
    print("=" * 60)
    
    # Ensure data directory exists
    Path("data").mkdir(exist_ok=True)
    Path("results").mkdir(exist_ok=True)
    
    all_dataset_mappings = {}
    
    # Download structure queries and extract codelists for each dataset
    for dataset_name, url in STRUCTURE_URLS.items():
        print(f"\n{'='*20} {dataset_name.upper()} {'='*20}")
        
        # Download structure query
        structure_file = download_structure_query(dataset_name, url)
        
        if structure_file and structure_file.exists():
            # Extract codelists for this dataset
            codelists = extract_dataset_codelists(structure_file, dataset_name)
            all_dataset_mappings[dataset_name] = codelists
            
            # Save individual dataset mappings
            output_file = Path(f"results/{dataset_name}_mappings.json")
            with open(output_file, 'w') as f:
                json.dump(codelists, f, indent=2)
            print(f"  Saved {dataset_name} mappings to: {output_file}")
            
            # Print summary for this dataset
            print(f"\n  {dataset_name} Summary:")
            for mapping_name, codes in codelists.items():
                print(f"    {mapping_name}: {len(codes)} codes")
        else:
            print(f"  Skipping {dataset_name} due to download error")
    
    # Save combined mappings
    combined_file = Path("results/all_datasets_mappings.json")
    with open(combined_file, 'w') as f:
        json.dump(all_dataset_mappings, f, indent=2)
    
    print(f"\nSaved combined mappings to: {combined_file}")
    
    # Print final summary
    print("\n" + "=" * 60)
    print("Final Summary:")
    print("=" * 60)
    
    for dataset_name, codelists in all_dataset_mappings.items():
        print(f"\n{dataset_name}:")
        total_codes = sum(len(codes) for codes in codelists.values())
        print(f"  Total mappings: {len(codelists)}")
        print(f"  Total codes: {total_codes}")
        for mapping_name, codes in codelists.items():
            print(f"    {mapping_name}: {len(codes)} codes")
    
    print("\n" + "=" * 60)
    print("Next steps:")
    print("1. Review the extracted mappings in results/")
    print("2. Update label_data.py to use dataset-specific mappings")
    print("3. Test the updated labeling script")
    print("=" * 60)

if __name__ == "__main__":
    main() 