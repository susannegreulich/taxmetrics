#!/usr/bin/env python3
"""
Fetch Real OECD Data from SDMX-ML API

This script fetches data from three OECD tables using their SDMX-ML API endpoints,
parses the XML responses with pandasdmx, converts them to pandas DataFrames,
saves them as CSV files for further analysis, and downloads structure queries
for labeling purposes.
"""

import os
import requests
import pandasdmx
import time
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
    'labor_force': 'https://sdmx.oecd.org/public/rest/dataflow/OECD.SDD.TPS/DSD_LFS@DF_IALFS_LF_Q/1.0?references=all'
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
with open("data/raw/tax_revenues.xml", "wb") as f:
    f.write(response1.content)
msg1 = pandasdmx.read_sdmx("data/raw/tax_revenues.xml")
df1 = msg1.to_pandas()
df1.to_csv("data/raw/tax_revenues.csv")
print("Saved as data/raw/tax_revenues.csv")
print(df1.head())

# Add delay between requests to avoid rate limiting
time.sleep(2)

# --- Second Table: National Accounts GDP per capita and PPP ---
print("Fetching Table 2: GDPs...")
url2 = "https://sdmx.oecd.org/public/rest/data/OECD.SDD.NAD,DSD_NAMAIN10@DF_TABLE1,2.0/A..S1...._T..PC+USD_PPP_PS+USD_PPP..G1.T0101?startPeriod=1990&endPeriod=2023&dimensionAtObservation=AllDimensions"
response2 = requests.get(url2, headers=headers)
response2.raise_for_status()
with open("data/raw/gdp.xml", "wb") as f:
    f.write(response2.content)
msg2 = pandasdmx.read_sdmx("data/raw/gdp.xml")
df2 = msg2.to_pandas()
df2.to_csv("data/raw/gdp.csv")
print("Saved as data/raw/gdp.csv")
print(df2.head())

# Add delay between requests to avoid rate limiting
time.sleep(2)

# --- Third Table: Labor Force Statistics (Working-age population) ---
print("Fetching Table 3: Labor Force Populations...")
url3 = "https://sdmx.oecd.org/public/rest/data/OECD.SDD.TPS,DSD_LFS@DF_IALFS_LF_Q,1.0/.LF.._Z.Y._T.Y15T64..A?startPeriod=1990&endPeriod=2023&dimensionAtObservation=AllDimensions"
response3 = requests.get(url3, headers=headers)
response3.raise_for_status()
with open("data/raw/labor_force.xml", "wb") as f:
    f.write(response3.content)
msg3 = pandasdmx.read_sdmx("data/raw/labor_force.xml")
df3 = msg3.to_pandas()
df3.to_csv("data/raw/labor_force.csv")
print("Saved as data/raw/labor_force.csv")
print(df3.head())

print("All data collection completed successfully!")
print("\n" + "=" * 60)
print("Complete Data Collection Process Finished!")
print("=" * 60)
print("Files generated:")
print("- Data CSV files: data/raw/tax_revenues.csv, data/raw/gdp.csv, data/raw/labor_force.csv")
print("- Data XML files: data/raw/tax_revenues.xml, data/raw/gdp.xml, data/raw/labor_force.xml")
print("- Structure XML files: data/raw/tax_revenues_structure.xml, data/raw/gdp_structure.xml, data/raw/labor_force_structure.xml")
print("\nNext step: Run label_data.py to apply labels to the CSV files")
print("=" * 60) 