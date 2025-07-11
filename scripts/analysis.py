#!/usr/bin/env python3
"""
Basic example of tax policy analysis.

This script demonstrates the core functionality of the tax analysis framework.
"""

import sys
import os
from datetime import datetime

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

import pandas as pd
import numpy as np

# Now import from the src modules
from models.tax_policy import ProgressiveTax, FlatTax, RegressiveTax
from analysis.revenue_calculator import RevenueCalculator
from analysis.policy_comparator import PolicyComparator
from visualization.charts import TaxPolicyCharts


class ReportGenerator:
    """Generate markdown reports for tax analysis results."""
    
    def __init__(self, output_dir="results"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.report_content = []
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def add_header(self, title, level=1):
        """Add a header to the report."""
        self.report_content.append(f"{'#' * level} {title}\n")
    
    def add_text(self, text):
        """Add plain text to the report."""
        self.report_content.append(f"{text}\n")
    
    def add_subsection(self, title, level=2):
        """Add a subsection header."""
        self.report_content.append(f"{'#' * level} {title}\n")
    
    def add_table(self, data, headers=None):
        """Add a table to the report."""
        if isinstance(data, pd.DataFrame):
            # Convert DataFrame to markdown table
            if headers is None:
                headers = data.columns.tolist()
            
            # Add header row
            self.report_content.append("| " + " | ".join(str(h) for h in headers) + " |")
            self.report_content.append("| " + " | ".join(["---"] * len(headers)) + " |")
            
            # Add data rows
            for _, row in data.iterrows():
                self.report_content.append("| " + " | ".join(str(val) for val in row) + " |")
            self.report_content.append("")
        else:
            # Handle list of lists
            if headers:
                self.report_content.append("| " + " | ".join(str(h) for h in headers) + " |")
                self.report_content.append("| " + " | ".join(["---"] * len(headers)) + " |")
            
            for row in data:
                self.report_content.append("| " + " | ".join(str(val) for val in row) + " |")
            self.report_content.append("")
    
    def add_list(self, items, ordered=False):
        """Add a list to the report."""
        for i, item in enumerate(items, 1):
            if ordered:
                self.report_content.append(f"{i}. {item}")
            else:
                self.report_content.append(f"- {item}")
        self.report_content.append("")
    
    def add_code_block(self, code, language=""):
        """Add a code block to the report."""
        self.report_content.append(f"```{language}")
        self.report_content.append(code)
        self.report_content.append("```\n")
    
    def save_report(self, filename="tax_analysis_report.md"):
        """Save the report to a markdown file."""
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.report_content))
        print(f"Report saved to: {filepath}")
        return filepath


def analyze_oecd_data(analysis_data, report_gen):
    """Perform basic analysis on OECD tax data and add to report."""
    print("\nOECD Tax Data Analysis")
    print("=" * 40)
    
    report_gen.add_header("OECD Tax Data Analysis")
    
    if analysis_data.empty:
        print("   No analysis data available")
        report_gen.add_text("No analysis data available.")
        return
    
    # Summary statistics
    print("   Summary statistics:")
    report_gen.add_subsection("Summary Statistics")
    
    summary_stats = {
        "Countries": analysis_data['country'].nunique(),
        "Years": analysis_data['year'].nunique(),
        "Total Records": len(analysis_data)
    }
    
    for key, value in summary_stats.items():
        print(f"     {key}: {value}")
        report_gen.add_text(f"**{key}:** {value}")
    
    # Tax revenue analysis
    if 'total_tax_revenue' in analysis_data.columns:
        print("\n   Tax Revenue Analysis:")
        report_gen.add_subsection("Tax Revenue Analysis")
        
        revenue_stats = analysis_data['total_tax_revenue'].describe()
        revenue_summary = {
            "Mean": f"{revenue_stats['mean']:.1f}% of GDP",
            "Median": f"{revenue_stats['50%']:.1f}% of GDP",
            "Range": f"{revenue_stats['min']:.1f}% - {revenue_stats['max']:.1f}% of GDP"
        }
        
        for key, value in revenue_summary.items():
            print(f"     {key}: {value}")
            report_gen.add_text(f"**{key}:** {value}")
    
    # Tax rates analysis
    if 'top_personal_rate' in analysis_data.columns:
        print("\n   Personal Tax Rates:")
        report_gen.add_subsection("Personal Tax Rates")
        
        rate_stats = analysis_data['top_personal_rate'].describe()
        rate_summary = {
            "Mean Top Rate": f"{rate_stats['mean']:.1f}%",
            "Median Top Rate": f"{rate_stats['50%']:.1f}%",
            "Range": f"{rate_stats['min']:.1f}% - {rate_stats['max']:.1f}%"
        }
        
        for key, value in rate_summary.items():
            print(f"     {key}: {value}")
            report_gen.add_text(f"**{key}:** {value}")
    
    # Corporate tax rates analysis
    if 'corporate_rate' in analysis_data.columns:
        print("\n   Corporate Tax Rates:")
        report_gen.add_subsection("Corporate Tax Rates")
        
        corp_stats = analysis_data['corporate_rate'].describe()
        corp_summary = {
            "Mean Corporate Rate": f"{corp_stats['mean']:.1f}%",
            "Median Corporate Rate": f"{corp_stats['50%']:.1f}%",
            "Range": f"{corp_stats['min']:.1f}% - {corp_stats['max']:.1f}%"
        }
        
        for key, value in corp_summary.items():
            print(f"     {key}: {value}")
            report_gen.add_text(f"**{key}:** {value}")
    
    # Country comparison
    print("\n   Country Comparison (Latest Year):")
    report_gen.add_subsection("Country Comparison (Latest Year)")
    
    latest_year = analysis_data['year'].max()
    latest_data = analysis_data[analysis_data['year'] == latest_year]
    
    if not latest_data.empty:
        # Create a table for country comparison
        comparison_data = []
        for _, row in latest_data.iterrows():
            country = row['country']
            revenue = row.get('total_tax_revenue', 'N/A')
            top_rate = row.get('top_personal_rate', 'N/A')
            corp_rate = row.get('corporate_rate', 'N/A')
            
            print(f"     {country}:")
            if revenue != 'N/A':
                print(f"       Tax Revenue: {revenue:.1f}% of GDP")
            if top_rate != 'N/A':
                print(f"       Top Personal Rate: {top_rate:.1f}%")
            if corp_rate != 'N/A':
                print(f"       Corporate Rate: {corp_rate:.1f}%")
            
            comparison_data.append([
                country,
                f"{revenue:.1f}%" if revenue != 'N/A' else 'N/A',
                f"{top_rate:.1f}%" if top_rate != 'N/A' else 'N/A',
                f"{corp_rate:.1f}%" if corp_rate != 'N/A' else 'N/A'
            ])
        
        headers = ["Country", "Tax Revenue (% GDP)", "Top Personal Rate (%)", "Corporate Rate (%)"]
        report_gen.add_table(comparison_data, headers)


def basic_analysis(report_gen):
    """Perform a basic tax policy analysis and add to report."""
    print("Basic Tax Policy Analysis")
    print("=" * 40)
    
    report_gen.add_header("Basic Tax Policy Analysis")
    
    # Initialize components
    revenue_calculator = RevenueCalculator()
    policy_comparator = PolicyComparator()
    charts = TaxPolicyCharts()
    
    # Generate income distribution for tax base
    print("1. Generating income distribution for tax base...")
    report_gen.add_subsection("1. Income Distribution Generation")
    
    income_distribution = revenue_calculator.generate_income_distribution(
        population_size=100000,
        distribution_type="lognormal",
        mean=10.5,
        std=0.6
    )
    
    population = income_distribution['population'].sum()
    total_income = (income_distribution['income'] * income_distribution['population']).sum()
    
    print(f"   Population: {population:,}")
    print(f"   Total income: ${total_income:,.0f}")
    
    report_gen.add_text(f"**Population:** {population:,}")
    report_gen.add_text(f"**Total Income:** ${total_income:,.0f}")
    
    # Create tax policies
    print("\n2. Creating tax policies...")
    report_gen.add_subsection("2. Tax Policy Definitions")
    
    progressive = ProgressiveTax(
        brackets=[
            (0, 20000, 0.10),
            (20000, 60000, 0.20),
            (60000, float('inf'), 0.30)
        ],
        name="Progressive Tax"
    )
    
    flat = FlatTax(rate=0.20, name="Flat Tax (20%)")
    
    regressive = RegressiveTax(
        brackets=[
            (0, 40000, 0.25),
            (40000, 80000, 0.20),
            (80000, float('inf'), 0.15)
        ],
        name="Regressive Tax"
    )
    
    policies = [progressive, flat, regressive]
    
    # Add policy definitions to report
    policy_definitions = []
    for policy in policies:
        if hasattr(policy, 'brackets'):
            brackets_str = ", ".join([f"${b[0]:,.0f}-${b[1]:,.0f}: {b[2]:.1%}" for b in policy.brackets])
            policy_definitions.append([policy.name, brackets_str])
        else:
            policy_definitions.append([policy.name, f"{policy.rate:.1%}"])
    
    report_gen.add_table(policy_definitions, ["Policy", "Rate Structure"])
    
    # Calculate revenues
    print("\n3. Calculating revenues...")
    report_gen.add_subsection("3. Revenue Calculations")
    
    revenue_results = []
    for policy in policies:
        revenue_data = revenue_calculator.calculate_revenue(policy, income_distribution.copy())
        print(f"   {policy.name}:")
        print(f"     Total Revenue: ${revenue_data['total_revenue']:,.0f}")
        print(f"     Revenue per Capita: ${revenue_data['revenue_per_capita']:,.0f}")
        print(f"     Average Tax Rate: {revenue_data['average_effective_rate']:.1%}")
        print()
        
        revenue_results.append([
            policy.name,
            f"${revenue_data['total_revenue']:,.0f}",
            f"${revenue_data['revenue_per_capita']:,.0f}",
            f"{revenue_data['average_effective_rate']:.1%}"
        ])
    
    report_gen.add_table(revenue_results, ["Policy", "Total Revenue", "Revenue per Capita", "Average Tax Rate"])
    
    # Compare policies
    print("4. Policy comparison...")
    report_gen.add_subsection("4. Policy Comparison")
    
    comparison = policy_comparator.comprehensive_comparison(policies, income_distribution)
    
    # Display tax burden analysis
    tax_burden_data = comparison['tax_burden_analysis']
    print("Tax Burden Analysis:")
    report_gen.add_subsection("Tax Burden Analysis")
    
    burden_results = []
    for _, row in tax_burden_data.iterrows():
        print(f"   {row['policy_name']}:")
        print(f"     Average Effective Rate: {row['avg_effective_rate']:.1%}")
        print(f"     Total Tax Revenue: ${row['total_tax']:,.0f}")
        print(f"     Tax per Capita: ${row['tax_per_capita']:,.0f}")
        print()
        
        burden_results.append([
            row['policy_name'],
            f"{row['avg_effective_rate']:.1%}",
            f"${row['total_tax']:,.0f}",
            f"${row['tax_per_capita']:,.0f}"
        ])
    
    report_gen.add_table(burden_results, ["Policy", "Average Effective Rate", "Total Tax Revenue", "Tax per Capita"])
    
    # Create simple visualization
    print("5. Creating visualization...")
    report_gen.add_subsection("5. Visualizations")
    
    tax_burden_fig = charts.plot_tax_burden_comparison(policies)
    
    # Save to file
    chart_filename = "basic_tax_burden_comparison.html"
    chart_path = os.path.join("results", chart_filename)
    tax_burden_fig.write_html(chart_path)
    print("   Chart saved to results/basic_tax_burden_comparison.html")
    
    report_gen.add_text(f"Interactive tax burden comparison chart: [{chart_filename}]({chart_filename})")
    
    print("\nAnalysis complete!")
    report_gen.add_subsection("Key Findings")
    
    findings = [
        "Progressive tax provides moderate revenue with high progressivity",
        "Flat tax provides moderate revenue with moderate progressivity", 
        "Regressive tax may generate more revenue but with low progressivity"
    ]
    
    print("\nKey findings:")
    for finding in findings:
        print(f"- {finding}")
    
    report_gen.add_list(findings)


def main():
    """Main function to run different types of analysis."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Run tax policy analysis')
    parser.add_argument('--type', choices=['basic', 'oecd', 'both'], default='basic',
                       help='Type of analysis to run (default: basic)')
    parser.add_argument('--data-file', type=str, 
                       help='Path to analysis-ready data file (required for OECD analysis)')
    parser.add_argument('--output', type=str, default='tax_analysis_report.md',
                       help='Output filename for the markdown report (default: tax_analysis_report.md)')
    
    args = parser.parse_args()
    
    # Initialize report generator
    report_gen = ReportGenerator()
    report_gen.add_header("Tax Policy Analysis Report")
    report_gen.add_text(f"**Generated:** {report_gen.timestamp}")
    report_gen.add_text("This report contains comprehensive analysis of tax policies and their economic impacts.")
    
    if args.type in ['basic', 'both']:
        basic_analysis(report_gen)
    
    if args.type in ['oecd', 'both']:
        if not args.data_file:
            print("Error: --data-file is required for OECD analysis")
            return
        
        if not os.path.exists(args.data_file):
            print(f"Error: Data file {args.data_file} not found")
            return
        
        try:
            analysis_data = pd.read_csv(args.data_file)
            analyze_oecd_data(analysis_data, report_gen)
        except Exception as e:
            print(f"Error loading or analyzing data: {e}")
            report_gen.add_text(f"**Error during OECD analysis:** {e}")
    
    # Save the complete report
    report_gen.save_report(args.output)


if __name__ == "__main__":
    main() 