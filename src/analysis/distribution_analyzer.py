"""
Tax burden analysis of tax policies.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
try:
    from ..models.tax_policy import TaxPolicy
except ImportError:
    from models.tax_policy import TaxPolicy


class TaxBurdenAnalyzer:
    """Analyze the tax burden effects of tax policies."""
    
    def __init__(self):
        """Initialize the tax burden analyzer."""
        pass
    
    def analyze_tax_burden_by_income_groups(self, income_distribution: pd.DataFrame, 
                                           tax_policy: TaxPolicy) -> pd.DataFrame:
        """
        Analyze tax burden and effective rates by income groups.
        
        Args:
            income_distribution: DataFrame with income and population data
            tax_policy: Tax policy to analyze
            
        Returns:
            DataFrame with tax burden analysis
        """
        # Create a copy to avoid modifying the original
        df = income_distribution.copy()
        
        # Calculate tax for each income level
        df['tax'] = df['income'].apply(tax_policy.calculate_tax)
        df['effective_rate'] = df['income'].apply(tax_policy.calculate_effective_rate)
        
        # Sort by income and calculate income groups
        sorted_data = df.sort_values('income').copy()
        sorted_data['cumulative_population'] = sorted_data['population'].cumsum()
        total_population = sorted_data['population'].sum()
        
        # Define income groups for tax burden analysis
        income_groups = [
            (0, 25000, "Low Income"),
            (25000, 50000, "Lower Middle"),
            (50000, 100000, "Middle Income"),
            (100000, 250000, "Upper Middle"),
            (250000, float('inf'), "High Income")
        ]
        
        group_results = []
        
        for min_income, max_income, group_name in income_groups:
            mask = (df['income'] >= min_income) & (df['income'] < max_income)
            group_data = df[mask]
            
            if not group_data.empty:
                group_income = (group_data['income'] * group_data['population']).sum()
                group_tax = (group_data['tax'] * group_data['population']).sum()
                group_population = group_data['population'].sum()
                avg_effective_rate = group_tax / group_income if group_income > 0 else 0
                
                group_results.append({
                    'income_group': group_name,
                    'income_range': f"${min_income:,.0f} - ${max_income:,.0f}" if max_income != float('inf') else f"${min_income:,.0f}+",
                    'total_income': group_income,
                    'total_tax': group_tax,
                    'population': group_population,
                    'avg_effective_rate': avg_effective_rate,
                    'tax_per_capita': group_tax / group_population if group_population > 0 else 0,
                    'income_per_capita': group_income / group_population if group_population > 0 else 0,
                    'share_of_total_income': group_income / df['income'].sum() if df['income'].sum() > 0 else 0,
                    'share_of_total_tax': group_tax / df['tax'].sum() if df['tax'].sum() > 0 else 0
                })
        
        return pd.DataFrame(group_results)
    
    def analyze_tax_incidence(self, income_distribution: pd.DataFrame, 
                            tax_policy: TaxPolicy) -> pd.DataFrame:
        """
        Analyze tax incidence across different income groups.
        
        Args:
            income_distribution: Income distribution data
            tax_policy: Tax policy to analyze
            
        Returns:
            DataFrame with tax incidence analysis
        """
        # Create a copy to avoid modifying the original
        df = income_distribution.copy()
        
        # Calculate tax for each income level
        df['tax'] = df['income'].apply(tax_policy.calculate_tax)
        df['effective_rate'] = df['income'].apply(tax_policy.calculate_effective_rate)
        
        # Define income groups
        income_groups = [
            (0, 25000, "Low Income"),
            (25000, 50000, "Lower Middle"),
            (50000, 100000, "Middle Income"),
            (100000, 250000, "Upper Middle"),
            (250000, float('inf'), "High Income")
        ]
        
        group_results = []
        
        for min_income, max_income, group_name in income_groups:
            mask = (df['income'] >= min_income) & (df['income'] < max_income)
            group_data = df[mask]
            
            if not group_data.empty:
                group_income = (group_data['income'] * group_data['population']).sum()
                group_tax = (group_data['tax'] * group_data['population']).sum()
                group_population = group_data['population'].sum()
                avg_effective_rate = group_tax / group_income if group_income > 0 else 0
                
                group_results.append({
                    'income_group': group_name,
                    'income_range': f"${min_income:,.0f} - ${max_income:,.0f}" if max_income != float('inf') else f"${min_income:,.0f}+",
                    'total_income': group_income,
                    'total_tax': group_tax,
                    'population': group_population,
                    'avg_effective_rate': avg_effective_rate,
                    'tax_per_capita': group_tax / group_population if group_population > 0 else 0,
                    'income_per_capita': group_income / group_population if group_population > 0 else 0,
                    'share_of_total_income': group_income / df['income'].sum() if df['income'].sum() > 0 else 0,
                    'share_of_total_tax': group_tax / df['tax'].sum() if df['tax'].sum() > 0 else 0
                })
        
        return pd.DataFrame(group_results)
    
    def calculate_tax_progressivity(self, income_distribution: pd.DataFrame, 
                                  tax_policy: TaxPolicy) -> Dict[str, float]:
        """
        Calculate tax progressivity metrics.
        
        Args:
            income_distribution: Income distribution data
            tax_policy: Tax policy to analyze
            
        Returns:
            Dictionary with progressivity metrics
        """
        # Create a copy to avoid modifying the original
        df = income_distribution.copy()
        
        # Calculate tax for each income level
        df['tax'] = df['income'].apply(tax_policy.calculate_tax)
        df['effective_rate'] = df['income'].apply(tax_policy.calculate_effective_rate)
        
        # Calculate weighted averages
        total_population = df['population'].sum()
        total_income = (df['income'] * df['population']).sum()
        total_tax = (df['tax'] * df['population']).sum()
        
        # Calculate average effective tax rate
        avg_effective_rate = total_tax / total_income if total_income > 0 else 0
        
        # Calculate progressivity index (Kakwani index)
        # This measures how progressive the tax system is
        if total_income > 0 and total_tax > 0:
            # Calculate concentration coefficient for taxes
            sorted_data = df.sort_values('income').copy()
            sorted_data['cumulative_population'] = sorted_data['population'].cumsum()
            sorted_data['cumulative_income'] = (sorted_data['income'] * sorted_data['population']).cumsum()
            sorted_data['cumulative_tax'] = (sorted_data['tax'] * sorted_data['population']).cumsum()
            
            # Calculate concentration coefficient
            concentration_coeff = 0
            for i in range(len(sorted_data)):
                if i == 0:
                    concentration_coeff += sorted_data.iloc[i]['tax'] * sorted_data.iloc[i]['population'] * 0.5
                else:
                    concentration_coeff += sorted_data.iloc[i]['tax'] * sorted_data.iloc[i]['population'] * (
                        sorted_data.iloc[i-1]['cumulative_population'] + 0.5 * sorted_data.iloc[i]['population']
                    )
            
            concentration_coeff = 2 * concentration_coeff / (total_tax * total_population) - 1
            
            # Calculate Gini coefficient for income
            income_gini = 0
            for i in range(len(sorted_data)):
                if i == 0:
                    income_gini += sorted_data.iloc[i]['income'] * sorted_data.iloc[i]['population'] * 0.5
                else:
                    income_gini += sorted_data.iloc[i]['income'] * sorted_data.iloc[i]['population'] * (
                        sorted_data.iloc[i-1]['cumulative_population'] + 0.5 * sorted_data.iloc[i]['population']
                    )
            
            income_gini = 2 * income_gini / (total_income * total_population) - 1
            
            # Kakwani index = concentration coefficient - Gini coefficient
            kakwani_index = concentration_coeff - income_gini
        else:
            kakwani_index = 0
        
        return {
            'avg_effective_rate': avg_effective_rate,
            'total_tax_revenue': total_tax,
            'total_income': total_income,
            'kakwani_index': kakwani_index,
            'tax_progressivity': 'Progressive' if kakwani_index > 0 else 'Regressive' if kakwani_index < 0 else 'Proportional'
        } 