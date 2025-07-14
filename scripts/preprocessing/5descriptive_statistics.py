#!/usr/bin/env python3
"""
Descriptive Statistics Script for Labeled Datasets

This script analyzes the VALUE column in the three labeled datasets:
- GDP labeled data (economic growth indicators in US dollars PPP)
- Population labeled data (population counts in persons)
- Tax revenues labeled data (tax revenue percentages of GDP)

Outputs comprehensive descriptive statistics in markdown format.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
from datetime import datetime

def load_dataset(file_path, dataset_name):
    """Load a dataset and return basic info and statistics."""
    try:
        df = pd.read_csv(file_path)
        
        # Check if 'value' column exists (case insensitive)
        value_col = None
        for col in df.columns:
            if col.lower() == 'value':
                value_col = col
                break
        
        if value_col is None:
            return {
                'name': dataset_name,
                'error': f"No 'value' column found. Available columns: {list(df.columns)}"
            }
        
        # Convert to numeric, handling any non-numeric values
        df[value_col] = pd.to_numeric(df[value_col], errors='coerce')
        
        # Remove NaN values for statistics
        values = df[value_col].dropna()
        
        if len(values) == 0:
            return {
                'name': dataset_name,
                'error': "No valid numeric values found in the 'value' column"
            }
        
        # Calculate descriptive statistics
        stats = {
            'name': dataset_name,
            'file_path': str(file_path),
            'total_rows': len(df),
            'valid_values': len(values),
            'missing_values': len(df) - len(values),
            'missing_percentage': round((len(df) - len(values)) / len(df) * 100, 2),
            'mean': round(values.mean(), 4),
            'median': round(values.median(), 4),
            'std': round(values.std(), 4),
            'min': round(values.min(), 4),
            'max': round(values.max(), 4),
            'q25': round(values.quantile(0.25), 4),
            'q75': round(values.quantile(0.75), 4),
            'iqr': round(values.quantile(0.75) - values.quantile(0.25), 4),
            'skewness': round(values.skew(), 4),
            'kurtosis': round(values.kurtosis(), 4),
            'range': round(values.max() - values.min(), 4),
            'cv': round(values.std() / values.mean() * 100, 2) if values.mean() != 0 else float('inf')
        }
        
        return stats
        
    except Exception as e:
        return {
            'name': dataset_name,
            'error': f"Error loading dataset: {str(e)}"
        }

def generate_markdown_report(stats_list):
    """Generate a comprehensive markdown report from the statistics."""
    
    report = []
    report.append("# Descriptive Statistics Report")
    report.append("")
    report.append(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    report.append("## Overview")
    report.append("")
    report.append("This report provides comprehensive descriptive statistics for the VALUE column in the three labeled datasets:")
    report.append("")
    report.append("1. **GDP** - Economic growth indicators (US dollars, PPP converted)")
    report.append("2. **Population** - Population counts (persons)") 
    report.append("3. **Tax Revenues** - Government tax revenue data (percentage of GDP)")
    report.append("")
    
    # Calculate column widths for proper alignment
    def calculate_column_widths(stats_list):
        # Initialize with header widths
        widths = {
            'dataset': len('Dataset'),
            'total_rows': len('Total Rows'),
            'valid_values': len('Valid Values'),
            'missing_values': len('Missing Values (%)'),
            'mean': len('Mean'),
            'median': len('Median'),
            'std_dev': len('Std Dev'),
            'min': len('Min'),
            'max': len('Max')
        }
        
        # Update widths based on actual data
        for stats in stats_list:
            if 'error' not in stats:
                widths['dataset'] = max(widths['dataset'], len(stats['name']))
                widths['total_rows'] = max(widths['total_rows'], len(f"{stats['total_rows']:,}"))
                widths['valid_values'] = max(widths['valid_values'], len(f"{stats['valid_values']:,}"))
                widths['missing_values'] = max(widths['missing_values'], len(f"{stats['missing_percentage']}%"))
                widths['mean'] = max(widths['mean'], len(f"{stats['mean']:.4f}"))
                widths['median'] = max(widths['median'], len(f"{stats['median']:.4f}"))
                widths['std_dev'] = max(widths['std_dev'], len(f"{stats['std']:.4f}"))
                widths['min'] = max(widths['min'], len(f"{stats['min']:.4f}"))
                widths['max'] = max(widths['max'], len(f"{stats['max']:.4f}"))
            else:
                widths['dataset'] = max(widths['dataset'], len(stats['name']))
                widths['total_rows'] = max(widths['total_rows'], len('ERROR'))
                widths['valid_values'] = max(widths['valid_values'], len('ERROR'))
                widths['missing_values'] = max(widths['missing_values'], len('ERROR'))
                widths['mean'] = max(widths['mean'], len('ERROR'))
                widths['median'] = max(widths['median'], len('ERROR'))
                widths['std_dev'] = max(widths['std_dev'], len('ERROR'))
                widths['min'] = max(widths['min'], len('ERROR'))
                widths['max'] = max(widths['max'], len('ERROR'))
        
        return widths
    
    widths = calculate_column_widths(stats_list)
    
    # Summary table
    report.append("## Summary Table")
    report.append("")
    
    # Header row
    header = f"| {'Dataset':<{widths['dataset']}} | {'Total Rows':<{widths['total_rows']}} | {'Valid Values':<{widths['valid_values']}} | {'Missing Values (%)':<{widths['missing_values']}} | {'Mean':<{widths['mean']}} | {'Median':<{widths['median']}} | {'Std Dev':<{widths['std_dev']}} | {'Min':<{widths['min']}} | {'Max':<{widths['max']}} |"
    report.append(header)
    
    # Separator row
    separator = f"|{'-' * (widths['dataset'] + 2)}|{'-' * (widths['total_rows'] + 2)}|{'-' * (widths['valid_values'] + 2)}|{'-' * (widths['missing_values'] + 2)}|{'-' * (widths['mean'] + 2)}|{'-' * (widths['median'] + 2)}|{'-' * (widths['std_dev'] + 2)}|{'-' * (widths['min'] + 2)}|{'-' * (widths['max'] + 2)}|"
    report.append(separator)
    
    # Data rows
    for stats in stats_list:
        if 'error' in stats:
            row = f"| {stats['name']:<{widths['dataset']}} | {'ERROR':<{widths['total_rows']}} | {'ERROR':<{widths['valid_values']}} | {'ERROR':<{widths['missing_values']}} | {'ERROR':<{widths['mean']}} | {'ERROR':<{widths['median']}} | {'ERROR':<{widths['std_dev']}} | {'ERROR':<{widths['min']}} | {'ERROR':<{widths['max']}} |"
        else:
            row = f"| {stats['name']:<{widths['dataset']}} | {stats['total_rows']:<{widths['total_rows']},} | {stats['valid_values']:<{widths['valid_values']},} | {stats['missing_percentage']:<{widths['missing_values']-1}}% | {stats['mean']:<{widths['mean']}.4f} | {stats['median']:<{widths['median']}.4f} | {stats['std']:<{widths['std_dev']}.4f} | {stats['min']:<{widths['min']}.4f} | {stats['max']:<{widths['max']}.4f} |"
        report.append(row)
    
    report.append("")
    
    # Detailed statistics for each dataset
    for stats in stats_list:
        report.append(f"## {stats['name']}")
        report.append("")
        
        if 'error' in stats:
            report.append(f"**Error:** {stats['error']}")
            report.append("")
            continue
            
        report.append(f"**File:** `{stats['file_path']}`")
        report.append("")
        
        # Data quality
        report.append("### Data Quality")
        report.append("")
        report.append(f"- **Total Observations:** {stats['total_rows']:,}")
        report.append(f"- **Valid Values:** {stats['valid_values']:,}")
        report.append(f"- **Missing Values:** {stats['missing_values']:,} ({stats['missing_percentage']}%)")
        report.append("")
        
        # Central tendency
        report.append("### Central Tendency")
        report.append("")
        report.append(f"- **Mean:** {stats['mean']}")
        report.append(f"- **Median:** {stats['median']}")
        report.append("")
        
        # Dispersion
        report.append("### Dispersion")
        report.append("")
        report.append(f"- **Standard Deviation:** {stats['std']}")
        report.append(f"- **Range:** {stats['range']}")
        report.append(f"- **Interquartile Range (IQR):** {stats['iqr']}")
        report.append(f"- **Coefficient of Variation:** {stats['cv']}%")
        report.append("")
        
        # Percentiles
        report.append("### Percentiles")
        report.append("")
        report.append(f"- **25th Percentile (Q1):** {stats['q25']}")
        report.append(f"- **75th Percentile (Q3):** {stats['q75']}")
        report.append("")
        
        # Distribution shape
        report.append("### Distribution Shape")
        report.append("")
        report.append(f"- **Skewness:** {stats['skewness']}")
        if stats['skewness'] > 0.5:
            report.append("  - *Interpretation: Right-skewed (positive skew)*")
        elif stats['skewness'] < -0.5:
            report.append("  - *Interpretation: Left-skewed (negative skew)*")
        else:
            report.append("  - *Interpretation: Approximately symmetric*")
        report.append("")
        report.append(f"- **Kurtosis:** {stats['kurtosis']}")
        if stats['kurtosis'] > 3:
            report.append("  - *Interpretation: Heavy-tailed (leptokurtic)*")
        elif stats['kurtosis'] < 3:
            report.append("  - *Interpretation: Light-tailed (platykurtic)*")
        else:
            report.append("  - *Interpretation: Normal-like tails (mesokurtic)*")
        report.append("")
        
        # Extreme values
        report.append("### Extreme Values")
        report.append("")
        report.append(f"- **Minimum:** {stats['min']}")
        report.append(f"- **Maximum:** {stats['max']}")
        report.append("")
    
    # Comparative analysis
    report.append("## Comparative Analysis")
    report.append("")
    
    # Filter out datasets with errors
    valid_stats = [s for s in stats_list if 'error' not in s]
    
    if len(valid_stats) >= 2:
        report.append("### Scale Comparison")
        report.append("")
        report.append("The datasets operate on different scales:")
        report.append("")
        
        for stats in valid_stats:
            if stats['mean'] > 1000000:
                scale = "Very large scale (millions+)"
            elif stats['mean'] > 10000:
                scale = "Large scale (tens of thousands+)"
            elif stats['mean'] > 100:
                scale = "Medium scale (hundreds+)"
            elif stats['mean'] > 10:
                scale = "Small scale (tens)"
            else:
                scale = "Very small scale (units/percentages)"
            
            report.append(f"- **{stats['name']}:** {scale} (mean: {stats['mean']})")
        
        report.append("")
        
        # Variability comparison
        report.append("### Variability Comparison")
        report.append("")
        report.append("Coefficient of Variation (CV) comparison (lower = less variable):")
        report.append("")
        
        for stats in valid_stats:
            cv_interpretation = "Low variability" if stats['cv'] < 15 else "Medium variability" if stats['cv'] < 35 else "High variability"
            report.append(f"- **{stats['name']}:** CV = {stats['cv']}% ({cv_interpretation})")
        
        report.append("")
    
    # Recommendations
    report.append("## Recommendations")
    report.append("")
    report.append("### Data Quality")
    report.append("")
    for stats in stats_list:
        if 'error' not in stats:
            if stats['missing_percentage'] > 10:
                report.append(f"- **{stats['name']}:** High missing data rate ({stats['missing_percentage']}%). Consider investigating data collection issues.")
            elif stats['missing_percentage'] > 5:
                report.append(f"- **{stats['name']}:** Moderate missing data rate ({stats['missing_percentage']}%). Consider imputation methods if appropriate.")
            else:
                report.append(f"- **{stats['name']}:** Good data quality with low missing rate ({stats['missing_percentage']}%).")
    
    report.append("")
    report.append("### Statistical Considerations")
    report.append("")
    for stats in stats_list:
        if 'error' not in stats:
            if abs(stats['skewness']) > 1:
                report.append(f"- **{stats['name']}:** Highly skewed distribution. Consider log transformation or non-parametric methods.")
            elif abs(stats['skewness']) > 0.5:
                report.append(f"- **{stats['name']}:** Moderately skewed. Parametric methods may still be appropriate.")
            else:
                report.append(f"- **{stats['name']}:** Approximately symmetric distribution. Parametric methods are suitable.")
    
    report.append("")
    report.append("---")
    report.append("*Report generated automatically by descriptive_statistics.py*")
    
    return "\n".join(report)

def main():
    """Main function to run the descriptive statistics analysis."""
    
    # Define dataset paths
    data_dir = Path("data/labeled")
    datasets = [
        ("GDP", data_dir / "gdp_labeled.csv"),
        ("Population", data_dir / "population_labeled.csv"),
        ("Tax Revenues", data_dir / "tax_revenues_labeled.csv")
    ]
    
    print("Loading and analyzing datasets...")
    
    # Load and analyze each dataset
    stats_list = []
    for name, file_path in datasets:
        print(f"Processing {name}...")
        stats = load_dataset(file_path, name)
        stats_list.append(stats)
    
    # Generate markdown report
    print("Generating markdown report...")
    report = generate_markdown_report(stats_list)
    
    # Save report to file
    output_file = Path("data/summary/descriptive_stats.md")
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Report saved to: {output_file}")
    print("\n" + "="*50)
    print("DESCRIPTIVE STATISTICS SUMMARY")
    print("="*50)
    
    # Print summary to console
    for stats in stats_list:
        print(f"\n{stats['name']}:")
        if 'error' in stats:
            print(f"  ERROR: {stats['error']}")
        else:
            print(f"  Rows: {stats['total_rows']:,}, Valid: {stats['valid_values']:,}, Missing: {stats['missing_percentage']}%")
            print(f"  Mean: {stats['mean']}, Median: {stats['median']}, Std: {stats['std']}")
            print(f"  Range: [{stats['min']}, {stats['max']}]")

if __name__ == "__main__":
    main() 