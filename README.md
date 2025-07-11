# Tax Policy Analysis Tool

A comprehensive Python-based tool for analyzing tax policies and their revenue implications.

## Features

- **Tax Policy Modeling**: Simulate different tax structures (progressive, flat, regressive)
- **Revenue Analysis**: Calculate expected tax revenues under various scenarios
- **Tax Burden Analysis**: Analyze tax burden across different income groups
- **Visualization**: Interactive charts and graphs for policy comparison
- **Scenario Testing**: Compare multiple tax policy scenarios side-by-side

## Project Structure

```
taxmetrics/
├── src/                # Tax analysis library (excluded from git)
│   ├── models/          # Tax policy models
│   ├── analysis/        # Tax analysis functions
│   ├── visualization/   # Plotting and charts
│   └── data_collection/ # OECD data collection
├── data/               # Sample data and results
├── notebooks/          # Jupyter notebooks for analysis
├── tests/             # Unit tests
├── requirements.txt    # Python dependencies
└── config/            # Configuration files
```

**Note**: The `src/` directory contains the imported tax analysis library code and is excluded from git commits via `.gitignore`. This library provides the core functionality for tax policy modeling, analysis, and visualization.

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
   # Real data analysis (using OECD data)
   python3 scripts/analysis.py --type real
   
   # OECD descriptive statistics
   python3 scripts/analysis.py --type oecd
   
   # Both real data and OECD analysis (default)
   python3 scripts/analysis.py --type both
   ```

4. Explore interactive notebooks:
   ```bash
   jupyter notebook notebooks/
   ```

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
```python
# Run analysis using real OECD data
python3 scripts/analysis.py --type real --data-file data/processed/analysis_ready_data.csv

# This creates tax policies based on actual country data:
# - France Progressive (48.6% top rate)
# - Germany Progressive (43.4% top rate) 
# - Japan Progressive (50.0% top rate)
# - UK Progressive (58.3% top rate)
# - USA Progressive (34.0% top rate)
```

## Data Sources

All tax data is sourced from OECD databases:
- **Revenue Statistics**: https://stats.oecd.org/index.aspx?DataSetCode=REV
- **Taxing Wages**: https://stats.oecd.org/index.aspx?DataSetCode=TAXWAGE
- **Tax Structures**: https://stats.oecd.org/index.aspx?DataSetCode=TAX_STRUCT

## Contributing

This project is designed for tax policy research and analysis. Contributions are welcome for:
- Additional tax policy models
- Enhanced visualization capabilities
- New analysis methodologies
- Documentation improvements

## License

MIT License - see LICENSE file for details. 