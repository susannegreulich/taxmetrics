#!/usr/bin/env python3
"""
Fetch OECD data with identifiers and apply comprehensive label mappings.

This script fetches OECD data using the simple JSON format and applies
pre-defined label mappings to make the data human-readable.
"""

import os
import requests
import pandas as pd
import time
import random
import sys
import json

def make_request_with_retry(url, max_retries=5, base_delay=10):
    """Make HTTP request with retry logic and exponential backoff"""
    for attempt in range(max_retries):
        try:
            print(f"Making request to {url} (attempt {attempt + 1}/{max_retries})")
            response = requests.get(url)
            
            if response.status_code == 429:
                # Rate limited - wait much longer
                delay = base_delay * (3 ** attempt) + random.uniform(5, 15)
                print(f"Rate limited (429). Waiting {delay:.1f} seconds before retry...")
                time.sleep(delay)
                continue
            elif response.status_code >= 500:
                # Server error - retry with exponential backoff
                delay = base_delay * (2 ** attempt) + random.uniform(1, 3)
                print(f"Server error ({response.status_code}). Waiting {delay:.1f} seconds before retry...")
                time.sleep(delay)
                continue
            else:
                response.raise_for_status()
                return response
                
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise e
            delay = base_delay * (2 ** attempt) + random.uniform(1, 3)
            print(f"Request failed: {e}. Waiting {delay:.1f} seconds before retry...")
            time.sleep(delay)
    
    raise requests.exceptions.RequestException(f"Failed after {max_retries} attempts")

def get_comprehensive_label_mappings():
    """Get comprehensive label mappings for OECD data"""
    mappings = {}
    
    # Country mappings (REF_AREA) - Major OECD and non-OECD countries
    country_mappings = {
        # OECD Countries
        'AUS': 'Australia', 'AUT': 'Austria', 'BEL': 'Belgium', 'CAN': 'Canada',
        'CHE': 'Switzerland', 'CHL': 'Chile', 'COL': 'Colombia', 'CZE': 'Czech Republic',
        'DNK': 'Denmark', 'EST': 'Estonia', 'FIN': 'Finland', 'FRA': 'France',
        'DEU': 'Germany', 'GRC': 'Greece', 'HUN': 'Hungary', 'ISL': 'Iceland',
        'IRL': 'Ireland', 'ISR': 'Israel', 'ITA': 'Italy', 'JPN': 'Japan',
        'KOR': 'Korea', 'LVA': 'Latvia', 'LTU': 'Lithuania', 'LUX': 'Luxembourg',
        'MEX': 'Mexico', 'NLD': 'Netherlands', 'NZL': 'New Zealand', 'NOR': 'Norway',
        'POL': 'Poland', 'PRT': 'Portugal', 'SVK': 'Slovak Republic', 'SVN': 'Slovenia',
        'ESP': 'Spain', 'SWE': 'Sweden', 'TUR': 'Turkey', 'GBR': 'United Kingdom',
        'USA': 'United States',
        
        # Major Non-OECD Countries
        'ARG': 'Argentina', 'BRA': 'Brazil', 'CHN': 'China', 'CRI': 'Costa Rica',
        'IND': 'India', 'IDN': 'Indonesia', 'PER': 'Peru', 'RUS': 'Russian Federation',
        'ZAF': 'South Africa', 'THA': 'Thailand', 'VNM': 'Vietnam',
        
        # Regional Aggregates
        'OECD': 'OECD Total', 'OECD_REP': 'OECD Representative Countries',
        'EU27_2020': 'European Union (27 countries)', 'EU15': 'European Union (15 countries)',
        'EA20': 'Euro Area (20 countries)', 'G20': 'G20 Countries',
        
        # Other Countries
        'AZE': 'Azerbaijan', 'BGR': 'Bulgaria', 'HRV': 'Croatia', 'CYP': 'Cyprus',
        'GEO': 'Georgia', 'HKG': 'Hong Kong', 'KAZ': 'Kazakhstan', 'MDA': 'Moldova',
        'MNE': 'Montenegro', 'MKD': 'North Macedonia', 'ROU': 'Romania', 'SRB': 'Serbia',
        'UKR': 'Ukraine', 'ALB': 'Albania', 'ARM': 'Armenia', 'ATG': 'Antigua and Barbuda',
        'BHS': 'Bahamas', 'BRB': 'Barbados', 'BLZ': 'Belize', 'BOL': 'Bolivia',
        'BTN': 'Bhutan', 'BWA': 'Botswana', 'BFA': 'Burkina Faso', 'BGD': 'Bangladesh',
        'CIV': "Côte d'Ivoire", 'CMR': 'Cameroon', 'COD': 'Democratic Republic of the Congo',
        'COG': 'Republic of the Congo', 'COK': 'Cook Islands', 'CPV': 'Cape Verde',
        'CUB': 'Cuba', 'DOM': 'Dominican Republic', 'ECU': 'Ecuador', 'EGY': 'Egypt',
        'FJI': 'Fiji', 'GAB': 'Gabon', 'GHA': 'Ghana', 'GIN': 'Guinea', 'GNQ': 'Equatorial Guinea',
        'GTM': 'Guatemala', 'GUY': 'Guyana', 'HND': 'Honduras', 'JAM': 'Jamaica',
        'KEN': 'Kenya', 'KGZ': 'Kyrgyzstan', 'KHM': 'Cambodia', 'KIR': 'Kiribati',
        'LAO': 'Lao People\'s Democratic Republic', 'LCA': 'Saint Lucia', 'LIE': 'Liechtenstein',
        'LKA': 'Sri Lanka', 'LSO': 'Lesotho', 'MAR': 'Morocco', 'MDG': 'Madagascar',
        'MDV': 'Maldives', 'MHL': 'Marshall Islands', 'MLI': 'Mali', 'MLT': 'Malta',
        'MNG': 'Mongolia', 'MOZ': 'Mozambique', 'MRT': 'Mauritania', 'MUS': 'Mauritius',
        'MWI': 'Malawi', 'MYS': 'Malaysia', 'NAM': 'Namibia', 'NER': 'Niger',
        'NGA': 'Nigeria', 'NIC': 'Nicaragua', 'NIU': 'Niue', 'NRU': 'Nauru',
        'PAK': 'Pakistan', 'PAN': 'Panama', 'PHL': 'Philippines', 'PNG': 'Papua New Guinea',
        'PRY': 'Paraguay', 'RWA': 'Rwanda', 'SEN': 'Senegal', 'SGP': 'Singapore',
        'SLB': 'Solomon Islands', 'SLE': 'Sierra Leone', 'SLV': 'El Salvador',
        'SOM': 'Somalia', 'SWZ': 'Eswatini', 'SYC': 'Seychelles', 'TCD': 'Chad',
        'TGO': 'Togo', 'TKL': 'Tokelau', 'TLS': 'Timor-Leste', 'TTO': 'Trinidad and Tobago',
        'TUN': 'Tunisia', 'UGA': 'Uganda', 'URY': 'Uruguay', 'VEN': 'Venezuela',
        'VUT': 'Vanuatu', 'WSM': 'Samoa', 'ZMB': 'Zambia'
    }
    
    # Tax category mappings (STANDARD_REVENUE)
    tax_mappings = {
        '_T': 'Total tax revenue',
        'T_1000': 'Taxes on income, profits and capital gains',
        'T_1100': 'Taxes on income, profits and capital gains of individuals',
        'T_1110': 'Taxes on income, profits and capital gains of individuals',
        'T_1120': 'Taxes on income, profits and capital gains of individuals',
        'T_1200': 'Taxes on income, profits and capital gains of corporations',
        'T_1210': 'Taxes on income, profits and capital gains of corporations',
        'T_1220': 'Taxes on income, profits and capital gains of corporations',
        'T_1300': 'Taxes on income, profits and capital gains',
        'T_2000': 'Social security contributions',
        'T_2100': 'Social security contributions paid by employees',
        'T_2110': 'Social security contributions paid by employees',
        'T_2120': 'Social security contributions paid by employees',
        'T_2200': 'Social security contributions paid by employers',
        'T_2210': 'Social security contributions paid by employers',
        'T_2220': 'Social security contributions paid by employers',
        'T_2300': 'Social security contributions paid by self-employed or non-employed',
        'T_2310': 'Social security contributions paid by self-employed or non-employed',
        'T_2320': 'Social security contributions paid by self-employed or non-employed',
        'T_2400': 'Social security contributions',
        'T_2410': 'Social security contributions',
        'T_2420': 'Social security contributions',
        'T_3000': 'Taxes on payroll and workforce',
        'T_4000': 'Taxes on property',
        'T_4100': 'Recurrent taxes on immovable property',
        'T_4110': 'Recurrent taxes on immovable property',
        'T_4120': 'Recurrent taxes on immovable property',
        'T_4200': 'Recurrent taxes on net wealth',
        'T_4210': 'Recurrent taxes on net wealth',
        'T_4220': 'Recurrent taxes on net wealth',
        'T_4300': 'Estate, inheritance and gift taxes',
        'T_4310': 'Estate, inheritance and gift taxes',
        'T_4320': 'Estate, inheritance and gift taxes',
        'T_4400': 'Taxes on financial and capital transactions',
        'T_4500': 'Non-recurrent taxes',
        'T_4510': 'Non-recurrent taxes',
        'T_4520': 'Non-recurrent taxes',
        'T_4600': 'Other recurrent taxes on property',
        'T_5000': 'Taxes on goods and services',
        'T_5100': 'Taxes on production, sale, transfer, leasing and delivery of goods and rendering of services',
        'T_5110': 'Taxes on production, sale, transfer, leasing and delivery of goods and rendering of services',
        'T_5111': 'Taxes on production, sale, transfer, leasing and delivery of goods and rendering of services',
        'T_5112': 'Taxes on production, sale, transfer, leasing and delivery of goods and rendering of services',
        'T_5113': 'Taxes on production, sale, transfer, leasing and delivery of goods and rendering of services',
        'T_5120': 'Taxes on production, sale, transfer, leasing and delivery of goods and rendering of services',
        'T_5121': 'Taxes on production, sale, transfer, leasing and delivery of goods and rendering of services',
        'T_5122': 'Taxes on production, sale, transfer, leasing and delivery of goods and rendering of services',
        'T_5123': 'Taxes on production, sale, transfer, leasing and delivery of goods and rendering of services',
        'T_5124': 'Taxes on production, sale, transfer, leasing and delivery of goods and rendering of services',
        'T_5125': 'Taxes on production, sale, transfer, leasing and delivery of goods and rendering of services',
        'T_5126': 'Taxes on production, sale, transfer, leasing and delivery of goods and rendering of services',
        'T_5127': 'Taxes on production, sale, transfer, leasing and delivery of goods and rendering of services',
        'T_5128': 'Taxes on production, sale, transfer, leasing and delivery of goods and rendering of services',
        'T_5130': 'Taxes on production, sale, transfer, leasing and delivery of goods and rendering of services',
        'T_5200': 'Taxes on use of goods and on permission to use goods or perform activities',
        'T_5210': 'Taxes on use of goods and on permission to use goods or perform activities',
        'T_5211': 'Taxes on use of goods and on permission to use goods or perform activities',
        'T_5212': 'Taxes on use of goods and on permission to use goods or perform activities',
        'T_5213': 'Taxes on use of goods and on permission to use goods or perform activities',
        'T_5220': 'Taxes on use of goods and on permission to use goods or perform activities',
        'T_5300': 'Taxes on extraction, production or use of natural resources',
        'T_6000': 'Other taxes',
        'T_6100': 'Other taxes',
        'T_6200': 'Other taxes',
        'T_CUS': 'Customs and import duties'
    }
    
    # Unit measure mappings (UNIT_MEASURE)
    unit_mappings = {
        'PT_B1GQ': 'Percentage of GDP',
        'PT_OTR_SECTOR': 'Percentage of other sector',
        'USD': 'US Dollars',
        'XDC': 'National currency',
        'IX': 'Index',
        'USD_EXC': 'US Dollars (exchange rate)'
    }
    
    # Frequency mappings (FREQ)
    freq_mappings = {
        'A': 'Annual',
        'Q': 'Quarterly',
        'M': 'Monthly'
    }
    
    # Sector mappings (SECTOR)
    sector_mappings = {
        'S1': 'Total economy',
        'S13': 'General government',
        'S1311': 'Central government',
        'S1312': 'State government',
        'S1313': 'Local government',
        'S1314': 'Social security funds',
        'S1315': 'General government (excluding social security)'
    }
    
    # Measure mappings (MEASURE)
    measure_mappings = {
        'TAX_REV': 'Tax revenue',
        'B1G': 'Gross domestic product',
        'B1GQ': 'Gross domestic product',
        'LF': 'Labour force',
        'LI': 'Labour input'
    }
    
    # Transaction mappings (TRANSACTION)
    transaction_mappings = {
        'B1G': 'Gross domestic product',
        'B1GQ': 'Gross domestic product',
        'B1GXP119': 'Gross domestic product',
        'D21': 'Taxes on products',
        'D21X31': 'Taxes on products',
        'D31': 'Compensation of employees',
        'YA1': 'Gross value added'
    }
    
    # Activity mappings (ACTIVITY)
    activity_mappings = {
        '_T': 'Total',
        '_Z': 'Not applicable',
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
    
    # Price base mappings (PRICE_BASE)
    price_mappings = {
        'DR': 'Deflator',
        'L': 'Laspeyres',
        'LR': 'Laspeyres',
        'V': 'Current prices',
        'VQ': 'Current prices',
        'Y': 'Previous year prices'
    }
    
    mappings['REF_AREA'] = country_mappings
    mappings['STANDARD_REVENUE'] = tax_mappings
    mappings['UNIT_MEASURE'] = unit_mappings
    mappings['FREQ'] = freq_mappings
    mappings['SECTOR'] = sector_mappings
    mappings['MEASURE'] = measure_mappings
    mappings['TRANSACTION'] = transaction_mappings
    mappings['ACTIVITY'] = activity_mappings
    mappings['PRICE_BASE'] = price_mappings
    
    return mappings

def apply_label_mappings(df, mappings):
    """Apply label mappings to DataFrame columns"""
    df_labeled = df.copy()
    
    # If it's a Series with MultiIndex, convert to DataFrame first
    if isinstance(df_labeled, pd.Series) and isinstance(df_labeled.index, pd.MultiIndex):
        print("Converting Series with MultiIndex to DataFrame")
        df_labeled = df_labeled.reset_index()
    
    # Apply mappings to columns
    for col in df_labeled.columns:
        if col in mappings:
            print(f"Applying labels to {col}")
            df_labeled[col] = df_labeled[col].map(mappings[col]).fillna(df_labeled[col])
    
    return df_labeled

def fetch_oecd_data(url, filename, description):
    """Fetch OECD data in XML format and apply labels"""
    print(f"\n=== {description} ===")
    print(f"Fetching data from: {url}")
    
    # Make request with retry logic
    response = make_request_with_retry(url)
    
    # Save XML response
    xml_filename = f"data/{filename}.xml"
    with open(xml_filename, "wb") as f:
        f.write(response.content)
    
    print(f"Saved XML to {xml_filename}")
    
    # Parse XML with pandasdmx
    msg = pandasdmx.read_sdmx(xml_filename)
    df = msg.to_pandas()
    
    # Display info about the data
    print(f"Data shape: {df.shape}")
    print(f"Data type: {type(df)}")
    
    # If it's a Series with MultiIndex, convert to DataFrame
    if isinstance(df, pd.Series) and isinstance(df.index, pd.MultiIndex):
        print("Converting Series with MultiIndex to DataFrame")
        df = df.reset_index()
        print(f"After reset_index, shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
    
    print("\nFirst few rows:")
    print(df.head())
    
    # Apply label mappings
    mappings = get_comprehensive_label_mappings()
    df_labeled = apply_label_mappings(df, mappings)
    
    # Save both versions
    df.to_csv(f"data/{filename}_raw.csv", index=False)
    df_labeled.to_csv(f"data/{filename}_labeled.csv", index=False)
    
    print(f"Saved raw data to data/{filename}_raw.csv")
    print(f"Saved labeled data to data/{filename}_labeled.csv")
    
    return df_labeled

# Check command line arguments
table_to_run = None
if len(sys.argv) > 1:
    table_to_run = int(sys.argv[1])
    print(f"Running only table {table_to_run}")

# Ensure the data directory exists
os.makedirs("data", exist_ok=True)

# Define the OECD data tables to fetch
tables = [
    {
        "id": 1,
        "url": "https://sdmx.oecd.org/public/rest/data/OECD.CTP.TPS,DSD_REV_COMP_GLOBAL@DF_RSGLOBAL,2.1/..S13._T..PT_B1GQ.A?startPeriod=2014&dimensionAtObservation=AllDimensions",
        "filename": "oecd_tax_revenue_statistics",
        "description": "Tax Revenue Statistics (Total tax revenue as % of GDP)"
    },
    {
        "id": 2,
        "url": "https://sdmx.oecd.org/public/rest/data/OECD.SDD.NAD,DSD_NAMAIN10@DF_TABLE1_OUTPUT,2.0/A.AUS........V..?startPeriod=2019&dimensionAtObservation=AllDimensions",
        "filename": "oecd_national_accounts",
        "description": "National Accounts Main Aggregates (GDP data for Australia)"
    },
    {
        "id": 3,
        "url": "https://sdmx.oecd.org/public/rest/data/OECD.SDD.TPS,DSD_LFS@DF_IALFS_LF_Q,1.0/.LF.._Z.Y._T.Y15T64..A?startPeriod=2018&dimensionAtObservation=AllDimensions",
        "filename": "oecd_labour_force",
        "description": "Labour Force Statistics (Employment rates)"
    },
    {
        "id": 4,
        "url": "https://sdmx.oecd.org/public/rest/data/OECD.CTP.TPS,DSD_REV_COMP_GLOBAL@DF_RSGLOBAL,2.1/..S13.T_5000+T_4000+T_1000+_T+T_2000..PT_B1GQ.A?startPeriod=2014&dimensionAtObservation=AllDimensions",
        "filename": "oecd_detailed_tax_revenue",
        "description": "Detailed Tax Revenue by Category (Multiple tax categories)"
    }
]

# Run the specified table(s)
for table in tables:
    if table_to_run is None or table_to_run == table["id"]:
        print(f"\n{'='*60}")
        print(f"Processing Table {table['id']}: {table['description']}")
        print(f"{'='*60}")
        
        try:
            df = fetch_oecd_data(
                table["url"], 
                table["filename"], 
                table["description"]
            )
            
            print(f"✓ Successfully fetched table {table['id']}")
            
            # Add delay between tables to avoid rate limiting
            if table_to_run is None and table["id"] < len(tables):
                delay = 30 + random.uniform(10, 20)
                print(f"Waiting {delay:.1f} seconds before next table...")
                time.sleep(delay)
                
        except Exception as e:
            print(f"✗ Error fetching table {table['id']}: {e}")
            continue

print(f"\n{'='*60}")
print("Data collection completed!")
print(f"{'='*60}")

# List all generated files
print("\nGenerated files:")
for file in os.listdir("data"):
    if file.endswith(".csv") and "oecd_" in file:
        filepath = os.path.join("data", file)
        size = os.path.getsize(filepath)
        print(f"  {file} ({size:,} bytes)") 