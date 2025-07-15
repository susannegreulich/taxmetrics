# TaxMetrics: OECD Tax and Economic Data Analysis

A Python-based data analysis pipeline for examining the relationship between tax policies and economic performance using real OECD data from 1990-2023.

## Project Overview

This project analyzes the relationship between different types of taxation and economic growth across OECD countries. It fetches real data from OECD databases, processes it through a standardized pipeline, and generates interactive visualizations and statistical analyses to understand tax policy impacts.

## What It Does

1. **Data Collection**: Fetches tax revenue, GDP, and population data from OECD SDMX APIs
2. **Data Processing**: Filters, cleans, and labels the raw data for analysis
3. **Time Series Analysis**: Tracks tax rates and economic metrics over time (1990-2023)
4. **Statistical Analysis**: Computes country averages and correlation analyses
5. **Visualization**: Creates interactive HTML charts and scatter plots

## Key Metrics Analyzed

- **Tax Revenue Types**: Total tax, income tax, goods/services tax, property tax, social security
- **Economic Indicators**: GDP per capita, GDP growth rates
- **Time Period**: 1990-2023 across OECD countries
- **Units**: Tax revenue as percentage of GDP, GDP per capita in USD PPP

## Project Structure

```
taxmetrics/
├── scripts/           # Analysis pipeline scripts
│   ├── 1fetch_data.py      # Collect OECD data via API
│   ├── 2filter_data.py     # Filter and clean data
│   ├── 3label_data.py      # Apply human-readable labels
│   ├── 4over_time.py       # Time series analysis
│   ├── 5data_quality_check.py # Data validation
│   ├── 6averages.py        # Country averages computation
│   └── 7visuals.py         # Generate interactive charts
├── data/              # Data storage
│   ├── raw/           # Raw OECD XML/CSV files
│   ├── filtered/      # Cleaned datasets
│   └── labeled/       # Human-readable labeled data
├── results/           # Analysis outputs
│   ├── over_time/     # Time series data and HTML charts
│   └── averages/      # Country averages and correlation plots
└── config/            # Configuration files
```

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the complete analysis pipeline**:
   ```bash
   python scripts/1fetch_data.py    # Collect OECD data
   python scripts/2filter_data.py   # Clean and filter
   python scripts/3label_data.py    # Apply labels
   python scripts/4over_time.py     # Time series analysis
   python scripts/5data_quality_check.py  # Validate data
   python scripts/6averages.py      # Compute averages
   python scripts/7visuals.py       # Generate charts
   ```

3. **View results**:
   - Interactive time series charts: `results/over_time/*.html`
   - Country averages: `results/averages/all_metrics_country_averages.csv`
   - Correlation analysis: `results/averages/correlation_summary.csv`

## Key Findings

The analysis reveals relationships between:
- **Tax Revenue vs GDP Growth**: Correlation between total tax burden and economic growth
- **Tax Type Analysis**: Different impacts of income, goods, property, and social security taxes
- **Country Comparisons**: Tax policy effectiveness across OECD nations
- **Temporal Trends**: How tax policies and economic performance evolved over 30+ years

## Data Sources

All data sourced from OECD databases. I used the OECD data explorer, went to the respective tables given by the URLs below, chose the settings/configs, and then 
used the Developer API links for the data query and structure query. Below is a list of all the table links and queries.

tax link: https://data-explorer.oecd.org/vis?fs[0]=Topic%2C1%7CTaxation%23TAX%23%7CGlobal%20tax%20revenues%23TAX_GTR%23&pg=0&fc=Topic&bp=true&snb=155&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_REV_COMP_GLOBAL%40DF_RSGLOBAL&df[ag]=OECD.CTP.TPS&df[vs]=2.1&dq=..S13.T_5000%2BT_4000%2BT_2000%2BT_1000%2B_T..PT_B1GQ.A&to[TIME_PERIOD]=false&pd=1990%2C2023
tax data query: https://sdmx.oecd.org/public/rest/data/OECD.CTP.TPS,DSD_REV_COMP_GLOBAL@DF_RSGLOBAL,2.1/..S13.T_5000+T_4000+T_2000+T_1000+_T..PT_B1GQ.A?startPeriod=1990&endPeriod=2023&dimensionAtObservation=AllDimensions
tax structure query: https://sdmx.oecd.org/public/rest/dataflow/OECD.CTP.TPS/DSD_REV_COMP_GLOBAL@DF_RSGLOBAL/2.1?references=all
unit of measurement: percentage of GDP

# GDP link: https://data-explorer.oecd.org/vis?tm=annual%20gdp%20developer&pg=0&hc[Table%20identifier]=&snb=157&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_NAMAIN10%40DF_TABLE1&df[ag]=OECD.SDD.NAD&df[vs]=2.0&dq=A..S1..B1GQ._Z._Z._Z.USD_PPP.V.N.T0102&pd=1990%2C2023&to[TIME_PERIOD]=false
data "https://sdmx.oecd.org/public/rest/data/OECD.SDD.NAD,DSD_NAMAIN10@DF_TABLE1,2.0/A..S1..B1GQ._Z._Z._Z.USD_PPP.V.N.T0102?startPeriod=1990&endPeriod=2023&dimensionAtObservation=AllDimensions"
structure: 'https://sdmx.oecd.org/public/rest/dataflow/OECD.SDD.NAD/DSD_NAMAIN10@DF_TABLE1/2.0?references=all',
Unit of measurement: US dollars, PPP converted, Current prices, Millions


population: https://data-explorer.oecd.org/vis?tm=population&pg=0&hc[Transaction]=&snb=305&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_NAMAIN10%40DF_TABLE3&df[ag]=OECD.SDD.NAD&df[vs]=2.0&dq=A..S1.S1.POP.._Z..PS...&pd=1990%2C2023&to[TIME_PERIOD]=false
data query: https://sdmx.oecd.org/public/rest/data/OECD.SDD.NAD,DSD_NAMAIN10@DF_TABLE3,2.0/A..S1.S1.POP.._Z..PS...?startPeriod=1990&endPeriod=2023&dimensionAtObservation=AllDimensions
structure query: https://sdmx.oecd.org/public/rest/dataflow/OECD.SDD.NAD/DSD_NAMAIN10@DF_TABLE3/2.0?references=all
Unit of measurement: one thousand persons


## Output Files

### Interactive Visualizations
- Time series charts for each tax type and economic metric
- Dropdown selection for individual countries
- Hover information and legends

### Statistical Analysis
- Country averages across all time periods
- Correlation coefficients between tax types and GDP growth
- Descriptive statistics and data quality reports

### Data Files
- Cleaned CSV datasets ready for further analysis
- Labeled data with human-readable categories
- Missing value reports and data quality metrics

## Technical Details

- **Data Format**: SDMX-XML from OECD APIs, converted to pandas DataFrames
- **Visualization**: Plotly for interactive HTML charts
- **Analysis**: Pandas for data manipulation, NumPy for statistical calculations
- **Coverage**: 30+ OECD countries, 1990-2023 time period
- **Update Frequency**: Data can be refreshed by re-running the pipeline

## Future Enhancements

- Using ONLY countries with zero missing values. 
- Multiple linear regression, with GDP growth rate as dependent variable, and the 
various tax rates as independent variables. 
- Laffer curve analysis for optimal tax rates