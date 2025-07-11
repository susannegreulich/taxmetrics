# Tax Policy Analysis Tool

A comprehensive Python-based tool for analyzing tax policies and their revenue implications using real OECD data.

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
├── data/               # OECD data and processed datasets
│   ├── raw/            # Raw OECD data files
│   └── processed/      # Analysis-ready datasets
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
   python3 scripts/fetch_data.py
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

### Key Insights from Real Data
- **Tax Revenue**: Average 35.7% of GDP across countries (range: 21.5% - 49.5%)
- **Top Personal Tax Rates**: Average 46.9% (range: 30.9% - 59.0%)
- **Corporate Tax Rates**: Average 21.4% (range: 15.3% - 30.0%)

## Key Components

### Data Collection
- **OECD Data Collector**: Comprehensive tax data from OECD databases
- **Revenue Statistics**: Tax revenue as % of GDP across countries
- **Tax Rates**: Personal and corporate tax rates
- **Tax Structures**: Tax system characteristics and brackets

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

# Collect OECD tax data
collector = OECDDataCollector()
data = collector.get_comprehensive_tax_data(['USA', 'GBR', 'DEU'], [2015, 2023])

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
python3 scripts/analysis.py --type real --data-file data/processed/analysis_ready_data.csv
```

## Data Sources

All tax data is sourced from OECD databases:
- **Revenue Statistics**: https://stats.oecd.org/index.aspx?DataSetCode=REV
- **Taxing Wages**: https://stats.oecd.org/index.aspx?DataSetCode=TAXWAGE
- **Tax Structures**: https://stats.oecd.org/index.aspx?DataSetCode=TAX_STRUCT

## Output Files

### Generated Reports
- `results/tax_analysis_report.md` - Comprehensive markdown report with OECD data analysis and real data tax policy analysis
- `results/real_data_tax_burden_comparison.html` - Interactive chart showing tax burden comparisons across countries

### Data Files
- `data/processed/analysis_ready_data.csv` - Processed OECD data ready for analysis
- `data/raw/` - Raw OECD data files (revenue statistics, tax rates, tax structures)

## Contributing

This project is designed for tax policy research and analysis. Contributions are welcome for:
- Additional tax policy models
- Enhanced visualization capabilities
- New analysis methodologies
- Documentation improvements
- Expanding country coverage

## License

MIT License - see LICENSE file for details. 

# Todos: 
sanity check results. france's tax rate really low, can it be possible
add button options to interactive html. ie view by country, country averages, etc. 
add more data. fetch more data. more countries, more years. 