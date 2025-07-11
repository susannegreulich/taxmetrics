"""
Revenue calculation and analysis for tax policies.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Union
try:
    from ..models.tax_policy import TaxPolicy
except ImportError:
    from models.tax_policy import TaxPolicy


class RevenueCalculator:
    """Calculate tax revenues for different tax policies and income distributions."""
    
    def __init__(self):
        """Initialize the revenue calculator."""
        pass
    
    def calculate_revenue(self, tax_policy: TaxPolicy, income_distribution: pd.DataFrame) -> Dict[str, float]:
        """
        Calculate total revenue for a tax policy given an income distribution.
        
        Args:
            tax_policy: Tax policy to evaluate
            income_distribution: DataFrame with 'income' and 'population' columns
            
        Returns:
            Dictionary with revenue statistics
        """
        if 'income' not in income_distribution.columns or 'population' not in income_distribution.columns:
            raise ValueError("Income distribution must have 'income' and 'population' columns")
        
        # Calculate tax for each income level
        income_distribution['tax'] = income_distribution['income'].apply(tax_policy.calculate_tax)
        income_distribution['effective_rate'] = income_distribution['income'].apply(tax_policy.calculate_effective_rate)
        income_distribution['marginal_rate'] = income_distribution['income'].apply(tax_policy.get_marginal_rate)
        
        # Calculate weighted totals
        total_population = income_distribution['population'].sum()
        total_income = (income_distribution['income'] * income_distribution['population']).sum()
        total_revenue = (income_distribution['tax'] * income_distribution['population']).sum()
        
        # Calculate revenue by income quintiles
        quintile_revenue = self._calculate_quintile_revenue(income_distribution)
        
        return {
            'total_revenue': total_revenue,
            'total_population': total_population,
            'total_income': total_income,
            'average_effective_rate': total_revenue / total_income if total_income > 0 else 0,
            'revenue_per_capita': total_revenue / total_population if total_population > 0 else 0,
            'quintile_revenue': quintile_revenue,
            'detailed_data': income_distribution
        }
    
    def _calculate_quintile_revenue(self, income_distribution: pd.DataFrame) -> Dict[str, float]:
        """Calculate revenue by income quintiles."""
        # Sort by income and calculate cumulative population
        sorted_data = income_distribution.sort_values('income').copy()
        sorted_data['cumulative_population'] = sorted_data['population'].cumsum()
        total_population = sorted_data['population'].sum()
        
        quintile_revenue = {}
        quintile_size = total_population / 5
        
        for i in range(5):
            start_pop = i * quintile_size
            end_pop = (i + 1) * quintile_size
            
            # Find rows in this quintile
            mask = (sorted_data['cumulative_population'] > start_pop) & \
                   (sorted_data['cumulative_population'] <= end_pop)
            
            quintile_data = sorted_data[mask]
            if not quintile_data.empty:
                quintile_revenue[f'quintile_{i+1}'] = (quintile_data['tax'] * quintile_data['population']).sum()
            else:
                quintile_revenue[f'quintile_{i+1}'] = 0.0
        
        return quintile_revenue
    
    def compare_policies(self, policies: List[TaxPolicy], income_distribution: pd.DataFrame) -> pd.DataFrame:
        """
        Compare multiple tax policies side by side.
        
        Args:
            policies: List of tax policies to compare
            income_distribution: Income distribution data
            
        Returns:
            DataFrame with comparison results
        """
        results = []
        
        for policy in policies:
            revenue_data = self.calculate_revenue(policy, income_distribution.copy())
            
            results.append({
                'policy_name': policy.name,
                'total_revenue': revenue_data['total_revenue'],
                'average_effective_rate': revenue_data['average_effective_rate'],
                'revenue_per_capita': revenue_data['revenue_per_capita'],
                'total_population': revenue_data['total_population'],
                'total_income': revenue_data['total_income']
            })
        
        return pd.DataFrame(results)
    
    def sensitivity_analysis(self, tax_policy: TaxPolicy, income_distribution: pd.DataFrame, 
                           parameter_range: List[float], parameter_name: str = "rate") -> pd.DataFrame:
        """
        Perform sensitivity analysis by varying a parameter.
        
        Args:
            tax_policy: Base tax policy
            income_distribution: Income distribution data
            parameter_range: List of parameter values to test
            parameter_name: Name of the parameter being varied
            
        Returns:
            DataFrame with sensitivity analysis results
        """
        results = []
        
        for param_value in parameter_range:
            # Create a copy of the policy with modified parameter
            if hasattr(tax_policy, 'rate'):  # Flat tax
                modified_policy = type(tax_policy)(rate=param_value, name=f"{tax_policy.name} ({param_name}={param_value})")
            elif hasattr(tax_policy, 'brackets'):  # Progressive/Regressive tax
                # For bracket-based taxes, we'd need to modify the brackets
                # This is a simplified version - in practice you'd want more sophisticated parameter modification
                modified_policy = tax_policy
            else:
                modified_policy = tax_policy
            
            revenue_data = self.calculate_revenue(modified_policy, income_distribution.copy())
            
            results.append({
                parameter_name: param_value,
                'total_revenue': revenue_data['total_revenue'],
                'average_effective_rate': revenue_data['average_effective_rate'],
                'revenue_per_capita': revenue_data['revenue_per_capita']
            })
        
        return pd.DataFrame(results)
    
    def generate_income_distribution(self, population_size: int = 1000000, 
                                   distribution_type: str = "lognormal",
                                   **kwargs) -> pd.DataFrame:
        """
        Generate synthetic income distribution for analysis.
        
        Args:
            population_size: Number of individuals in the population
            distribution_type: Type of distribution ('lognormal', 'normal', 'exponential')
            **kwargs: Parameters for the distribution
            
        Returns:
            DataFrame with income distribution
        """
        if distribution_type == "lognormal":
            mean = kwargs.get('mean', 10.0)  # log of mean income
            std = kwargs.get('std', 0.5)
            incomes = np.random.lognormal(mean, std, population_size)
        elif distribution_type == "normal":
            mean = kwargs.get('mean', 50000)
            std = kwargs.get('std', 20000)
            incomes = np.random.normal(mean, std, population_size)
            incomes = np.maximum(incomes, 0)  # Ensure non-negative
        elif distribution_type == "exponential":
            scale = kwargs.get('scale', 50000)
            incomes = np.random.exponential(scale, population_size)
        else:
            raise ValueError(f"Unknown distribution type: {distribution_type}")
        
        # Create income brackets for aggregation
        income_bins = np.linspace(0, np.percentile(incomes, 99.9), 100)
        hist, bin_edges = np.histogram(incomes, bins=income_bins)
        
        # Create DataFrame
        income_levels = (bin_edges[:-1] + bin_edges[1:]) / 2
        population_counts = hist
        
        return pd.DataFrame({
            'income': income_levels,
            'population': population_counts
        }) 