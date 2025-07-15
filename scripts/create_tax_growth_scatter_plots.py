#!/usr/bin/env python3
"""
Script to create scatter plots for GDP per capita growth rates against each tax type.
Uses country averages data to show the relationship between economic growth and tax structures.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def load_data(file_path):
    """Load the country averages data."""
    df = pd.read_csv(file_path)
    
    # Clean the data - remove rows with missing values
    df = df.dropna()
    
    # Also remove any rows where any tax column is 0 or negative (except for specific cases like SSC which can be 0)
    tax_columns = [col for col in df.columns if col not in ['Country', 'GDP per capita growth rates']]
    for col in tax_columns:
        if col != 'Social security contributions (SSC)':  # SSC can legitimately be 0
            df = df[df[col] > 0]
    
    return df

def create_scatter_plots(df, output_dir):
    """Create scatter plots for GDP growth rates against each tax type."""
    
    # Set up the plotting style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Define tax columns (excluding GDP growth rates and Country)
    tax_columns = [col for col in df.columns if col not in ['Country', 'GDP per capita growth rates']]
    
    # Create a figure with subplots
    n_cols = 2
    n_rows = (len(tax_columns) + 1) // 2
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5 * n_rows))
    fig.suptitle('GDP Per Capita Growth Rates vs Tax Types (Country Averages)', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    # Flatten axes for easier iteration
    if n_rows == 1:
        axes = axes.reshape(1, -1)
    axes = axes.flatten()
    
    for idx, tax_col in enumerate(tax_columns):
        ax = axes[idx]
        
        # Create scatter plot
        scatter = ax.scatter(df[tax_col], df['GDP per capita growth rates'], 
                           alpha=0.7, s=60, edgecolors='black', linewidth=0.5)
        
        # Add country labels for points
        for i, country in enumerate(df['Country']):
            ax.annotate(country, (df[tax_col].iloc[i], df['GDP per capita growth rates'].iloc[i]),
                       xytext=(5, 5), textcoords='offset points', fontsize=8, alpha=0.8)
        
        # Calculate correlation coefficient
        correlation = df[tax_col].corr(df['GDP per capita growth rates'])
        
        # Add trend line (with error handling)
        try:
            z = np.polyfit(df[tax_col], df['GDP per capita growth rates'], 1)
            p = np.poly1d(z)
            ax.plot(df[tax_col], p(df[tax_col]), "r--", alpha=0.8, linewidth=2)
        except (np.linalg.LinAlgError, ValueError) as e:
            print(f"Warning: Could not fit trend line for {tax_col}: {e}")
            correlation = np.nan
        
        # Customize the plot
        ax.set_xlabel(f'{tax_col} (% of GDP)', fontsize=12, fontweight='bold')
        ax.set_ylabel('GDP Per Capita Growth Rate (%)', fontsize=12, fontweight='bold')
        if not np.isnan(correlation):
            ax.set_title(f'{tax_col}\nCorrelation: {correlation:.3f}', 
                        fontsize=11, fontweight='bold')
        else:
            ax.set_title(f'{tax_col}\nCorrelation: N/A', 
                        fontsize=11, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Add correlation text
        if not np.isnan(correlation):
            ax.text(0.05, 0.95, f'r = {correlation:.3f}', transform=ax.transAxes, 
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8),
                   fontsize=10, fontweight='bold')
        else:
            ax.text(0.05, 0.95, 'r = N/A', transform=ax.transAxes, 
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8),
                   fontsize=10, fontweight='bold')
    
    # Hide empty subplots if any
    for idx in range(len(tax_columns), len(axes)):
        axes[idx].set_visible(False)
    
    # Adjust layout
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    
    # Save the plot
    output_path = output_dir / 'tax_growth_scatter_plots.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Scatter plots saved to: {output_path}")
    
    # Show the plot
    plt.show()
    
    return output_path

def create_individual_plots(df, output_dir):
    """Create individual scatter plots for each tax type."""
    
    # Use the main output directory directly (no subfolder)
    individual_dir = output_dir
    
    # Define tax columns
    tax_columns = [col for col in df.columns if col not in ['Country', 'GDP per capita growth rates']]
    
    for tax_col in tax_columns:
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Create scatter plot
        scatter = ax.scatter(df[tax_col], df['GDP per capita growth rates'], 
                           alpha=0.7, s=80, edgecolors='black', linewidth=0.5, c='steelblue')
        
        # Add country labels
        for i, country in enumerate(df['Country']):
            ax.annotate(country, (df[tax_col].iloc[i], df['GDP per capita growth rates'].iloc[i]),
                       xytext=(5, 5), textcoords='offset points', fontsize=9, alpha=0.8)
        
        # Calculate correlation
        correlation = df[tax_col].corr(df['GDP per capita growth rates'])
        
        # Add trend line (with error handling)
        try:
            z = np.polyfit(df[tax_col], df['GDP per capita growth rates'], 1)
            p = np.poly1d(z)
            ax.plot(df[tax_col], p(df[tax_col]), "r--", alpha=0.8, linewidth=2, label=f'Trend line')
        except (np.linalg.LinAlgError, ValueError) as e:
            print(f"Warning: Could not fit trend line for {tax_col}: {e}")
            correlation = np.nan
        
        # Customize plot
        ax.set_xlabel(f'{tax_col} (% of GDP)', fontsize=14, fontweight='bold')
        ax.set_ylabel('GDP Per Capita Growth Rate (%)', fontsize=14, fontweight='bold')
        if not np.isnan(correlation):
            ax.set_title(f'GDP Growth vs {tax_col}\nCorrelation: {correlation:.3f}', 
                        fontsize=16, fontweight='bold')
        else:
            ax.set_title(f'GDP Growth vs {tax_col}\nCorrelation: N/A', 
                        fontsize=16, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Add correlation info
        if not np.isnan(correlation):
            ax.text(0.05, 0.95, f'Correlation coefficient: {correlation:.3f}', 
                   transform=ax.transAxes, bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.9),
                   fontsize=12, fontweight='bold')
        else:
            ax.text(0.05, 0.95, 'Correlation coefficient: N/A', 
                   transform=ax.transAxes, bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.9),
                   fontsize=12, fontweight='bold')
        
        # Save individual plot
        safe_filename = tax_col.replace(' ', '_').replace(',', '').replace('(', '').replace(')', '')
        output_path = individual_dir / f'{safe_filename}_vs_gdp_growth.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Individual plot saved: {output_path}")
    
    return individual_dir

def generate_summary_statistics(df):
    """Generate summary statistics for correlations."""
    tax_columns = [col for col in df.columns if col not in ['Country', 'GDP per capita growth rates']]
    
    correlations = {}
    for tax_col in tax_columns:
        correlation = df[tax_col].corr(df['GDP per capita growth rates'])
        correlations[tax_col] = correlation
    
    # Create summary DataFrame
    summary_df = pd.DataFrame(list(correlations.items()), columns=['Tax Type', 'Correlation with GDP Growth'])
    summary_df = summary_df.sort_values('Correlation with GDP Growth', ascending=False)
    
    return summary_df

def main():
    """Main function to execute the script."""
    
    # Define paths
    data_file = Path('results/country_averages/all_metrics_country_averages.csv')
    output_dir = Path('results/country_averages')
    
    print("Loading country averages data...")
    df = load_data(data_file)
    
    print(f"Loaded data for {len(df)} countries")
    print(f"Tax types available: {[col for col in df.columns if col not in ['Country', 'GDP per capita growth rates']]}")
    
    # Create combined scatter plots
    print("\nCreating combined scatter plots...")
    create_scatter_plots(df, output_dir)
    
    # Create individual plots
    print("\nCreating individual scatter plots...")
    create_individual_plots(df, output_dir)
    
    # Generate summary statistics
    print("\nGenerating summary statistics...")
    summary_df = generate_summary_statistics(df)
    
    # Save summary statistics
    summary_path = output_dir / 'correlation_summary.csv'
    summary_df.to_csv(summary_path, index=False)
    print(f"Correlation summary saved to: {summary_path}")
    
    # Print summary
    print("\n" + "="*60)
    print("CORRELATION SUMMARY")
    print("="*60)
    print(summary_df.to_string(index=False))
    print("\n" + "="*60)
    
    print(f"\nAnalysis complete! Results saved to: {output_dir}")

if __name__ == "__main__":
    main() 