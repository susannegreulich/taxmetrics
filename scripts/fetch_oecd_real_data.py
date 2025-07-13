#!/usr/bin/env python3
"""
Parse local OECD SDMX-JSON file (data.org) using pandasdmx and save as CSV.

This script loads a local SDMX-JSON file (e.g., downloaded from OECD), parses it with pandasdmx,
converts it to a pandas DataFrame, and saves it as CSV for further analysis.
"""

import os
import requests
import pandasdmx

# Data URLS
# tax revs: https://data-explorer.oecd.org/vis?fs[0]=Topic%2C1%7CTaxation%23TAX%23%7CGlobal%20tax%20revenues%23TAX_GTR%23&pg=0&fc=Topic&bp=true&snb=155&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_REV_COMP_GLOBAL%40DF_RSGLOBAL&df[ag]=OECD.CTP.TPS&df[vs]=2.1&dq=..S13._T..PT_B1GQ.A&lom=LASTNPERIODS&lo=10&to[TIME_PERIOD]=false
# GDP: https://data-explorer.oecd.org/vis?tm=annual%20gdp%20developer&pg=0&hc[Table%20identifier]=&snb=157&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_NAMAIN10%40DF_TABLE1&df[ag]=OECD.SDD.NAD&df[vs]=2.0&dq=A........PC%2BUSD_PPP_PS%2BUSD_PPP..G1.T0101&pd=1990%2C2024&to[TIME_PERIOD]=false
# labor force pop: https://data-explorer.oecd.org/vis?tm=population%20labour&pg=0&snb=99&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_LFS%40DF_IALFS_LF_Q&df[ag]=OECD.SDD.TPS&df[vs]=1.0&dq=.LF.._Z.Y._T.Y15T64..Q&lom=LASTNPERIODS&lo=7&to[TIME_PERIOD]=false&vw=tb

# Ensure the data directory exists
os.makedirs("data", exist_ok=True)

# --- First Table: Revenue Statistics ---
url1 = "https://sdmx.oecd.org/public/rest/data/OECD.CTP.TPS,DSD_REV_COMP_GLOBAL@DF_RSGLOBAL,2.1/..S13._T..PT_B1GQ.A?startPeriod=2014&dimensionAtObservation=AllDimensions"
response1 = requests.get(url1)
response1.raise_for_status()
with open("data/oecd_data.xml", "wb") as f:
    f.write(response1.content)
msg1 = pandasdmx.read_sdmx("data/oecd_data.xml")
df1 = msg1.to_pandas()
df1.to_csv("data/oecd_api_data.csv")
print("Saved as data/oecd_api_data.csv")
print(df1.head())

# --- Second Table: National Accounts Main Aggregates (Australia) ---
url2 = "https://sdmx.oecd.org/public/rest/data/OECD.SDD.NAD,DSD_NAMAIN10@DF_TABLE1_OUTPUT,2.0/A.AUS........V..?startPeriod=2019&dimensionAtObservation=AllDimensions"
response2 = requests.get(url2)
response2.raise_for_status()
with open("data/oecd_data2.xml", "wb") as f:
    f.write(response2.content)
msg2 = pandasdmx.read_sdmx("data/oecd_data2.xml")
df2 = msg2.to_pandas()
df2.to_csv("data/oecd_api_data2.csv")
print("Saved as data/oecd_api_data2.csv")
print(df2.head())

# --- Third Table: Detailed Tax Categories ---
url3 = "https://sdmx.oecd.org/public/rest/data/OECD.CTP.TPS,DSD_REV_COMP_GLOBAL@DF_RSGLOBAL,2.1/..S13.T_5000+T_4000+T_2000+T_1000+_T..PT_B1GQ.A?startPeriod=2014&dimensionAtObservation=AllDimensions"
response3 = requests.get(url3)
response3.raise_for_status()
with open("data/oecd_data3.xml", "wb") as f:
    f.write(response3.content)
msg3 = pandasdmx.read_sdmx("data/oecd_data3.xml")
df3 = msg3.to_pandas()
df3.to_csv("data/oecd_api_data3.csv")
print("Saved as data/oecd_api_data3.csv")
print(df3.head())

# --- Fourth Table: National Accounts GDP per capita and PPP ---
url4 = "https://sdmx.oecd.org/public/rest/data/OECD.SDD.NAD,DSD_NAMAIN10@DF_TABLE1,2.0/A........PC+USD_PPP_PS+USD_PPP..G1.T0101?startPeriod=1990&endPeriod=2024&dimensionAtObservation=AllDimensions"
response4 = requests.get(url4)
response4.raise_for_status()
with open("data/oecd_data4.xml", "wb") as f:
    f.write(response4.content)
msg4 = pandasdmx.read_sdmx("data/oecd_data4.xml")
df4 = msg4.to_pandas()
df4.to_csv("data/oecd_api_data4.csv")
print("Saved as data/oecd_api_data4.csv")
print(df4.head()) 