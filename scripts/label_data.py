#!/usr/bin/env python3
"""
Apply label mappings to existing data CSV files.

This script takes the official OECD identifier-label dictionary and applies it to all CSV files 
in the data directory to create human-readable labeled versions.
"""

import os
import pandas as pd
import json
from pathlib import Path

def load_official_oecd_mappings():
    """Load official OECD mappings from the extracted structure files"""
    print("Loading official OECD mappings...")
    
    # Load mappings for each dataset
    mappings = {}
    
    # Load tax revenues mappings
    tax_file = Path("results/tax_revenues_mappings.json")
    if tax_file.exists():
        with open(tax_file, 'r') as f:
            tax_mappings = json.load(f)
        mappings['tax_revenues'] = tax_mappings
        print(f"  Loaded tax_revenues mappings: {len(tax_mappings)} categories")
    
    # Load GDP mappings
    gdp_file = Path("results/gdp_mappings.json")
    if gdp_file.exists():
        with open(gdp_file, 'r') as f:
            gdp_mappings = json.load(f)
        mappings['gdp'] = gdp_mappings
        print(f"  Loaded gdp mappings: {len(gdp_mappings)} categories")
    
    # Load labor force mappings
    labor_file = Path("results/labor_force_mappings.json")
    if labor_file.exists():
        with open(labor_file, 'r') as f:
            labor_mappings = json.load(f)
        mappings['labor_force'] = labor_mappings
        print(f"  Loaded labor_force mappings: {len(labor_mappings)} categories")
    
    return mappings

def get_comprehensive_label_mappings():
    """Get comprehensive label mappings for OECD data (fallback to manual mappings)"""
    print("Loading fallback manual mappings...")
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
    
    # Common OECD codes that appear across datasets
    common_mappings = {
        'S1': 'Total economy',
        '_Z': 'Not applicable',
        '_T': 'Total',
        '_X': 'Unspecified'
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
    mappings['COUNTERPART_SECTOR'] = common_mappings
    mappings['EXPENDITURE'] = common_mappings
    
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

def process_csv_file(input_file, output_file, dataset_mappings, fallback_mappings):
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
            mappings_to_use = dataset_mappings.get('tax_revenues', fallback_mappings)
            dataset_name = 'tax_revenues'
        elif 'gdp' in filename:
            mappings_to_use = dataset_mappings.get('gdp', fallback_mappings)
            dataset_name = 'gdp'
        elif 'labor' in filename:
            mappings_to_use = dataset_mappings.get('labor_force', fallback_mappings)
            dataset_name = 'labor_force'
        else:
            mappings_to_use = fallback_mappings
            dataset_name = 'unknown'
        
        print(f"  Using mappings for dataset: {dataset_name}")
        
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

def main():
    """Main function to process all CSV files"""
    print("=" * 60)
    print("Applying Official OECD Labels to CSV Files")
    print("=" * 60)
    
    # Load official OECD mappings
    dataset_mappings = load_official_oecd_mappings()
    
    # Load fallback mappings
    fallback_mappings = get_comprehensive_label_mappings()
    
    # Define the data directory
    data_dir = Path("data")
    if not data_dir.exists():
        print(f"Error: Data directory {data_dir} does not exist")
        return
    
    # Find all CSV files in the data directory
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
            
        # Create output filename
        output_file = csv_file.parent / f"{csv_file.stem}_labeled.csv"
        
        # Process the file
        if process_csv_file(csv_file, output_file, dataset_mappings, fallback_mappings):
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
    for file in data_dir.glob("*_labeled.csv"):
        size = file.stat().st_size
        print(f"  {file.name} ({size:,} bytes)")

if __name__ == "__main__":
    main() 