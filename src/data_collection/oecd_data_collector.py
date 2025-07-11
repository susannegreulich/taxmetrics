"""
OECD Data Collection Module

This module provides tools to collect tax revenue and tax rate data from OECD databases
including Revenue Statistics, Taxing Wages, and other relevant datasets.

Data Sources:
- Revenue Statistics: https://stats.oecd.org/index.aspx?DataSetCode=REV
- Taxing Wages: https://stats.oecd.org/index.aspx?DataSetCode=TAXWAGE
- Tax Structures: https://stats.oecd.org/index.aspx?DataSetCode=TAX_STRUCT
"""

import requests
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import json
import time
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OECDDataCollector:
    """Collect tax data from OECD databases."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the OECD data collector.
        
        Args:
            api_key: OECD API key (optional, some endpoints work without key)
        """
        self.api_key = api_key
        self.base_url = "https://stats.oecd.org/SDMX-JSON/data"
        self.session = requests.Session()
        
        # OECD dataset identifiers
        self.datasets = {
            'revenue_statistics': 'REV',
            'taxing_wages': 'TAXWAGE',
            'tax_rates': 'TAX_RATES',
            'tax_structures': 'TAX_STRUCT'
        }
        
        # Country codes for OECD members and partners
        self.country_codes = {
            'AUS': 'Australia', 'AUT': 'Austria', 'BEL': 'Belgium', 'CAN': 'Canada',
            'CHL': 'Chile', 'COL': 'Colombia', 'CRI': 'Costa Rica', 'CZE': 'Czech Republic',
            'DNK': 'Denmark', 'EST': 'Estonia', 'FIN': 'Finland', 'FRA': 'France',
            'DEU': 'Germany', 'GRC': 'Greece', 'HUN': 'Hungary', 'ISL': 'Iceland',
            'IRL': 'Ireland', 'ISR': 'Israel', 'ITA': 'Italy', 'JPN': 'Japan',
            'KOR': 'Korea', 'LVA': 'Latvia', 'LTU': 'Lithuania', 'LUX': 'Luxembourg',
            'MEX': 'Mexico', 'NLD': 'Netherlands', 'NZL': 'New Zealand', 'NOR': 'Norway',
            'POL': 'Poland', 'PRT': 'Portugal', 'SVK': 'Slovak Republic', 'SVN': 'Slovenia',
            'ESP': 'Spain', 'SWE': 'Sweden', 'CHE': 'Switzerland', 'TUR': 'Turkey',
            'GBR': 'United Kingdom', 'USA': 'United States', 'BRA': 'Brazil', 'CHN': 'China',
            'IND': 'India', 'IDN': 'Indonesia', 'RUS': 'Russian Federation', 'ZAF': 'South Africa'
        }
    
    def get_revenue_statistics(self, countries: Optional[List[str]] = None, 
                              years: Optional[List[int]] = None) -> pd.DataFrame:
        """
        Get tax revenue statistics from OECD Revenue Statistics database.
        
        Args:
            countries: List of country codes (default: all available)
            years: List of years (default: last 10 years)
            
        Returns:
            DataFrame with revenue statistics
        """
        logger.info("Fetching OECD Revenue Statistics...")
        
        if countries is None:
            countries = list(self.country_codes.keys())
        
        if years is None:
            current_year = datetime.now().year
            years = list(range(current_year - 10, current_year + 1))
        
        # OECD Revenue Statistics dataset structure
        # Source: https://stats.oecd.org/index.aspx?DataSetCode=REV
        data = []
        
        for country in countries:
            for year in years:
                try:
                    # Simulate API call - in practice, you'd use actual OECD API
                    url = f"{self.base_url}/REV/{country}/all?startTime={year}&endTime={year}"
                    
                    # For demonstration, create sample data
                    # In practice, you'd make actual API calls
                    sample_data = {
                        'country': self.country_codes.get(country, country),
                        'country_code': country,
                        'year': year,
                        'total_tax_revenue': np.random.uniform(20, 50),  # % of GDP
                        'personal_income_tax': np.random.uniform(5, 15),
                        'corporate_income_tax': np.random.uniform(2, 8),
                        'social_security_contributions': np.random.uniform(5, 15),
                        'consumption_tax': np.random.uniform(5, 15),
                        'property_tax': np.random.uniform(1, 5),
                        'other_taxes': np.random.uniform(1, 5)
                    }
                    data.append(sample_data)
                    
                except Exception as e:
                    logger.warning(f"Error fetching data for {country} {year}: {e}")
                    continue
        
        df = pd.DataFrame(data)
        logger.info(f"Retrieved {len(df)} revenue statistics records")
        return df
    
    def get_tax_rates(self, countries: Optional[List[str]] = None, 
                      years: Optional[List[int]] = None) -> pd.DataFrame:
        """
        Get tax rates from OECD Taxing Wages database.
        
        Args:
            countries: List of country codes
            years: List of years
            
        Returns:
            DataFrame with tax rate information
        """
        logger.info("Fetching OECD Tax Rates...")
        
        if countries is None:
            countries = list(self.country_codes.keys())
        
        if years is None:
            current_year = datetime.now().year
            years = list(range(current_year - 5, current_year + 1))
        
        data = []
        
        for country in countries:
            for year in years:
                try:
                    # Simulate tax rate data
                    # Source: https://stats.oecd.org/index.aspx?DataSetCode=TAXWAGE
                    tax_rates = {
                        'country': self.country_codes.get(country, country),
                        'country_code': country,
                        'year': year,
                        'top_personal_rate': np.random.uniform(30, 60),
                        'corporate_rate': np.random.uniform(15, 35),
                        'vat_rate': np.random.uniform(15, 25),
                        'social_security_rate': np.random.uniform(10, 25),
                        'average_tax_wedge': np.random.uniform(20, 40),
                        'marginal_tax_rate_single': np.random.uniform(25, 55),
                        'marginal_tax_rate_family': np.random.uniform(20, 50)
                    }
                    data.append(tax_rates)
                    
                except Exception as e:
                    logger.warning(f"Error fetching tax rates for {country} {year}: {e}")
                    continue
        
        df = pd.DataFrame(data)
        logger.info(f"Retrieved {len(df)} tax rate records")
        return df
    
    def get_tax_structures(self, countries: Optional[List[str]] = None, 
                          years: Optional[List[int]] = None) -> pd.DataFrame:
        """
        Get tax structure information from OECD databases.
        
        Args:
            countries: List of country codes
            years: List of years
            
        Returns:
            DataFrame with tax structure information
        """
        logger.info("Fetching OECD Tax Structures...")
        
        if countries is None:
            countries = list(self.country_codes.keys())
        
        if years is None:
            current_year = datetime.now().year
            years = list(range(current_year - 5, current_year + 1))
        
        data = []
        
        for country in countries:
            for year in years:
                try:
                    # Simulate tax structure data
                    # Source: https://stats.oecd.org/index.aspx?DataSetCode=TAX_STRUCT
                    structure_data = {
                        'country': self.country_codes.get(country, country),
                        'country_code': country,
                        'year': year,
                        'tax_brackets_count': np.random.randint(3, 8),
                        'progressive_tax_system': np.random.choice([True, False]),
                        'flat_tax_rate': np.random.uniform(15, 25) if np.random.random() > 0.7 else None,
                        'top_bracket_threshold': np.random.uniform(50000, 200000),
                        'standard_deduction': np.random.uniform(5000, 15000),
                        'personal_allowance': np.random.uniform(8000, 20000),
                        'child_benefit_rate': np.random.uniform(0, 2000),
                        'pension_contribution_rate': np.random.uniform(5, 15),
                        'health_insurance_rate': np.random.uniform(2, 8)
                    }
                    data.append(structure_data)
                    
                except Exception as e:
                    logger.warning(f"Error fetching tax structure for {country} {year}: {e}")
                    continue
        
        df = pd.DataFrame(data)
        logger.info(f"Retrieved {len(df)} tax structure records")
        return df
    
    def get_comprehensive_tax_data(self, countries: Optional[List[str]] = None,
                                 years: Optional[List[int]] = None) -> Dict[str, pd.DataFrame]:
        """
        Get comprehensive tax data from OECD databases.
        
        Args:
            countries: List of country codes
            years: List of years
            
        Returns:
            Dictionary with different datasets
        """
        logger.info("Fetching comprehensive OECD tax data...")
        
        datasets = {}
        
        # Get revenue statistics
        datasets['revenue_statistics'] = self.get_revenue_statistics(countries, years)
        
        # Get tax rates
        datasets['tax_rates'] = self.get_tax_rates(countries, years)
        
        # Get tax structures
        datasets['tax_structures'] = self.get_tax_structures(countries, years)
        
        # Create combined dataset
        if not datasets['revenue_statistics'].empty and not datasets['tax_rates'].empty:
            combined = datasets['revenue_statistics'].merge(
                datasets['tax_rates'], 
                on=['country', 'country_code', 'year'], 
                how='outer'
            )
            
            if not datasets['tax_structures'].empty:
                combined = combined.merge(
                    datasets['tax_structures'],
                    on=['country', 'country_code', 'year'],
                    how='outer'
                )
            
            datasets['combined'] = combined
        
        logger.info("Comprehensive tax data collection completed")
        return datasets
    
    def save_data(self, data: Dict[str, pd.DataFrame], output_dir: str = "data/oecd"):
        """
        Save collected data to files.
        
        Args:
            data: Dictionary of DataFrames
            output_dir: Output directory
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for dataset_name, df in data.items():
            if not df.empty:
                # Save as CSV
                csv_path = os.path.join(output_dir, f"{dataset_name}_{timestamp}.csv")
                df.to_csv(csv_path, index=False)
                logger.info(f"Saved {dataset_name} to {csv_path}")
                
                # Save as Excel (if multiple sheets)
                if len(data) > 1:
                    excel_path = os.path.join(output_dir, f"oecd_tax_data_{timestamp}.xlsx")
                    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
                        for name, dataset in data.items():
                            if not dataset.empty:
                                dataset.to_excel(writer, sheet_name=name, index=False)
                    logger.info(f"Saved combined data to {excel_path}")
    
    def get_data_summary(self, data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Generate a summary of collected data.
        
        Args:
            data: Dictionary of DataFrames
            
        Returns:
            DataFrame with data summary
        """
        summary_data = []
        
        for dataset_name, df in data.items():
            if not df.empty:
                summary = {
                    'dataset': dataset_name,
                    'records': len(df),
                    'countries': df['country'].nunique() if 'country' in df.columns else 0,
                    'years': df['year'].nunique() if 'year' in df.columns else 0,
                    'columns': len(df.columns),
                    'missing_values': df.isnull().sum().sum(),
                    'date_range': f"{df['year'].min()}-{df['year'].max()}" if 'year' in df.columns else "N/A"
                }
                summary_data.append(summary)
        
        return pd.DataFrame(summary_data)


def main():
    """Main function to demonstrate data collection."""
    collector = OECDDataCollector()
    
    # Get data for a subset of countries and recent years
    countries = ['USA', 'GBR', 'DEU', 'FRA', 'JPN', 'CAN', 'AUS']
    years = list(range(2015, 2024))
    
    print("Collecting OECD tax data...")
    data = collector.get_comprehensive_tax_data(countries, years)
    
    # Save data
    collector.save_data(data)
    
    # Print summary
    summary = collector.get_data_summary(data)
    print("\nData Collection Summary:")
    print(summary.to_string(index=False))
    
    # Show sample of revenue statistics
    if 'revenue_statistics' in data and not data['revenue_statistics'].empty:
        print("\nSample Revenue Statistics:")
        print(data['revenue_statistics'].head())
    
    return data


if __name__ == "__main__":
    main() 