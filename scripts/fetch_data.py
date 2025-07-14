#!/usr/bin/env python3
"""
Fetch Real OECD Data from SDMX-ML API

This script fetches data from three OECD tables using their SDMX-ML API endpoints,
parses the XML responses with pandasdmx, converts them to pandas DataFrames,
and saves them as CSV files for further analysis.
"""

import os
import requests
import pandasdmx
import time

# Data Source URLS
# tax revs: https://data-explorer.oecd.org/vis?fs[0]=Topic%2C1%7CTaxation%23TAX%23%7CGlobal%20tax%20revenues%23TAX_GTR%23&pg=0&fc=Topic&bp=true&snb=155&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_REV_COMP_GLOBAL%40DF_RSGLOBAL&df[ag]=OECD.CTP.TPS&df[vs]=2.1&dq=..S13._T..PT_B1GQ.A&lom=LASTNPERIODS&lo=10&to[TIME_PERIOD]=false
# GDP: https://data-explorer.oecd.org/vis?tm=annual%20gdp%20developer&pg=0&hc[Table%20identifier]=&snb=157&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_NAMAIN10%40DF_TABLE1&df[ag]=OECD.SDD.NAD&df[vs]=2.0&dq=A........PC%2BUSD_PPP_PS%2BUSD_PPP..G1.T0101&pd=1990%2C2024&to[TIME_PERIOD]=false
# labor force pop: https://data-explorer.oecd.org/vis?tm=population%20labour&pg=0&snb=99&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_LFS%40DF_IALFS_LF_Q&df[ag]=OECD.SDD.TPS&df[vs]=1.0&dq=.LF.._Z.Y._T.Y15T64..Q&lom=LASTNPERIODS&lo=7&to[TIME_PERIOD]=false&vw=tb

# Ensure the data directory exists
os.makedirs("data", exist_ok=True)

# Set up headers to mimic a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/vnd.sdmx.genericdata+xml; charset=utf-8; version=2.1',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# structure query: https://sdmx.oecd.org/public/rest/dataflow/OECD.CTP.TPS/DSD_REV_COMP_GLOBAL@DF_RSGLOBAL/2.1?references=all
# --- First Table: Tax Revenues 1990-2023
print("Fetching Table 1: Tax Revenues...")
url1 = "https://sdmx.oecd.org/public/rest/data/OECD.CTP.TPS,DSD_REV_COMP_GLOBAL@DF_RSGLOBAL,2.1/..S13.T_5000+T_4000+T_2000+T_1000+_T..PT_B1GQ.A?startPeriod=1990&endPeriod=2023&dimensionAtObservation=AllDimensions"
response1 = requests.get(url1, headers=headers)
response1.raise_for_status()
with open("data/tax_revenues.xml", "wb") as f:
    f.write(response1.content)
msg1 = pandasdmx.read_sdmx("data/tax_revenues.xml")
df1 = msg1.to_pandas()
df1.to_csv("data/tax_revenues.csv")
print("Saved as data/tax_revenues.csv")
print(df1.head())

# Add delay between requests to avoid rate limiting
time.sleep(2)

# --- Second Table: National Accounts GDP per capita and PPP ---
print("Fetching Table 2: GDPs...")
url2 = "https://sdmx.oecd.org/public/rest/data/OECD.SDD.NAD,DSD_NAMAIN10@DF_TABLE1,2.0/A........PC+USD_PPP_PS+USD_PPP..G1.T0101?startPeriod=1990&endPeriod=2023&dimensionAtObservation=AllDimensions"
response2 = requests.get(url2, headers=headers)
response2.raise_for_status()
with open("data/gdp.xml", "wb") as f:
    f.write(response2.content)
msg2 = pandasdmx.read_sdmx("data/gdp.xml")
df2 = msg2.to_pandas()
df2.to_csv("data/gdp.csv")
print("Saved as data/gdp.csv")
print(df2.head())

# Add delay between requests to avoid rate limiting
time.sleep(2)

# --- Third Table: Labor Force Statistics (Working-age population) ---
print("Fetching Table 3: Labor Force Populations...")
url3 = "https://sdmx.oecd.org/public/rest/data/OECD.SDD.TPS,DSD_LFS@DF_IALFS_LF_Q,1.0/.LF.._Z.Y._T.Y15T64..A?startPeriod=1990&endPeriod=2023&dimensionAtObservation=AllDimensions"
response3 = requests.get(url3, headers=headers)
response3.raise_for_status()
with open("data/labor_force.xml", "wb") as f:
    f.write(response3.content)
msg3 = pandasdmx.read_sdmx("data/labor_force.xml")
df3 = msg3.to_pandas()
df3.to_csv("data/labor_force.csv")
print("Saved as data/labor_force.csv")
print(df3.head())

print("All data collection completed successfully!") 