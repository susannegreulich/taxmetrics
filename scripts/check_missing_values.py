#!/usr/bin/env python3
"""
Script to check for missing values in all CSV files in the filtered folder.
Returns counts and locations of missing values for each file.
"""

import pandas as pd
import os
import glob
from pathlib import Path

def check_missing_values(csv_file_path):
    """
    Check for missing values in a CSV file and return detailed information.
    
    Args:
        csv_file_path (str): Path to the CSV file
        
    Returns:
        dict: Dictionary containing missing value information
    """
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file_path)
        
        # Get basic file info
        file_info = {
            'file_name': os.path.basename(csv_file_path),
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'total_cells': len(df) * len(df.columns)
        }
        
        # Check for missing values
        missing_info = df.isnull()
        total_missing = missing_info.sum().sum()
        
        # Get missing value counts by column
        missing_by_column = df.isnull().sum()
        missing_by_column = missing_by_column[missing_by_column > 0].to_dict()
        
        # Get missing value counts by row
        missing_by_row = df.isnull().sum(axis=1)
        missing_by_row = missing_by_row[missing_by_row > 0].to_dict()
        
        # Find specific locations of missing values
        missing_locations = []
        for row_idx, row in missing_info.iterrows():
            for col_idx, is_missing in row.items():
                if is_missing:
                    missing_locations.append({
                        'row': row_idx,
                        'column': col_idx,
                        'row_label': df.index[row_idx] if row_idx < len(df.index) else f"Row_{row_idx}",
                        'column_label': col_idx
                    })
        
        # Calculate percentages
        missing_percentage = (total_missing / file_info['total_cells']) * 100 if file_info['total_cells'] > 0 else 0
        
        return {
            'file_info': file_info,
            'total_missing': total_missing,
            'missing_percentage': missing_percentage,
            'missing_by_column': missing_by_column,
            'missing_by_row': missing_by_row,
            'missing_locations': missing_locations,
            'columns_with_missing': len(missing_by_column),
            'rows_with_missing': len(missing_by_row)
        }
        
    except Exception as e:
        return {
            'file_name': os.path.basename(csv_file_path),
            'error': str(e)
        }

def main():
    """Main function to check all CSV files in the filtered folder."""
    
    # Define the path to the filtered folder
    filtered_folder = Path("data/filtered")
    
    # Check if the folder exists
    if not filtered_folder.exists():
        print(f"Error: Folder {filtered_folder} does not exist!")
        return
    
    # Find all CSV files in the filtered folder
    csv_files = list(filtered_folder.glob("*.csv"))
    
    if not csv_files:
        print(f"No CSV files found in {filtered_folder}")
        return
    
    print(f"Found {len(csv_files)} CSV file(s) in {filtered_folder}")
    print("Processing...")
    
    # Check each CSV file
    all_results = []
    
    for csv_file in csv_files:
        result = check_missing_values(str(csv_file))
        
        if 'error' in result:
            print(f"Error processing {csv_file.name}: {result['error']}")
            continue
        
        all_results.append(result)
    
    # Generate markdown report
    report_content = generate_markdown_report(all_results, csv_files)
    
    # Save markdown report
    report_file = "data/filtered/missing_values_report.md"
    os.makedirs("data/filtered", exist_ok=True)
    
    with open(report_file, 'w') as f:
        f.write(report_content)
    
    print(f"Report saved to: {report_file}")
    
    # Save detailed results to CSV as well
    output_file = "data/filtered/missing_values_summary.csv"
    
    summary_data = []
    for result in all_results:
        summary_data.append({
            'file_name': result['file_info']['file_name'],
            'total_rows': result['file_info']['total_rows'],
            'total_columns': result['file_info']['total_columns'],
            'total_cells': result['file_info']['total_cells'],
            'missing_values': result['total_missing'],
            'missing_percentage': result['missing_percentage'],
            'columns_with_missing': result['columns_with_missing'],
            'rows_with_missing': result['rows_with_missing']
        })
    
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_csv(output_file, index=False)
    print(f"CSV summary saved to: {output_file}")


def generate_markdown_report(all_results, csv_files):
    """Generate a markdown report from the missing values analysis."""
    
    report = []
    report.append("# Missing Values Analysis Report")
    report.append("")
    report.append(f"**Generated:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"**Files analyzed:** {len(csv_files)}")
    report.append("")
    
    # Overall summary
    total_files = len(all_results)
    total_cells = sum(r['file_info']['total_cells'] for r in all_results)
    total_missing = sum(r['total_missing'] for r in all_results)
    overall_missing_percentage = (total_missing / total_cells) * 100 if total_cells > 0 else 0
    
    report.append("## Overall Summary")
    report.append("")
    report.append(f"- **Total files processed:** {total_files}")
    report.append(f"- **Total cells across all files:** {total_cells:,}")
    report.append(f"- **Total missing values:** {total_missing:,}")
    report.append(f"- **Overall missing percentage:** {overall_missing_percentage:.2f}%")
    report.append("")
    
    # Files ranked by missing values
    if all_results:
        report.append("## Files Ranked by Missing Value Count")
        report.append("")
        sorted_files = sorted(all_results, key=lambda x: x['total_missing'], reverse=True)
        for i, result in enumerate(sorted_files, 1):
            file_name = result['file_info']['file_name']
            missing_count = result['total_missing']
            missing_pct = result['missing_percentage']
            report.append(f"{i}. **{file_name}**: {missing_count:,} missing ({missing_pct:.2f}%)")
        report.append("")
    
    # Detailed analysis for each file
    report.append("## Detailed Analysis by File")
    report.append("")
    
    for result in all_results:
        file_info = result['file_info']
        report.append(f"### {file_info['file_name']}")
        report.append("")
        report.append(f"- **Dimensions:** {file_info['total_rows']} rows × {file_info['total_columns']} columns")
        report.append(f"- **Total cells:** {file_info['total_cells']:,}")
        report.append(f"- **Missing values:** {result['total_missing']:,} ({result['missing_percentage']:.2f}%)")
        report.append(f"- **Columns with missing values:** {result['columns_with_missing']}")
        report.append(f"- **Rows with missing values:** {result['rows_with_missing']}")
        report.append("")
        
        # Missing values by column
        if result['missing_by_column']:
            report.append("#### Top Columns with Missing Values")
            report.append("")
            sorted_columns = sorted(result['missing_by_column'].items(), key=lambda x: x[1], reverse=True)
            for col, count in sorted_columns[:10]:
                report.append(f"- **{col}**: {count:,} missing values")
            report.append("")
        
        # Missing values by row
        if result['missing_by_row']:
            report.append("#### Top Rows with Missing Values")
            report.append("")
            sorted_rows = sorted(result['missing_by_row'].items(), key=lambda x: x[1], reverse=True)
            for row, count in sorted_rows[:10]:
                report.append(f"- **Row {row}**: {count:,} missing values")
            report.append("")
        
        # Sample missing value locations
        if result['missing_locations']:
            report.append("#### Sample Missing Value Locations")
            report.append("")
            for loc in result['missing_locations'][:10]:
                report.append(f"- Row {loc['row']} ({loc['row_label']}), Column: {loc['column_label']}")
            report.append("")
        
        report.append("---")
        report.append("")
    
    return "\n".join(report)

if __name__ == "__main__":
    main() 