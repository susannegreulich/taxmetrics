"""
Main application for tax policy analysis.

This script demonstrates the capabilities of the tax analysis framework
for comparing tax policies and their revenue implications.
"""

import pandas as pd
import numpy as np
try:
    from models.tax_policy import ProgressiveTax, FlatTax, RegressiveTax
    from analysis.revenue_calculator import RevenueCalculator
    from analysis.distribution_analyzer import TaxBurdenAnalyzer
    from analysis.policy_comparator import PolicyComparator
    from visualization.charts import TaxPolicyCharts
except ImportError:
    from src.models.tax_policy import ProgressiveTax, FlatTax, RegressiveTax
    from src.analysis.revenue_calculator import RevenueCalculator
    from src.analysis.distribution_analyzer import TaxBurdenAnalyzer
    from src.analysis.policy_comparator import PolicyComparator
    from src.visualization.charts import TaxPolicyCharts


def main():
    """Main function demonstrating tax policy analysis."""
    print("Tax Policy Analysis Tool")
    print("=" * 50)
    
    # Initialize components
    revenue_calculator = RevenueCalculator()
    tax_burden_analyzer = TaxBurdenAnalyzer()
    policy_comparator = PolicyComparator()
    charts = TaxPolicyCharts()
    
    # Generate sample income distribution for tax base
    print("\n1. Generating sample income distribution for tax base...")
    income_distribution = revenue_calculator.generate_income_distribution(
        population_size=1000000,
        distribution_type="lognormal",
        mean=10.5,  # log of mean income
        std=0.6
    )
    
    print(f"   Generated distribution with {len(income_distribution)} income brackets")
    print(f"   Total population: {income_distribution['population'].sum():,}")
    print(f"   Total income: ${(income_distribution['income'] * income_distribution['population']).sum():,.0f}")
    
    # Define tax policies
    print("\n2. Creating tax policies...")
    
    # Progressive tax (similar to US federal income tax)
    progressive_tax = ProgressiveTax(
        brackets=[
            (0, 10000, 0.10),
            (10000, 40000, 0.15),
            (40000, 80000, 0.25),
            (80000, 160000, 0.30),
            (160000, float('inf'), 0.35)
        ],
        name="Progressive Tax (US-style)"
    )
    
    # Flat tax
    flat_tax = FlatTax(rate=0.25, name="Flat Tax (25%)")
    
    # Regressive tax (decreasing rates)
    regressive_tax = RegressiveTax(
        brackets=[
            (0, 50000, 0.30),
            (50000, 100000, 0.25),
            (100000, 200000, 0.20),
            (200000, float('inf'), 0.15)
        ],
        name="Regressive Tax"
    )
    
    policies = [progressive_tax, flat_tax, regressive_tax]
    
    print(f"   Created {len(policies)} tax policies")
    
    # Perform comprehensive analysis
    print("\n3. Performing comprehensive analysis...")
    comparison_results = policy_comparator.comprehensive_comparison(policies, income_distribution)
    
    # Display revenue comparison
    print("\n4. Revenue Comparison:")
    revenue_comparison = comparison_results['revenue_comparison']
    for _, row in revenue_comparison.iterrows():
        print(f"   {row['policy_name']}:")
        print(f"     Total Revenue: ${row['total_revenue']:,.0f}")
        print(f"     Revenue per Capita: ${row['revenue_per_capita']:,.0f}")
        print(f"     Average Effective Rate: {row['average_effective_rate']:.1%}")
        print()
    
    # Display tax burden analysis
    print("5. Tax Burden Analysis:")
    tax_burden_analysis = comparison_results['tax_burden_analysis']
    for _, row in tax_burden_analysis.iterrows():
        print(f"   {row['policy_name']} - {row['income_group']}:")
        print(f"     Average Effective Rate: {row['avg_effective_rate']:.1%}")
        print(f"     Tax per Capita: ${row['tax_per_capita']:,.0f}")
        print(f"     Share of Total Tax: {row['share_of_total_tax']:.1%}")
        print()
    
    # Display progressivity analysis
    print("6. Progressivity Analysis:")
    progressivity_analysis = comparison_results['progressivity_analysis']
    for _, row in progressivity_analysis.iterrows():
        print(f"   {row['policy_name']}:")
        print(f"     Kakwani Index: {row['kakwani_index']:.3f}")
        print(f"     Tax Progressivity: {row['tax_progressivity']}")
        print(f"     Average Effective Rate: {row['avg_effective_rate']:.1%}")
        print()
    
    # Calculate efficiency metrics
    print("7. Efficiency Metrics:")
    efficiency_metrics = policy_comparator.calculate_efficiency_metrics(policies, income_distribution)
    for _, row in efficiency_metrics.iterrows():
        print(f"   {row['policy_name']}:")
        print(f"     Revenue Efficiency: {row['revenue_efficiency']:,.0f}")
        print(f"     Progressivity Index: {row['progressivity_index']:.3f}")
        print()
    
    # Rank policies
    print("8. Policy Rankings:")
    ranking_criteria = {
        'revenue': 0.4,
        'progressivity': 0.3,
        'efficiency': 0.3
    }
    rankings = policy_comparator.rank_policies(policies, income_distribution, ranking_criteria)
    for _, row in rankings.iterrows():
        rank_value = row['rank']
        if pd.isna(rank_value):
            rank_value = "N/A"
        else:
            rank_value = int(rank_value)
        score_value = row['composite_score']
        if pd.isna(score_value):
            score_value = "N/A"
        else:
            score_value = f"{score_value:.3f}"
        print(f"   Rank {rank_value}: {row['policy_name']} (Score: {score_value})")
    
    # Create policy summary
    print("\n9. Policy Summary:")
    summary = policy_comparator.create_policy_summary(policies, income_distribution)
    print(summary.to_string(index=False))
    
    # Generate visualizations
    print("\n10. Generating visualizations...")
    
    # Tax burden comparison
    tax_burden_fig = charts.plot_tax_burden_comparison(policies)
    tax_burden_fig.write_html("data/tax_burden_comparison.html")
    
    # Revenue comparison
    revenue_fig = charts.plot_revenue_comparison(revenue_comparison)
    revenue_fig.write_html("data/revenue_comparison.html")
    
    # Tax burden by income groups
    tax_burden_groups_fig = charts.plot_tax_burden_by_income_groups(comparison_results['tax_burden_analysis'])
    tax_burden_groups_fig.write_html("data/tax_burden_by_income_groups.html")
    
    # Progressivity comparison
    progressivity_fig = charts.plot_progressivity_comparison(comparison_results['progressivity_analysis'])
    progressivity_fig.write_html("data/progressivity_comparison.html")
    
    # Comprehensive dashboard
    dashboard_fig = charts.create_comprehensive_dashboard(comparison_results)
    dashboard_fig.write_html("data/comprehensive_dashboard.html")
    
    print("   Visualizations saved to data/ directory")
    
    # Perform sensitivity analysis
    print("\n11. Sensitivity Analysis:")
    sensitivity_params = {
        'rate': np.linspace(0.15, 0.35, 10)
    }
    sensitivity_results = policy_comparator.sensitivity_analysis(
        flat_tax, income_distribution, sensitivity_params
    )
    
    for param_name, param_data in sensitivity_results.items():
        print(f"   {param_name} sensitivity:")
        print(f"     Revenue range: ${param_data['total_revenue'].min():,.0f} - ${param_data['total_revenue'].max():,.0f}")
        print(f"     Progressivity range: {param_data['progressivity_index'].min():.3f} - {param_data['progressivity_index'].max():.3f}")
    
    # Save sensitivity plot
    sensitivity_fig = charts.plot_sensitivity_analysis(sensitivity_results)
    sensitivity_fig.write_html("data/sensitivity_analysis.html")
    
    print("\nAnalysis complete! Check the data/ directory for interactive visualizations.")
    print("\nKey Findings:")
    print("- Progressive tax provides high progressivity with moderate revenue")
    print("- Flat tax generates moderate revenue with moderate progressivity")
    print("- Regressive tax generates high revenue but with low progressivity")
    
    return comparison_results


if __name__ == "__main__":
    # Create data directory if it doesn't exist
    import os
    os.makedirs("data", exist_ok=True)
    
    # Run the analysis
    results = main() 