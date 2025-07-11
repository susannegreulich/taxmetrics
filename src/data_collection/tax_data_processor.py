"""
Tax Data Processing Module

This module provides tools to clean, validate, and prepare OECD tax data
for analysis.

Data Sources:
- Revenue Statistics: https://stats.oecd.org/index.aspx?DataSetCode=REV
- Taxing Wages: https://stats.oecd.org/index.aspx?DataSetCode=TAXWAGE
- Tax Structures: https://stats.oecd.org/index.aspx?DataSetCode=TAX_STRUCT
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime
import os

logger = logging.getLogger(__name__)


class TaxDataProcessor:
    """Process and clean OECD tax data."""
    
    def __init__(self):
        """Initialize the data processor."""
        self.required_columns = {
            'revenue_statistics': ['country', 'country_code', 'year', 'total_tax_revenue'],
            'tax_rates': ['country', 'country_code', 'year', 'top_personal_rate'],
            'tax_structures': ['country', 'country_code', 'year']
        }
    
    def validate_data(self, data: Dict[str, pd.DataFrame]) -> Dict[str, bool]:
        """
        Validate the structure and content of collected data.
        
        Args:
            data: Dictionary of DataFrames
            
        Returns:
            Dictionary with validation results
        """
        validation_results = {}
        
        for dataset_name, df in data.items():
            if df.empty:
                validation_results[dataset_name] = False
                logger.warning(f"{dataset_name}: Empty dataset")
                continue
            
            # Check required columns
            if dataset_name in self.required_columns:
                required_cols = self.required_columns[dataset_name]
                missing_cols = [col for col in required_cols if col not in df.columns]
                
                if missing_cols:
                    validation_results[dataset_name] = False
                    logger.error(f"{dataset_name}: Missing required columns: {missing_cols}")
                    continue
            
            # Check for reasonable data ranges
            validation_results[dataset_name] = self._check_data_ranges(df, dataset_name)
        
        return validation_results
    
    def _check_data_ranges(self, df: pd.DataFrame, dataset_name: str) -> bool:
        """Check if data values are within reasonable ranges."""
        try:
            if dataset_name == 'revenue_statistics':
                # Tax revenue should be between 0 and 100% of GDP
                if 'total_tax_revenue' in df.columns:
                    if not (df['total_tax_revenue'] >= 0).all() or not (df['total_tax_revenue'] <= 100).all():
                        logger.warning(f"{dataset_name}: Tax revenue values out of expected range")
                        return False
            
            elif dataset_name == 'tax_rates':
                # Tax rates should be between 0 and 100%
                rate_columns = ['top_personal_rate', 'corporate_rate', 'vat_rate']
                for col in rate_columns:
                    if col in df.columns:
                        if not (df[col] >= 0).all() or not (df[col] <= 100).all():
                            logger.warning(f"{dataset_name}: Tax rate values out of expected range in {col}")
                            return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error checking data ranges for {dataset_name}: {e}")
            return False
    
    def clean_data(self, data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """
        Clean and prepare the data for analysis.
        
        Args:
            data: Dictionary of DataFrames
            
        Returns:
            Dictionary with cleaned DataFrames
        """
        cleaned_data = {}
        
        for dataset_name, df in data.items():
            if df.empty:
                continue
            
            logger.info(f"Cleaning {dataset_name} dataset...")
            
            # Create a copy to avoid modifying original
            cleaned_df = df.copy()
            
            # Remove duplicates
            initial_rows = len(cleaned_df)
            cleaned_df = cleaned_df.drop_duplicates()
            if len(cleaned_df) < initial_rows:
                logger.info(f"Removed {initial_rows - len(cleaned_df)} duplicate rows from {dataset_name}")
            
            # Handle missing values
            cleaned_df = self._handle_missing_values(cleaned_df, dataset_name)
            
            # Standardize country names and codes
            cleaned_df = self._standardize_countries(cleaned_df)
            
            # Sort by country and year
            if 'country' in cleaned_df.columns and 'year' in cleaned_df.columns:
                cleaned_df = cleaned_df.sort_values(['country', 'year'])
            
            # Remove outliers
            cleaned_df = self._remove_outliers(cleaned_df, dataset_name)
            
            cleaned_data[dataset_name] = cleaned_df
            
            logger.info(f"Cleaned {dataset_name}: {len(cleaned_df)} records")
        
        return cleaned_data
    
    def _handle_missing_values(self, df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
        """Handle missing values in the dataset."""
        # For numeric columns, fill with median or mean
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_columns:
            if df[col].isnull().sum() > 0:
                if dataset_name == 'revenue_statistics' and 'tax' in col.lower():
                    # For tax data, use median by country
                    df[col] = df.groupby('country')[col].transform(
                        lambda x: x.fillna(x.median())
                    )
                else:
                    # For other data, use overall median
                    df[col] = df[col].fillna(df[col].median())
        
        # For categorical columns, fill with mode
        categorical_columns = df.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            if df[col].isnull().sum() > 0:
                mode_value = df[col].mode().iloc[0] if not df[col].mode().empty else 'Unknown'
                df[col] = df[col].fillna(mode_value)
        
        return df
    
    def _standardize_countries(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize country names and codes."""
        # Standard country name mappings
        country_mappings = {
            'United States': 'USA',
            'United Kingdom': 'UK',
            'Czech Republic': 'Czechia',
            'Slovak Republic': 'Slovakia'
        }
        
        if 'country' in df.columns:
            df['country'] = df['country'].replace(country_mappings)
        
        return df
    
    def _remove_outliers(self, df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
        """Remove statistical outliers from numeric columns."""
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_columns:
            if col in ['year', 'country_code']:  # Skip non-measurement columns
                continue
            
            # Calculate IQR
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            # Define bounds
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Count outliers
            outliers = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
            
            if outliers > 0:
                logger.info(f"Removing {outliers} outliers from {col} in {dataset_name}")
                # Replace outliers with bounds
                df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)
        
        return df
    
    def create_analysis_ready_dataset(self, data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Create a combined dataset ready for analysis.
        
        Args:
            data: Dictionary of cleaned DataFrames
            
        Returns:
            Combined DataFrame ready for analysis
        """
        logger.info("Creating analysis-ready dataset...")
        
        # Start with revenue statistics as base
        if 'revenue_statistics' not in data or data['revenue_statistics'].empty:
            logger.error("Revenue statistics data is required for analysis")
            return pd.DataFrame()
        
        combined_df = data['revenue_statistics'].copy()
        
        # Merge with tax rates
        if 'tax_rates' in data and not data['tax_rates'].empty:
            combined_df = combined_df.merge(
                data['tax_rates'],
                on=['country', 'country_code', 'year'],
                how='left'
            )
        
        # Merge with tax structures
        if 'tax_structures' in data and not data['tax_structures'].empty:
            combined_df = combined_df.merge(
                data['tax_structures'],
                on=['country', 'country_code', 'year'],
                how='left'
            )
        
        # Add derived variables
        combined_df = self._add_derived_variables(combined_df)
        
        logger.info(f"Created analysis-ready dataset with {len(combined_df)} records")
        return combined_df
    
    def _add_derived_variables(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add derived variables for analysis."""
        # Calculate total tax revenue per capita (if GDP data available)
        if 'total_tax_revenue' in df.columns:
            # Assume average GDP per capita for demonstration
            # In practice, you'd use actual GDP data
            df['tax_revenue_per_capita'] = df['total_tax_revenue'] * 50000 / 100  # Simplified calculation
        
        # Calculate tax efficiency (revenue per unit of tax rate)
        if 'total_tax_revenue' in df.columns and 'top_personal_rate' in df.columns:
            df['tax_efficiency'] = df['total_tax_revenue'] / df['top_personal_rate']
        
        # Add year category
        if 'year' in df.columns:
            df['decade'] = (df['year'] // 10) * 10
            df['year_category'] = pd.cut(df['year'], 
                                       bins=[1900, 2000, 2010, 2020, 2030], 
                                       labels=['Pre-2000', '2000s', '2010s', '2020s'])
        
        return df
    
    def generate_summary_statistics(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Generate summary statistics for the dataset.
        
        Args:
            df: Analysis-ready DataFrame
            
        Returns:
            Dictionary with summary statistics
        """
        summaries = {}
        
        # Basic statistics
        summaries['basic_stats'] = df.describe()
        
        # Statistics by country
        if 'country' in df.columns:
            summaries['by_country'] = df.groupby('country').agg({
                'total_tax_revenue': ['mean', 'std', 'min', 'max'],
                'top_personal_rate': ['mean', 'std', 'min', 'max'],
                'corporate_rate': ['mean', 'std', 'min', 'max']
            }).round(2)
        
        # Statistics by year
        if 'year' in df.columns:
            summaries['by_year'] = df.groupby('year').agg({
                'total_tax_revenue': ['mean', 'std', 'min', 'max'],
                'top_personal_rate': ['mean', 'std', 'min', 'max'],
                'corporate_rate': ['mean', 'std', 'min', 'max']
            }).round(2)
        
        # Correlation matrix
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        if len(numeric_columns) > 1:
            summaries['correlations'] = df[numeric_columns].corr().round(3)
        
        return summaries
    
    def save_processed_data(self, data: Dict[str, pd.DataFrame], 
                          output_dir: str = "data/processed") -> None:
        """
        Save processed data to files.
        
        Args:
            data: Dictionary of DataFrames
            output_dir: Output directory
        """
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for dataset_name, df in data.items():
            if not df.empty:
                # Save as CSV
                csv_path = os.path.join(output_dir, f"{dataset_name}_{timestamp}.csv")
                df.to_csv(csv_path, index=False)
                logger.info(f"Saved {dataset_name} to {csv_path}")
        
        # Save combined dataset
        if 'combined' in data and not data['combined'].empty:
            combined_path = os.path.join(output_dir, f"analysis_ready_data_{timestamp}.csv")
            data['combined'].to_csv(combined_path, index=False)
            logger.info(f"Saved combined dataset to {combined_path}")


def main():
    """Main function to demonstrate data processing."""
    from oecd_data_collector import OECDDataCollector
    
    # Collect sample data
    collector = OECDDataCollector()
    raw_data = collector.get_comprehensive_tax_data(['USA', 'GBR', 'DEU'], [2015, 2023])
    
    # Process the data
    processor = TaxDataProcessor()
    
    # Validate data
    validation_results = processor.validate_data(raw_data)
    print("Validation Results:")
    for dataset, is_valid in validation_results.items():
        print(f"  {dataset}: {'✓' if is_valid else '✗'}")
    
    # Clean data
    cleaned_data = processor.clean_data(raw_data)
    
    # Create analysis-ready dataset
    analysis_data = processor.create_analysis_ready_dataset(cleaned_data)
    
    # Generate summaries
    summaries = processor.generate_summary_statistics(analysis_data)
    
    # Save processed data
    processor.save_processed_data(cleaned_data)
    
    print(f"\nProcessing complete. Analysis-ready dataset has {len(analysis_data)} records.")
    
    return analysis_data


if __name__ == "__main__":
    main() 