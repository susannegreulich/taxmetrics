#!/usr/bin/env python3
"""
Script to analyze unique values for each variable in OECD datasets.
This helps verify that the correct data was extracted from the API.
Shows EXHAUSTIVE lists of all unique values, not just samples.
"""

import pandas as pd
import os
from pathlib import Path
import json
from typing import Dict, List, Any

def analyze_dataset_unique_values(file_path: str) -> Dict[str, Any]:
    """
    Analyze unique values for each column in a dataset.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        Dictionary containing analysis results
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Get basic info
        total_rows = len(df)
        total_columns = len(df.columns)
        
        # Analyze each column (excluding VALUE column)
        column_analysis = {}
        
        for column in df.columns:
            # Skip the VALUE column as it contains numerical data we don't need to analyze
            if column.upper() == 'VALUE':
                continue
                
            unique_values = df[column].unique()
            unique_count = len(unique_values)
            
            # Get all unique values
            all_unique_values = unique_values.tolist()
            
            # Check for missing values
            missing_count = df[column].isnull().sum()
            missing_percentage = (missing_count / total_rows) * 100 if total_rows > 0 else 0
            
            # Get data type
            dtype = str(df[column].dtype)
            
            column_analysis[column] = {
                'unique_count': unique_count,
                'all_unique_values': all_unique_values,
                'missing_count': int(missing_count),
                'missing_percentage': round(missing_percentage, 2),
                'data_type': dtype
            }
        
        return {
            'file_path': file_path,
            'total_rows': total_rows,
            'total_columns': total_columns,
            'columns': column_analysis
        }
        
    except Exception as e:
        return {
            'file_path': file_path,
            'error': str(e)
        }

def print_analysis_results(analysis: Dict[str, Any], dataset_name: str):
    """
    Print formatted analysis results with EXHAUSTIVE lists of all unique values.
    
    Args:
        analysis: Analysis results dictionary
        dataset_name: Name of the dataset
    """
    print(f"\n{'='*80}")
    print(f"ANALYSIS RESULTS FOR {dataset_name.upper()}")
    print(f"{'='*80}")
    
    if 'error' in analysis:
        print(f"ERROR: {analysis['error']}")
        return
    
    print(f"File: {analysis['file_path']}")
    print(f"Total Rows: {analysis['total_rows']:,}")
    print(f"Total Columns: {analysis['total_columns']}")
    print()
    
    for column, info in analysis['columns'].items():
        print(f"Column: {column}")
        print(f"  Data Type: {info['data_type']}")
        print(f"  Unique Values: {info['unique_count']:,}")
        print(f"  Missing Values: {info['missing_count']:,} ({info['missing_percentage']}%)")
        
        # Always show all unique values, sorted for readability
        all_values = sorted(info['all_unique_values'])
        if info['unique_count'] <= 50:
            print(f"  All Unique Values: {all_values}")
        else:
            print(f"  All Unique Values ({info['unique_count']:,} total):")
            # Print in columns for better readability
            for i in range(0, len(all_values), 5):
                chunk = all_values[i:i+5]
                print(f"    {chunk}")
        
        print()

def save_analysis_to_json(analyses: Dict[str, Dict], output_file: str):
    """
    Save analysis results to JSON file.
    
    Args:
        analyses: Dictionary of analysis results
        output_file: Output file path
    """
    # Convert numpy types to native Python types for JSON serialization
    def convert_numpy_types(obj):
        if isinstance(obj, dict):
            return {k: convert_numpy_types(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_numpy_types(item) for item in obj]
        elif hasattr(obj, 'item'):  # numpy types
            return obj.item()
        else:
            return obj
    
    converted_analyses = convert_numpy_types(analyses)
    
    with open(output_file, 'w') as f:
        json.dump(converted_analyses, f, indent=2, default=str)
    
    print(f"\nAnalysis results saved to: {output_file}")

def main():
    """Main function to analyze all datasets."""
    # Define data directory and files
    data_dir = Path("data")
    
    # List of datasets to analyze (labeled versions)
    datasets = [
        ("tax_revenues_labeled.csv", "Tax Revenues Labeled Data"),
        ("gdp_labeled.csv", "GDP Labeled Data"), 
        ("labor_force_labeled.csv", "Labor Force Labeled Data")
    ]
    
    print("OECD Dataset Unique Values Analysis")
    print("=" * 50)
    print("This script analyzes unique values for each variable in the labeled OECD datasets")
    print("to help verify that the correct data was extracted from the API.")
    print("EXHAUSTIVE lists of all unique values will be shown.")
    print()
    
    all_analyses = {}
    
    for filename, dataset_name in datasets:
        file_path = data_dir / filename
        
        if not file_path.exists():
            print(f"WARNING: File {file_path} not found, skipping...")
            continue
        
        print(f"Analyzing {dataset_name}...")
        analysis = analyze_dataset_unique_values(str(file_path))
        all_analyses[dataset_name] = analysis
        
        # Print results
        print_analysis_results(analysis, dataset_name)
    
    # Save results to JSON file
    output_file = "results/unique_values_analysis_labeled.json"
    os.makedirs("results", exist_ok=True)
    save_analysis_to_json(all_analyses, output_file)
    
    # Print summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    for dataset_name, analysis in all_analyses.items():
        if 'error' not in analysis:
            print(f"{dataset_name}:")
            print(f"  - {analysis['total_rows']:,} rows, {analysis['total_columns']} columns")
            print(f"  - Columns: {', '.join(analysis['columns'].keys())}")
        else:
            print(f"{dataset_name}: ERROR - {analysis['error']}")
        print()

if __name__ == "__main__":
    main() 