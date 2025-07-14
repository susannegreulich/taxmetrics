#!/usr/bin/env python3
"""
Simplified GDP per capita analysis: outputs only growth rates, statistics, and average growth rates per country.
"""

import pandas as pd
from pathlib import Path

def analyze_gdp_per_capita():
    """
    Analyze GDP per capita data and generate only the required results.
    """
    # Create results directory if it doesn't exist
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    # Read the GDP per capita data
    gdp_per_capita_file = Path("data/labeled/gdp_per_capita.csv")
    if not gdp_per_capita_file.exists():
        raise FileNotFoundError(f"GDP per capita file not found: {gdp_per_capita_file}")
    
    df = pd.read_csv(gdp_per_capita_file)
    
    # 1. Basic Statistics Summary
    stats_summary = {
        'total_records': len(df),
        'time_period_range': f"{df['TIME_PERIOD'].min()} - {df['TIME_PERIOD'].max()}",
        'number_of_countries': df['REF_AREA'].nunique(),
        'gdp_per_capita_min': df['value'].min(),
        'gdp_per_capita_max': df['value'].max(),
        'gdp_per_capita_mean': df['value'].mean(),
        'gdp_per_capita_median': df['value'].median(),
        'gdp_per_capita_std': df['value'].std()
    }
    stats_df = pd.DataFrame(list(stats_summary.items()), columns=['Metric', 'Value'])
    stats_df.to_csv(results_dir / "gdp_per_capita_statistics.csv", index=False)
    
    # 2. Growth analysis
    growth_data = []
    for country in df['REF_AREA'].unique():
        country_data = df[df['REF_AREA'] == country].sort_values('TIME_PERIOD')
        if len(country_data) > 1:
            country_data = country_data.reset_index(drop=True)
            for i in range(1, len(country_data)):
                current_year = country_data.iloc[i]['TIME_PERIOD']
                previous_year = country_data.iloc[i-1]['TIME_PERIOD']
                current_gdp = country_data.iloc[i]['value']
                previous_gdp = country_data.iloc[i-1]['value']
                if previous_gdp > 0:
                    growth_rate = ((current_gdp - previous_gdp) / previous_gdp) * 100
                    growth_data.append({
                        'country': country,
                        'year': current_year,
                        'growth_rate': growth_rate
                    })
    growth_df = pd.DataFrame(growth_data)
    if not growth_df.empty:
        growth_df.to_csv(results_dir / "gdp_per_capita_growth_rates.csv", index=False)
        # Average growth rates by country
        avg_growth = growth_df.groupby('country')['growth_rate'].mean().sort_values(ascending=False)
        avg_growth.to_csv(results_dir / "average_growth_rates_by_country.csv")
    print(f"Analysis completed! Results saved to {results_dir}/")
    return df

if __name__ == "__main__":
    try:
        result = analyze_gdp_per_capita()
        print("\nGDP per capita analysis completed successfully!")
    except Exception as e:
        print(f"Error in GDP per capita analysis: {e}")
        raise 