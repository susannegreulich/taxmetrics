#!/usr/bin/env python3
"""
Example script demonstrating how to use the generated 2D CSV files.

This script shows how to load and analyze the 2D tax rate CSV files
that were created by create_tax_rate_2d_csvs.py.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def load_and_analyze_2d_csv(tax_type_name):
    """Load and analyze a 2D CSV file for a specific tax type."""
    
    # Construct filename
    safe_tax_type = tax_type_name.replace(' ', '_').replace(',', '').replace('(', '').replace(')', '').replace('&', 'and')
    filename = f"results/tax_rate_2d_csvs/{safe_tax_type}.csv"
    
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return None
    
    # Load the 2D CSV
    df = pd.read_csv(filename, index_col=0)
    df.index.name = 'Year'
    
    print(f"\n=== Analysis for {tax_type_name} ===")
    print(f"Shape: {df.shape} (years: {len(df)}, countries: {len(df.columns)})")
    print(f"Year range: {df.index.min()} - {df.index.max()}")
    print(f"Data coverage: {df.notna().sum().sum() / df.size * 100:.1f}%")
    
    # Basic statistics
    print(f"\nOverall statistics:")
    print(f"  Mean: {df.mean().mean():.2f}%")
    print(f"  Median: {df.median().median():.2f}%")
    print(f"  Min: {df.min().min():.2f}%")
    print(f"  Max: {df.max().max():.2f}%")
    
    # Top 5 countries by average rate
    country_means = df.mean().sort_values(ascending=False)
    print(f"\nTop 5 countries by average rate:")
    for i, (country, mean_rate) in enumerate(country_means.head().items(), 1):
        print(f"  {i}. {country}: {mean_rate:.2f}%")
    
    # Bottom 5 countries by average rate
    print(f"\nBottom 5 countries by average rate:")
    for i, (country, mean_rate) in enumerate(country_means.tail().items(), 1):
        print(f"  {i}. {country}: {mean_rate:.2f}%")
    
    return df

def plot_tax_evolution(df, tax_type_name, countries=None):
    """Plot the evolution of tax rates over time for selected countries."""
    
    if countries is None:
        # Select top 5 countries by average rate
        countries = df.mean().sort_values(ascending=False).head().index.tolist()
    
    # Filter data for selected countries
    plot_data = df[countries].copy()
    
    # Create the plot
    plt.figure(figsize=(12, 8))
    
    for country in countries:
        if country in plot_data.columns:
            plt.plot(plot_data.index, plot_data[country], marker='o', label=country, linewidth=2, markersize=4)
    
    plt.title(f'Evolution of {tax_type_name} Over Time', fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Tax Rate (%)', fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save the plot
    safe_tax_type = tax_type_name.replace(' ', '_').replace(',', '').replace('(', '').replace(')', '').replace('&', 'and')
    plot_filename = f"results/tax_rate_2d_csvs/{safe_tax_type}_evolution.png"
    plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
    print(f"Plot saved as: {plot_filename}")
    
    plt.show()

def compare_tax_types():
    """Compare different tax types across countries."""
    
    tax_types = [
        "Social security contributions (SSC)",
        "Taxes on property", 
        "Taxes on income, profits and capital gains of individuals and corporations",
        "Total tax revenue",
        "Taxes on goods and services"
    ]
    
    # Load data for all tax types
    tax_data = {}
    for tax_type in tax_types:
        df = load_and_analyze_2d_csv(tax_type)
        if df is not None:
            tax_data[tax_type] = df
    
    # Compare average rates across tax types
    print("\n=== Comparison of Average Tax Rates Across Types ===")
    comparison_data = []
    for tax_type, df in tax_data.items():
        avg_rate = df.mean().mean()
        comparison_data.append({
            'Tax Type': tax_type,
            'Average Rate (%)': avg_rate
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    comparison_df = comparison_df.sort_values('Average Rate (%)', ascending=False)
    
    for _, row in comparison_df.iterrows():
        print(f"  {row['Tax Type']}: {row['Average Rate (%)']:.2f}%")
    
    # Save comparison to CSV
    comparison_df.to_csv("results/tax_rate_2d_csvs/tax_type_comparison.csv", index=False)
    print(f"\nComparison saved to: results/tax_rate_2d_csvs/tax_type_comparison.csv")

def main():
    """Main function demonstrating usage of 2D CSV files."""
    
    print("Tax Rate 2D CSV Analysis Examples")
    print("=" * 50)
    
    # Example 1: Analyze total tax revenue
    print("\n1. Analyzing Total Tax Revenue...")
    total_tax_df = load_and_analyze_2d_csv("Total tax revenue")
    
    if total_tax_df is not None:
        # Plot evolution for top 5 countries
        plot_tax_evolution(total_tax_df, "Total tax revenue")
    
    # Example 2: Analyze social security contributions
    print("\n2. Analyzing Social Security Contributions...")
    ssc_df = load_and_analyze_2d_csv("Social security contributions (SSC)")
    
    if ssc_df is not None:
        # Plot evolution for specific countries
        selected_countries = ['France', 'Germany', 'Sweden', 'Denmark', 'Netherlands']
        plot_tax_evolution(ssc_df, "Social security contributions (SSC)", selected_countries)
    
    # Example 3: Compare all tax types
    print("\n3. Comparing All Tax Types...")
    compare_tax_types()
    
    print("\n" + "=" * 50)
    print("Analysis complete! Check the results/tax_rate_2d_csvs/ directory for all generated files.")

if __name__ == "__main__":
    main() 