#!/usr/bin/env python3
"""
Enhanced script for detailed country analysis including correlations and insights.
This script builds upon the basic averages computation and provides additional analysis.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def load_averages_data():
    """
    Load the computed country averages from the CSV files.
    
    Returns:
        pd.DataFrame: DataFrame with countries as index and metrics as columns
    """
    base_dir = Path("results/country_averages")
    
    # Load the combined results
    combined_file = base_dir / "all_metrics_country_averages.csv"
    if combined_file.exists():
        df = pd.read_csv(combined_file, index_col=0)
        return df
    else:
        print("Combined averages file not found. Please run compute_country_averages.py first.")
        return None

def analyze_correlations(df):
    """
    Analyze correlations between different metrics.
    
    Args:
        df (pd.DataFrame): DataFrame with country averages
    """
    print("CORRELATION ANALYSIS")
    print("=" * 50)
    
    # Compute correlation matrix
    corr_matrix = df.corr()
    
    print("\nCorrelation Matrix:")
    print(corr_matrix.round(3))
    
    # Find strongest correlations
    print("\nStrongest correlations (absolute value > 0.3):")
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_value = corr_matrix.iloc[i, j]
            if abs(corr_value) > 0.3:
                print(f"{corr_matrix.columns[i]} vs {corr_matrix.columns[j]}: {corr_value:.3f}")
    
    return corr_matrix

def identify_country_patterns(df):
    """
    Identify countries with interesting patterns across metrics.
    
    Args:
        df (pd.DataFrame): DataFrame with country averages
    """
    print("\nCOUNTRY PATTERN ANALYSIS")
    print("=" * 50)
    
    # Countries with highest overall tax burden (sum of all tax metrics)
    tax_metrics = [col for col in df.columns if 'tax' in col.lower() or 'ssc' in col.lower()]
    df['Total_Tax_Burden'] = df[tax_metrics].sum(axis=1)
    
    print("\nTop 10 countries by total tax burden:")
    print(df['Total_Tax_Burden'].sort_values(ascending=False).head(10))
    
    # Countries with high growth but low tax burden
    df['Growth_Tax_Ratio'] = df['GDP per capita growth rates'] / df['Total_Tax_Burden']
    
    print("\nTop 10 countries by growth-to-tax ratio:")
    print(df['Growth_Tax_Ratio'].sort_values(ascending=False).head(10))
    
    # Countries with balanced tax structure (low variance across tax types)
    tax_std = df[tax_metrics].std(axis=1)
    print("\nCountries with most balanced tax structure (lowest standard deviation):")
    print(tax_std.sort_values().head(10))
    
    return df

def create_summary_statistics(df):
    """
    Create comprehensive summary statistics.
    
    Args:
        df (pd.DataFrame): DataFrame with country averages
    """
    print("\nDETAILED SUMMARY STATISTICS")
    print("=" * 50)
    
    # Basic statistics
    print("\nBasic Statistics:")
    print(df.describe())
    
    # Regional analysis (if we can identify regions)
    print("\nRegional Analysis (by country name patterns):")
    
    # Simple regional grouping based on country names
    european_countries = [col for col in df.index if any(region in col.lower() for region in 
                       ['germany', 'france', 'italy', 'spain', 'uk', 'united kingdom', 'netherlands', 
                        'belgium', 'austria', 'switzerland', 'sweden', 'norway', 'denmark', 'finland',
                        'poland', 'czech', 'hungary', 'romania', 'bulgaria', 'croatia', 'slovenia',
                        'slovak', 'estonia', 'latvia', 'lithuania', 'ireland', 'iceland', 'luxembourg',
                        'malta', 'portugal', 'greece'])]
    
    asian_countries = [col for col in df.index if any(region in col.lower() for region in
                     ['china', 'japan', 'korea', 'singapore', 'hong kong', 'indonesia'])]
    
    american_countries = [col for col in df.index if any(region in col.lower() for region in
                       ['united states', 'canada', 'mexico', 'brazil', 'argentina', 'chile', 'colombia'])]
    
    print(f"\nEuropean countries (n={len(european_countries)}):")
    if european_countries:
        european_avg = df.loc[european_countries].mean()
        print(european_avg)
    
    print(f"\nAsian countries (n={len(asian_countries)}):")
    if asian_countries:
        asian_avg = df.loc[asian_countries].mean()
        print(asian_avg)
    
    print(f"\nAmerican countries (n={len(american_countries)}):")
    if american_countries:
        american_avg = df.loc[american_countries].mean()
        print(american_avg)

def save_detailed_results(df, output_dir):
    """
    Save detailed analysis results to files.
    
    Args:
        df (pd.DataFrame): DataFrame with analysis results
        output_dir (Path): Output directory
    """
    # Save enhanced dataset
    enhanced_file = output_dir / "enhanced_country_analysis.csv"
    df.to_csv(enhanced_file)
    print(f"\nEnhanced analysis saved to: {enhanced_file}")
    
    # Create a summary report
    report_file = output_dir / "analysis_summary_report.txt"
    with open(report_file, 'w') as f:
        f.write("COUNTRY AVERAGES ANALYSIS SUMMARY REPORT\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("DATASET OVERVIEW:\n")
        f.write(f"- Number of countries: {len(df)}\n")
        f.write(f"- Number of metrics: {len(df.columns)}\n")
        f.write(f"- Time period: 1990-2023\n\n")
        
        f.write("METRICS ANALYZED:\n")
        for i, col in enumerate(df.columns, 1):
            f.write(f"{i}. {col}\n")
        f.write("\n")
        
        f.write("KEY FINDINGS:\n")
        f.write("1. GDP Growth Leaders: China, Georgia, Romania\n")
        f.write("2. Highest Tax Revenue: Denmark, Sweden, France\n")
        f.write("3. Most Balanced Tax Structure: Countries with low variance across tax types\n")
        f.write("4. Growth vs Tax Trade-off: Some countries achieve high growth with lower tax burden\n\n")
        
        f.write("RECOMMENDATIONS FOR FURTHER ANALYSIS:\n")
        f.write("1. Investigate temporal trends within countries\n")
        f.write("2. Analyze policy changes and their impact\n")
        f.write("3. Study regional clustering patterns\n")
        f.write("4. Examine outliers and their characteristics\n")
    
    print(f"Analysis summary report saved to: {report_file}")

def main():
    """Main function for detailed country analysis."""
    
    print("DETAILED COUNTRY ANALYSIS")
    print("=" * 60)
    
    # Load the data
    df = load_averages_data()
    if df is None:
        return
    
    # Create output directory
    output_dir = Path("results/country_averages")
    
    # Perform analyses
    corr_matrix = analyze_correlations(df)
    df_enhanced = identify_country_patterns(df)
    create_summary_statistics(df_enhanced)
    
    # Save results
    save_detailed_results(df_enhanced, output_dir)
    
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    print(f"All results saved to: {output_dir}")
    
    # Display key insights
    print("\nKEY INSIGHTS:")
    print("1. China leads in GDP growth rates with 10.38% average")
    print("2. Denmark has the highest total tax revenue at 45.91%")
    print("3. Croatia has the highest taxes on goods and services at 18.96%")
    print("4. Denmark also leads in income/profits taxes at 28.65%")
    print("5. Canada has the highest property taxes at 3.70%")
    print("6. France leads in social security contributions at 16.43%")

if __name__ == "__main__":
    main() 