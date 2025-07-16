#!/usr/bin/env python3
"""
Script to create interactive HTML graphs for all 2D CSV files in the results/over_time directory.
Creates graphs with all countries in different colors by default, plus dropdown buttons
to select individual countries.
Also creates scatter plots for GDP per capita growth rates against each tax type.
Uses country averages data to show the relationship between economic growth and tax structures.
"""

import pandas as pd
import os
from pathlib import Path
import plotly.graph_objs as go
import plotly.offline as pyo
from plotly.subplots import make_subplots
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


def is_time_series_csv(csv_file):
    """
    Check if a CSV file contains time series data (has TIME_PERIOD column).
    
    Args:
        csv_file (Path): Path to the CSV file
        
    Returns:
        bool: True if the file contains time series data, False otherwise
    """
    try:
        df = pd.read_csv(csv_file)
        return 'TIME_PERIOD' in df.columns
    except Exception:
        return False

def create_interactive_graph(csv_file, output_dir, title_prefix="", y_axis_title="Value"):
    """
    Create an interactive HTML graph for a 2D CSV file.
    
    Args:
        csv_file (Path): Path to the CSV file
        output_dir (Path): Directory to save the HTML file
        title_prefix (str): Prefix for the graph title
        y_axis_title (str): Title for the y-axis
    """
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Check if this is a time series file
    if 'TIME_PERIOD' not in df.columns:
        print(f"Skipping {csv_file.name}: Not a time series file (no TIME_PERIOD column)")
        return None
    
    # Get the filename without extension for the output HTML file
    csv_name = csv_file.stem
    html_output_file = output_dir / f"{csv_name}.html"
    
    # Prepare data for Plotly
    countries = list(df.columns)
    countries.remove('TIME_PERIOD')
    years = df['TIME_PERIOD']
    
    # Create traces for all countries (all visible by default)
    traces = []
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
              '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
              '#a6cee3', '#fb9a99', '#fdbf6f', '#cab2d6', '#ffff99',
              '#b15928', '#fbb4ae', '#b3cde3', '#ccebc5', '#decbe4']
    
    for i, country in enumerate(countries):
        color = colors[i % len(colors)]
        trace = go.Scatter(
            x=years,
            y=df[country],
            mode='lines+markers',
            name=country,
            line=dict(color=color, width=2),
            marker=dict(size=6),
            visible=True  # All countries visible by default
        )
        traces.append(trace)
    
    # Create dropdown buttons for individual country selection
    buttons = []
    
    # Button for "All Countries" view
    buttons.append(dict(
        label="All Countries",
        method='update',
        args=[{'visible': [True] * len(countries)}, 
              {'title': f'{title_prefix} Over Time: All Countries'}]
    ))
    
    # Buttons for individual countries
    for i, country in enumerate(countries):
        visible = [False] * len(countries)
        visible[i] = True
        buttons.append(dict(
            label=country,
            method='update',
            args=[{'visible': visible}, 
                  {'title': f'{title_prefix} Over Time: {country}'}]
        ))
    
    # Create layout
    layout = go.Layout(
        title=f'{title_prefix} Over Time: All Countries',
        xaxis=dict(title='Year'),
        yaxis=dict(title=y_axis_title),
        updatemenus=[dict(
            active=0,
            buttons=buttons,
            x=1.15,
            y=1.15,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='black',
            borderwidth=1
        )],
        hovermode='x unified',
        legend=dict(
            orientation='v',
            x=1.05,  # Move legend to the right outside the plot area
            y=1,
            xanchor='left',
            yanchor='top',
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='black',
            borderwidth=1
        ),
        margin=dict(r=250),  # Add right margin for the legend
        width=1200,
        height=600
    )
    
    # Create figure and save
    fig = go.Figure(data=traces, layout=layout)
    pyo.plot(fig, filename=str(html_output_file), auto_open=False)
    
    print(f"Created interactive graph: {html_output_file}")
    return html_output_file

def create_all_interactive_graphs():
    """
    Create interactive HTML graphs for all 2D CSV files in the results/over_time directory.
    """
    results_dir = Path("results")
    over_time_dir = results_dir / "over_time"
    
    # Ensure results and over_time directories exist
    results_dir.mkdir(exist_ok=True)
    over_time_dir.mkdir(exist_ok=True)
    
    # Check if over_time directory exists
    if not over_time_dir.exists():
        print(f"Warning: Directory {over_time_dir} does not exist")
        return []
    
    # Get all CSV files in the over_time directory
    csv_files = list(over_time_dir.glob("*.csv"))
    
    if not csv_files:
        print(f"No CSV files found in {over_time_dir}")
        return []
    
    # Filter for time series files only
    time_series_files = [f for f in csv_files if is_time_series_csv(f)]
    
    print(f"Found {len(csv_files)} CSV files, {len(time_series_files)} are time series files")
    
    if not time_series_files:
        print(f"No time series CSV files found in {over_time_dir}")
        return []
    
    # Create configurations for all time series CSV files
    csv_configs = []
    for csv_file in time_series_files:
        # Create a nice title from the filename using new naming convention
        if csv_file.stem == "social_security":
            title = "Social Security"
        elif csv_file.stem == "goods_tax":
            title = "Taxes on Goods and Services"
        elif csv_file.stem == "income_tax":
            title = "Taxes on Income, Profits and Capital Gains"
        elif csv_file.stem == "property_tax":
            title = "Taxes on Property"
        elif csv_file.stem == "total_tax":
            title = "Total Tax Revenue"
        else:
            # Fallback for other files
            title = csv_file.stem.replace('_', ' ').title()
        
        # Determine y-axis title based on file content
        y_axis_title = "Value"  # Default
        if "gdp" in csv_file.name.lower():
            if "growth" in csv_file.name.lower():
                y_axis_title = "Growth Rate (%)"
            else:
                y_axis_title = "GDP per Capita (PPP-adjusted USD in current prices)"
        elif "tax" in csv_file.name.lower() or "social_security" in csv_file.name.lower():
            y_axis_title = "Tax Rate (% of GDP)"
        elif "revenue" in csv_file.name.lower():
            y_axis_title = "Revenue (% of GDP)"
        
        csv_configs.append({
            'file': csv_file,
            'title_prefix': title,
            'y_axis_title': y_axis_title
        })
    
    # Process each CSV file
    created_files = []
    for config in csv_configs:
        csv_file = config['file']
        
        if not csv_file.exists():
            print(f"Warning: CSV file not found: {csv_file}")
            continue
        
        try:
            # Create the interactive graph
            html_file = create_interactive_graph(
                csv_file=csv_file,
                output_dir=over_time_dir,
                title_prefix=config['title_prefix'],
                y_axis_title=config['y_axis_title']
            )
            if html_file:
                created_files.append(html_file)
            
        except Exception as e:
            print(f"Error creating graph for {csv_file}: {e}")
    
    # Print summary
    print(f"\nSummary:")
    print(f"Successfully created {len(created_files)} interactive HTML graphs:")
    for html_file in created_files:
        print(f"  - {html_file.name}")
    
    return created_files



def load_country_averages_data(file_path):
    """Load the country averages data."""
    df = pd.read_csv(file_path)
    
    # Clean the data - remove rows with missing values
    df = df.dropna()
    
    # Also remove any rows where any tax column is 0 or negative (except for specific cases like social security which can be 0)
    tax_columns = [col for col in df.columns if col not in ['Country', 'GDP per capita growth rates']]
    for col in tax_columns:
        if col != 'Social security contributions':  # Social security can legitimately be 0
            df = df[df[col] > 0]
    
    return df

def create_tax_growth_scatter_plots(df, output_dir):
    """Create scatter plots for GDP growth rates against each tax type and GDP per capita."""
    
    # Set up the plotting style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Define tax columns (excluding GDP growth rates, Country, and GDP per capita)
    tax_columns = [col for col in df.columns if col not in ['Country', 'GDP per capita growth rates', 'GDP per capita']]
    
    # Create a list of all plots: GDP per capita first, then tax types
    all_plots = [('GDP per capita', 'GDP per capita')] + [(tax_col, tax_col) for tax_col in tax_columns]
    
    # Create a figure with subplots
    n_cols = 2
    n_rows = (len(all_plots) + 1) // 2
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 6 * n_rows))  # Made taller: 6 * n_rows instead of 5
    fig.suptitle('GDP Per Capita Growth Rates vs Economic Indicators (Country Averages)', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    # Flatten axes for easier iteration
    if n_rows == 1:
        axes = axes.reshape(1, -1)
    axes = axes.flatten()
    
    for idx, (plot_name, column_name) in enumerate(all_plots):
        ax = axes[idx]
        
        # Create scatter plot
        if plot_name == 'GDP per capita':
            # GDP per capita vs growth rates plot
            scatter = ax.scatter(df[column_name], df['GDP per capita growth rates'], 
                               alpha=0.7, s=60, edgecolors='black', linewidth=0.5)
            
            # Add country labels for points
            for i, country in enumerate(df['Country']):
                ax.annotate(country, (df[column_name].iloc[i], df['GDP per capita growth rates'].iloc[i]),
                           xytext=(5, 5), textcoords='offset points', fontsize=8, alpha=0.8)
            
            # Calculate correlation coefficient
            correlation = df[column_name].corr(df['GDP per capita growth rates'])
            
            # Add trend line (with error handling)
            try:
                z = np.polyfit(df[column_name], df['GDP per capita growth rates'], 1)
                p = np.poly1d(z)
                ax.plot(df[column_name], p(df[column_name]), "r--", alpha=0.8, linewidth=2)
            except (np.linalg.LinAlgError, ValueError) as e:
                print(f"Warning: Could not fit trend line for {plot_name}: {e}")
                correlation = np.nan
            
            # Customize the plot for GDP per capita
            ax.set_xlabel('GDP per Capita (PPP-adjusted USD in current prices)', fontsize=12, fontweight='bold')
            ax.set_ylabel('GDP Per Capita Growth Rate (%)', fontsize=12, fontweight='bold')
            if not np.isnan(correlation):
                ax.set_title(f'GDP per capita\nCorrelation: {correlation:.3f}', 
                            fontsize=11, fontweight='bold')
            else:
                ax.set_title(f'GDP per capita\nCorrelation: N/A', 
                            fontsize=11, fontweight='bold')
        else:
            # Tax type vs growth rates plot
            scatter = ax.scatter(df[column_name], df['GDP per capita growth rates'], 
                               alpha=0.7, s=60, edgecolors='black', linewidth=0.5)
            
            # Add country labels for points
            for i, country in enumerate(df['Country']):
                ax.annotate(country, (df[column_name].iloc[i], df['GDP per capita growth rates'].iloc[i]),
                           xytext=(5, 5), textcoords='offset points', fontsize=8, alpha=0.8)
            
            # Calculate correlation coefficient
            correlation = df[column_name].corr(df['GDP per capita growth rates'])
            
            # Add trend line (with error handling)
            try:
                z = np.polyfit(df[column_name], df['GDP per capita growth rates'], 1)
                p = np.poly1d(z)
                ax.plot(df[column_name], p(df[column_name]), "r--", alpha=0.8, linewidth=2)
            except (np.linalg.LinAlgError, ValueError) as e:
                print(f"Warning: Could not fit trend line for {plot_name}: {e}")
                correlation = np.nan
            
            # Customize the plot for tax types
            ax.set_xlabel(f'{column_name} (% of GDP)', fontsize=12, fontweight='bold')
            ax.set_ylabel('GDP Per Capita Growth Rate (%)', fontsize=12, fontweight='bold')
            if not np.isnan(correlation):
                ax.set_title(f'{column_name}\nCorrelation: {correlation:.3f}', 
                            fontsize=11, fontweight='bold')
            else:
                ax.set_title(f'{column_name}\nCorrelation: N/A', 
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
    for idx in range(len(all_plots), len(axes)):
        axes[idx].set_visible(False)
    
    # Adjust layout with more space for title
    plt.tight_layout()
    plt.subplots_adjust(top=0.92)  # Reduced from 0.95 to give more space for title
    
    # Save the plot
    output_path = output_dir / 'all_scatter_plots.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Combined scatter plots saved to: {output_path}")
    
    # Show the plot
    plt.show()
    
    return output_path

def create_individual_tax_plots(df, output_dir):
    """Create individual scatter plots for each tax type."""
    
    # Use the main output directory directly (no subfolder)
    individual_dir = output_dir
    
    # Define tax columns (exclude GDP per capita as it's not a tax type)
    tax_columns = [col for col in df.columns if col not in ['Country', 'GDP per capita growth rates', 'GDP per capita']]
    
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
        
        # Save individual plot with new naming convention
        if tax_col == "Social security contributions":
            safe_filename = "social_security"
        elif tax_col == "Taxes on goods and services":
            safe_filename = "goods_tax"
        elif tax_col == "Taxes on income, profits, and capital gains":
            safe_filename = "income_tax"
        elif tax_col == "Taxes on property":
            safe_filename = "property_tax"
        elif tax_col == "Total tax revenue":
            safe_filename = "total_tax"
        else:
            # Fallback for any other tax types
            safe_filename = tax_col.replace(' ', '_').replace(',', '').replace('(', '').replace(')', '')
        
        output_path = individual_dir / f'{safe_filename}_vs_gdp_growth.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Individual plot saved: {output_path}")
    
    return individual_dir

def create_gdp_per_capita_vs_growth_plot(df, output_dir):
    """Create a scatter plot for GDP per capita vs GDP growth rates."""
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create scatter plot
    scatter = ax.scatter(df['GDP per capita'], df['GDP per capita growth rates'], 
                       alpha=0.7, s=80, edgecolors='black', linewidth=0.5, c='steelblue')
    
    # Add country labels
    for i, country in enumerate(df['Country']):
        ax.annotate(country, (df['GDP per capita'].iloc[i], df['GDP per capita growth rates'].iloc[i]),
                   xytext=(5, 5), textcoords='offset points', fontsize=9, alpha=0.8)
    
    # Calculate correlation
    correlation = df['GDP per capita'].corr(df['GDP per capita growth rates'])
    
    # Add trend line (with error handling)
    try:
        z = np.polyfit(df['GDP per capita'], df['GDP per capita growth rates'], 1)
        p = np.poly1d(z)
        ax.plot(df['GDP per capita'], p(df['GDP per capita']), "r--", alpha=0.8, linewidth=2, label='Trend line')
    except (np.linalg.LinAlgError, ValueError) as e:
        print(f"Warning: Could not fit trend line for GDP per capita vs growth rates: {e}")
        correlation = np.nan
    
    # Customize plot with correct units
    ax.set_xlabel('GDP per Capita (PPP-adjusted USD in current prices)', fontsize=14, fontweight='bold')
    ax.set_ylabel('GDP Per Capita Growth Rate (%)', fontsize=14, fontweight='bold')
    if not np.isnan(correlation):
        ax.set_title(f'GDP Per Capita vs Growth Rates\nCorrelation: {correlation:.3f}', 
                    fontsize=16, fontweight='bold')
    else:
        ax.set_title(f'GDP Per Capita vs Growth Rates\nCorrelation: N/A', 
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
    
    # Save the plot
    output_path = output_dir / 'GDP_per_capita_vs_gdp_growth.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"GDP per capita vs growth rates plot saved: {output_path}")
    return output_path

def generate_tax_correlation_summary(df):
    """Generate summary statistics for correlations."""
    tax_columns = [col for col in df.columns if col not in ['Country', 'GDP per capita growth rates', 'GDP per capita']]
    
    correlations = {}
    for tax_col in tax_columns:
        correlation = df[tax_col].corr(df['GDP per capita growth rates'])
        correlations[tax_col] = correlation
    
    # Create summary DataFrame
    summary_df = pd.DataFrame(list(correlations.items()), columns=['Tax Type', 'Correlation with GDP Growth'])
    summary_df = summary_df.sort_values('Correlation with GDP Growth', ascending=False)
    
    return summary_df

def create_tax_growth_analysis():
    """Create scatter plots for GDP per capita growth rates against each tax type."""
    
    # Define paths
    data_file = Path('results/averages/all_metrics_country_averages.csv')
    output_dir = Path('results/averages')
    
    # Ensure averages directory exists
    output_dir.mkdir(exist_ok=True)
    
    # Check if the data file exists
    if not data_file.exists():
        print(f"Warning: Country averages data file not found: {data_file}")
        print("Skipping tax-growth scatter plot analysis.")
        return
    
    print("Loading country averages data...")
    df = load_country_averages_data(data_file)
    
    print(f"Loaded data for {len(df)} countries")
    print(f"Tax types available: {[col for col in df.columns if col not in ['Country', 'GDP per capita growth rates']]}")
    
    # Create combined scatter plots
    print("\nCreating combined scatter plots...")
    create_tax_growth_scatter_plots(df, output_dir)
    
    # Create individual plots
    print("\nCreating individual scatter plots...")
    create_individual_tax_plots(df, output_dir)
    
    # Create GDP per capita vs growth rates plot
    print("\nCreating GDP per capita vs growth rates plot...")
    create_gdp_per_capita_vs_growth_plot(df, output_dir)
    
    # Generate summary statistics
    print("\nGenerating summary statistics...")
    summary_df = generate_tax_correlation_summary(df)
    
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
    
    print(f"\nTax-growth analysis complete! Results saved to: {output_dir}")

if __name__ == "__main__":
    try:
        print("Creating interactive HTML graphs for all CSV files in results/over_time...")
        created_files = create_all_interactive_graphs()
        
        print("\nCreating tax-growth scatter plot analysis...")
        create_tax_growth_analysis()
        
        print("\nAll visualizations created successfully!")
        print(f"Total interactive HTML files created: {len(created_files)}")
        
    except Exception as e:
        print(f"Error creating visualizations: {e}")
        raise 