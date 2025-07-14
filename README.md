# Tax Policy Analysis Tool

A Python-based tool for analyzing tax policies and their revenue implications using real OECD data.

## Features

- **Real Data Analysis**: Uses actual OECD tax data for country-specific policy analysis
- **Tax Policy Modeling**: Simulate different tax structures (progressive, flat, regressive)
- **Revenue Analysis**: Calculate expected tax revenues under various scenarios
- **Tax Burden Analysis**: Analyze tax burden across different income groups
- **Interactive Visualization**: Interactive charts for policy comparison
- **OECD Data Integration**: Comprehensive tax data from OECD databases

## Project Structure

```
taxmetrics/
├── src/                # Tax analysis library
│   ├── models/          # Tax policy models
│   ├── analysis/        # Tax analysis functions
│   ├── visualization/   # Plotting and charts
│   └── data_collection/ # OECD data collection
├── data/               # OECD data and filtered datasets
│   ├── raw/            # Raw OECD data files
│   └── filtered/      # Analysis-ready datasets
├── scripts/            # Analysis and data collection scripts
├── results/            # Generated analysis reports and visualizations
├── config/             # Configuration files
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Collect OECD tax data:
   ```bash
   # Basic data collection (few countries, recent years)
   python3 scripts/fetch_data.py
   
   # Comprehensive data collection (all countries, all years)
   python3 scripts/fetch_comprehensive_data.py --mode comprehensive
   
   # Test the comprehensive collection first
   python3 scripts/test_comprehensive_collection.py
   ```

3. Run tax policy analysis:
   ```bash
   # Real data analysis (using OECD data) - RECOMMENDED
   python3 scripts/analysis.py --type real
   
   # OECD descriptive statistics
   python3 scripts/analysis.py --type oecd
   
   # Both real data and OECD analysis (default)
   python3 scripts/analysis.py --type both
   ```

4. View results:
   - **Interactive Chart**: `results/real_data_tax_burden_comparison.html`
   - **Analysis Report**: `results/tax_analysis_report.md`

## Real Data Analysis

The tool now exclusively uses real OECD tax data for analysis, providing realistic and country-specific tax policy comparisons based on actual country data.

### Current Country Coverage
Based on OECD data, the system analyzes tax policies for:
- **France**: Progressive (48.6% top rate)
- **Germany**: Progressive (43.4% top rate) 
- **Japan**: Progressive (50.0% top rate)
- **UK**: Progressive (58.3% top rate)
- **USA**: Progressive (34.0% top rate)

### Comprehensive Data Collection
The system now supports comprehensive data collection for:
- **All OECD Countries**: 38 member countries
- **Major Non-OECD Economies**: Brazil, China, India, Indonesia, Russia, South Africa, and more
- **G20 Countries**: All G20 member countries
- **Historical Data**: Data from 1965 to present
- **Multiple Datasets**: Revenue statistics, tax rates, and tax structures

### Key Insights from Real Data
- **Tax Revenue**: Average 35.7% of GDP across countries (range: 21.5% - 49.5%)
- **Top Personal Tax Rates**: Average 46.9% (range: 30.9% - 59.0%)
- **Corporate Tax Rates**: Average 21.4% (range: 15.3% - 30.0%)

## Key Components

### Data Collection
- **OECD Data Collector**: Comprehensive tax data from OECD databases
- **Comprehensive Data Collection**: Support for all available countries and years
- **Revenue Statistics**: Tax revenue as % of GDP across countries
- **Tax Rates**: Personal and corporate tax rates
- **Tax Structures**: Tax system characteristics and brackets
- **Data Discovery**: Automatic detection of available countries and years
- **Flexible Collection Modes**: Comprehensive, OECD-only, major economies, G20, or custom selection

### Tax Models
- **Progressive Tax**: Standard progressive tax brackets
- **Flat Tax**: Single tax rate for all income levels
- **Regressive Tax**: Decreasing tax rates with income
- **Custom Tax**: User-defined tax structures

### Analysis Tools
- **Real Data Analysis**: Use actual OECD tax data to create country-specific tax policies
- **OECD Descriptive Statistics**: Analyze raw OECD data for insights and trends
- Revenue calculation under different scenarios
- Tax burden analysis (who pays what)
- Tax progressivity metrics
- Policy comparison framework

### Visualization
- Interactive tax burden charts
- Revenue comparison plots
- Tax incidence analysis
- Policy impact dashboards

## Usage Examples

### Data Collection
```python
from src.data_collection.oecd_data_collector import OECDDataCollector
from src.data_collection.tax_data_processor import TaxDataProcessor

# Basic data collection
collector = OECDDataCollector()
data = collector.get_comprehensive_tax_data(['USA', 'GBR', 'DEU'], [2015, 2023])

# Comprehensive data collection (all countries, all years)
all_data = collector.get_all_available_data()

# Get available countries and years
available_countries = collector.get_available_countries('REV')
available_years = collector.get_available_years('REV', 'USA')

# Process and clean data
processor = TaxDataProcessor()
cleaned_data = processor.clean_data(data)
analysis_data = processor.create_analysis_ready_dataset(cleaned_data)
```

### Tax Policy Analysis
```python
from src.models.tax_policy import ProgressiveTax, FlatTax
from src.analysis.revenue_calculator import RevenueCalculator

# Create tax policies
progressive = ProgressiveTax(brackets=[(0, 50000, 0.15), (50000, 100000, 0.25), (100000, float('inf'), 0.35)])
flat = FlatTax(rate=0.25)

# Calculate revenues
calculator = RevenueCalculator()
revenue_progressive = calculator.calculate_revenue(progressive, income_distribution)
revenue_flat = calculator.calculate_revenue(flat, income_distribution)
```

### Real Data Analysis
```bash
# Run analysis using real OECD data
python3 scripts/analysis.py --type real --data-file data/filtered/analysis_ready_data.csv

# Comprehensive data collection examples
python3 scripts/fetch_comprehensive_data.py --mode comprehensive
python3 scripts/fetch_comprehensive_data.py --mode oecd-only --years 2020-2024
python3 scripts/fetch_comprehensive_data.py --mode major-economies --years 2015-2024
python3 scripts/fetch_comprehensive_data.py --mode g20 --datasets revenue_statistics tax_rates
```

## Data Sources

All tax data is sourced from OECD databases:
- **Revenue Statistics**: https://stats.oecd.org/Index.aspx?DataSetCode=REV
- **Taxing Wages**: https://stats.oecd.org/Index.aspx?DataSetCode=TAXWAGE
- **Tax Structures**: https://stats.oecd.org/Index.aspx?DataSetCode=TAX_STRUCT
- **Tax Revenue**: https://stats.oecd.org/Index.aspx?DataSetCode=TAX_REV
- **Tax Policy**: https://stats.oecd.org/Index.aspx?DataSetCode=TAX_POL
- **Tax Database**: https://stats.oecd.org/Index.aspx?DataSetCode=TAX_DB
- **Tax Statistics**: https://stats.oecd.org/Index.aspx?DataSetCode=TAX_STAT
- **Government Revenue**: https://stats.oecd.org/Index.aspx?DataSetCode=GOV_REV
- **Fiscal Decentralisation**: https://stats.oecd.org/Index.aspx?DataSetCode=FISCAL_DEC
- **Tax Administration**: https://stats.oecd.org/Index.aspx?DataSetCode=TAX_ADMIN

## Output Files

### Generated Reports
- `results/tax_analysis_report.md` - Comprehensive markdown report with OECD data analysis and real data tax policy analysis
- `results/real_data_tax_burden_comparison.html` - Interactive chart showing tax burden comparisons across countries

### Data Files
- `data/filtered/analysis_ready_data.csv` - Filtered OECD data ready for analysis
- `data/raw/` - Raw OECD data files (revenue statistics, tax rates, tax structures)

## Contributing

This project is designed for tax policy research and analysis. Contributions are welcome for:
- Additional tax policy models
- Enhanced visualization capabilities
- New analysis methodologies
- Documentation improvements
- Expanding country coverage


# Todos: 
sanity check results. france's tax rate really low, can it be possible
add button options to interactive html. ie view by country, country averages, etc. 
add more data. fetch more data. more countries, more years. 
move the legend bar to bottom of html chart. EXPLAIN-UNDERSTAND THE CHART. 
add time series?;
check income distribution. which incomes is it? why total population only 1mio?
add SOURCES TO DATA. CURRENT URLS DON'T WORK. 

i'm going to have to collect the data and plan the analysis myself. 
first, find total revenues, then as percentage of GDP, then average GDP growth rate (to see relation
between taxation percentage and economic growth)
growth in revenues, vs growth in gdp
the optimal taxation regime maximizes ABSOLUTE REVENUES, but the absolute revenues must be compared RELATIVE TO POPULATION SIZE, since countries vary in size. 


total tax revenues
gdp
tax revenues/gdp
gdp growth rate
gdp per capita
tax revenue per capita
tax rev = tax base x rate. maximize base and rate. interactive effects. 
tax base = gdp

scatter plot tax base vs rate (gdp vs tax rate)
divided up in to tax TYPES, because it's that complicated. 

income tax rate vs gdp, vs tax revenues
corportae tax rate vs gdp, vs tax revenues
lever = tax rates. 
impact of tax rates on dependent variables tax revenue, gdp. 
tax revenue = a tax rate + b gdp multiple linear regression. 
interactive terms: various tax rates x gdp (because gdp function of tax rates)
evt draw a laffer curve


or import with identifiers as before, and just make a dictionary of labels. to be used in own python code, not necessary to import the data with labels. 


laffer curve: tax revenue as a function of tax rate. (revenues corresponding to rate of that particular tax type)

i need data for:
tax rates of various tax types
tax revenues for these various types, and total tax revenues
economic growth rate

scatter plots to see patterns. 


total tax revenues as percentage of gdp https://data-explorer.oecd.org/vis?fs[0]=Topic%2C1%7CTaxation%23TAX%23%7CGlobal%20tax%20revenues%23TAX_GTR%23&pg=0&fc=Topic&bp=true&snb=155&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_REV_COMP_GLOBAL%40DF_RSGLOBAL&df[ag]=OECD.CTP.TPS&df[vs]=2.1&dq=..S13._T..PT_B1GQ.A&lom=LASTNPERIODS&lo=10&to[TIME_PERIOD]=false&vw=ov


gdp https://data-explorer.oecd.org/vis?tm=gdp&pg=0&snb=364&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_NAMAIN10%40DF_TABLE1_OUTPUT&df[ag]=OECD.SDD.NAD&df[vs]=2.0&dq=A.AUS........V..&lom=LASTNPERIODS&lo=5&to[TIME_PERIOD]=false&vw=tb

find data for CAPITA, to divide gdp and tax revs per capita. labour force population. 
https://data-explorer.oecd.org/vis?tm=population&pg=0&snb=305&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_LFS%40DF_IALFS_LF_Q&df[ag]=OECD.SDD.TPS&df[vs]=1.0&dq=.LF.._Z.Y._T.Y15T64..A&lom=LASTNPERIODS&lo=7&to[TIME_PERIOD]=false


total tax revs per capita in absolute terms = tax rev pct gdp x gdp / capita

scatter plots, laffer curves patterns, for various tax revs PER CAPITA vs tax rates. 
scatter plot tax rates vs economic growth rate. 