#!/usr/bin/env python3
"""
Script to create interactive HTML graphs for all 2D CSV files in the results directory.
Creates graphs with all countries in different colors by default, plus dropdown buttons
to select individual countries.
"""

import pandas as pd
import os
from pathlib import Path
import plotly.graph_objs as go
import plotly.offline as pyo
from plotly.subplots import make_subplots
import numpy as np

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
    
    # Get the filename without extension for the output HTML file
    csv_name = csv_file.stem
    html_output_file = output_dir / f"{csv_name}_interactive.html"
    
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
    Create interactive HTML graphs for all 2D CSV files in the results directory.
    """
    results_dir = Path("results")
    tax_rate_dir = results_dir / "tax_rate_2d_csvs"
    
    # Ensure results directory exists
    results_dir.mkdir(exist_ok=True)
    
    # List of CSV files to process with their configurations
    csv_configs = [
        {
            'file': results_dir / "gdp_per_capita.csv",
            'title_prefix': "GDP per Capita",
            'y_axis_title': "GDP per Capita"
        },
        {
            'file': results_dir / "gdp_per_capita_growth_rates.csv",
            'title_prefix': "GDP per Capita Growth Rate",
            'y_axis_title': "Growth Rate (%)"
        }
    ]
    
    # Add tax rate CSV files
    if tax_rate_dir.exists():
        tax_csv_files = list(tax_rate_dir.glob("*.csv"))
        for csv_file in tax_csv_files:
            # Skip summary files
            if "summary" in csv_file.name.lower() or "comparison" in csv_file.name.lower():
                continue
            
            # Create a nice title from the filename
            title = csv_file.stem.replace('_', ' ').title()
            csv_configs.append({
                'file': csv_file,
                'title_prefix': title,
                'y_axis_title': "Tax Rate (%)"
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
                output_dir=results_dir,
                title_prefix=config['title_prefix'],
                y_axis_title=config['y_axis_title']
            )
            created_files.append(html_file)
            
        except Exception as e:
            print(f"Error creating graph for {csv_file}: {e}")
    
    # Print summary
    print(f"\nSummary:")
    print(f"Successfully created {len(created_files)} interactive HTML graphs:")
    for html_file in created_files:
        print(f"  - {html_file.name}")
    
    return created_files

def create_summary_dashboard():
    """
    Create a summary dashboard that shows key statistics for all datasets.
    """
    results_dir = Path("results")
    tax_rate_dir = results_dir / "tax_rate_2d_csvs"
    
    # Read main datasets
    datasets = {}
    
    # GDP per capita
    gdp_file = results_dir / "gdp_per_capita.csv"
    if gdp_file.exists():
        gdp_df = pd.read_csv(gdp_file)
        gdp_df = gdp_df.set_index('TIME_PERIOD')
        datasets['GDP per Capita'] = gdp_df
    
    # GDP per capita growth rates
    growth_file = results_dir / "gdp_per_capita_growth_rates.csv"
    if growth_file.exists():
        growth_df = pd.read_csv(growth_file)
        growth_df = growth_df.set_index('TIME_PERIOD')
        datasets['GDP Growth Rate (%)'] = growth_df
    
    # Tax rate datasets
    if tax_rate_dir.exists():
        tax_csv_files = list(tax_rate_dir.glob("*.csv"))
        for csv_file in tax_csv_files:
            if "summary" in csv_file.name.lower() or "comparison" in csv_file.name.lower():
                continue
            
            title = csv_file.stem.replace('_', ' ').title()
            df = pd.read_csv(csv_file)
            df = df.set_index('TIME_PERIOD')
            datasets[title] = df
    
    # Create summary statistics
    summary_data = []
    for dataset_name, df in datasets.items():
        countries = list(df.columns)
        years = list(df.index)
        
        # Calculate statistics
        all_values = df.values.flatten()
        valid_values = all_values[~np.isnan(all_values)]
        
        if len(valid_values) > 0:
            summary_data.append({
                'Dataset': dataset_name,
                'Countries': len(countries),
                'Years': len(years),
                'Min Value': f"{valid_values.min():.2f}",
                'Max Value': f"{valid_values.max():.2f}",
                'Mean Value': f"{valid_values.mean():.2f}",
                'Std Dev': f"{valid_values.std():.2f}"
            })
    
    # Create summary table
    if summary_data:
        summary_df = pd.DataFrame(summary_data)
        summary_file = results_dir / "dataset_summary.csv"
        summary_df.to_csv(summary_file, index=False)
        print(f"Created dataset summary: {summary_file}")
        
        # Create HTML table
        html_table = summary_df.to_html(index=False, classes='table table-striped')
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dataset Summary</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .table {{ border-collapse: collapse; width: 100%; }}
                .table th, .table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                .table th {{ background-color: #f2f2f2; }}
                .table tr:nth-child(even) {{ background-color: #f9f9f9; }}
                h1 {{ color: #333; }}
            </style>
        </head>
        <body>
            <h1>Dataset Summary</h1>
            {html_table}
        </body>
        </html>
        """
        
        summary_html_file = results_dir / "dataset_summary.html"
        with open(summary_html_file, 'w') as f:
            f.write(html_content)
        print(f"Created dataset summary HTML: {summary_html_file}")

if __name__ == "__main__":
    try:
        print("Creating interactive HTML graphs for all 2D CSV files...")
        created_files = create_all_interactive_graphs()
        
        print("\nCreating summary dashboard...")
        create_summary_dashboard()
        
        print("\nAll interactive graphs created successfully!")
        print(f"Total files created: {len(created_files)}")
        
    except Exception as e:
        print(f"Error creating interactive graphs: {e}")
        raise 