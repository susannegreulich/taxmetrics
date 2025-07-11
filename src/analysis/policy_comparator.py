"""
Policy comparison and evaluation tools.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
try:
    from ..models.tax_policy import TaxPolicy
    from .revenue_calculator import RevenueCalculator
    from .distribution_analyzer import TaxBurdenAnalyzer
except ImportError:
    from models.tax_policy import TaxPolicy
    from analysis.revenue_calculator import RevenueCalculator
    from analysis.distribution_analyzer import TaxBurdenAnalyzer


class PolicyComparator:
    """Compare multiple tax policies across various metrics."""
    
    def __init__(self):
        """Initialize the policy comparator."""
        self.revenue_calculator = RevenueCalculator()
        self.tax_burden_analyzer = TaxBurdenAnalyzer()
    
    def comprehensive_comparison(self, policies: List[TaxPolicy], 
                               income_distribution: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Perform comprehensive comparison of multiple tax policies.
        
        Args:
            policies: List of tax policies to compare
            income_distribution: Income distribution data
            
        Returns:
            Dictionary with comparison results
        """
        results = {}
        
        # Revenue comparison
        revenue_comparison = self.revenue_calculator.compare_policies(policies, income_distribution)
        results['revenue_comparison'] = revenue_comparison
        
        # Tax burden analysis for each policy
        tax_burden_analyses = []
        incidence_analyses = []
        progressivity_analyses = []
        
        for policy in policies:
            # Tax burden analysis
            tax_burden_data = self.tax_burden_analyzer.analyze_tax_burden_by_income_groups(
                income_distribution.copy(), policy
            )
            tax_burden_data['policy_name'] = policy.name
            tax_burden_analyses.append(tax_burden_data)
            
            # Tax incidence analysis
            incidence_data = self.tax_burden_analyzer.analyze_tax_incidence(
                income_distribution.copy(), policy
            )
            incidence_data['policy_name'] = policy.name
            incidence_analyses.append(incidence_data)
            
            # Progressivity analysis
            progressivity_data = self.tax_burden_analyzer.calculate_tax_progressivity(
                income_distribution.copy(), policy
            )
            progressivity_data['policy_name'] = policy.name
            progressivity_analyses.append(progressivity_data)
        
        results['tax_burden_analysis'] = pd.concat(tax_burden_analyses, ignore_index=True)
        results['incidence_analysis'] = pd.concat(incidence_analyses, ignore_index=True)
        results['progressivity_analysis'] = pd.DataFrame(progressivity_analyses)
        
        return results
    
    def calculate_efficiency_metrics(self, policies: List[TaxPolicy], 
                                   income_distribution: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate efficiency metrics for tax policies.
        
        Args:
            policies: List of tax policies to compare
            income_distribution: Income distribution data
            
        Returns:
            DataFrame with efficiency metrics
        """
        efficiency_results = []
        
        for policy in policies:
            # Calculate revenue and tax burden effects
            revenue_data = self.revenue_calculator.calculate_revenue(policy, income_distribution.copy())
            progressivity_data = self.tax_burden_analyzer.calculate_tax_progressivity(
                income_distribution.copy(), policy
            )
            
            # Calculate efficiency metrics
            total_revenue = revenue_data['total_revenue']
            total_income = revenue_data['total_income']
            avg_effective_rate = progressivity_data['avg_effective_rate']
            kakwani_index = progressivity_data['kakwani_index']
            
            # Revenue efficiency (revenue per unit of tax rate)
            revenue_efficiency = total_revenue / (avg_effective_rate * total_income) if avg_effective_rate > 0 else float('inf')
            
            # Progressivity index
            progressivity = kakwani_index
            
            # Average tax rate
            avg_tax_rate = total_revenue / total_income if total_income > 0 else 0
            
            efficiency_results.append({
                'policy_name': policy.name,
                'total_revenue': total_revenue,
                'avg_tax_rate': avg_tax_rate,
                'avg_effective_rate': avg_effective_rate,
                'progressivity_index': progressivity,
                'revenue_efficiency': revenue_efficiency,
                'revenue_per_capita': revenue_data['revenue_per_capita'],
                'tax_progressivity': progressivity_data['tax_progressivity']
            })
        
        return pd.DataFrame(efficiency_results)
    
    def rank_policies(self, policies: List[TaxPolicy], 
                     income_distribution: pd.DataFrame,
                     criteria: Dict[str, float]) -> pd.DataFrame:
        """
        Rank policies based on multiple criteria with weights.
        
        Args:
            policies: List of tax policies to rank
            income_distribution: Income distribution data
            criteria: Dictionary of criteria and their weights
                     (e.g., {'revenue': 0.4, 'progressivity': 0.3, 'efficiency': 0.3})
            
        Returns:
            DataFrame with policy rankings
        """
        # Calculate all metrics
        efficiency_metrics = self.calculate_efficiency_metrics(policies, income_distribution)
        
        # Normalize metrics for ranking (0-1 scale)
        normalized_metrics = efficiency_metrics.copy()
        
        for col in ['total_revenue', 'avg_tax_rate', 'avg_effective_rate', 'progressivity_index', 'revenue_efficiency', 'revenue_per_capita']:
            if col in normalized_metrics.columns:
                min_val = normalized_metrics[col].min()
                max_val = normalized_metrics[col].max()
                if max_val > min_val:
                    normalized_metrics[f'{col}_normalized'] = (normalized_metrics[col] - min_val) / (max_val - min_val)
                else:
                    normalized_metrics[f'{col}_normalized'] = 0.5
        
        # Calculate composite scores
        composite_scores = []
        
        for _, row in normalized_metrics.iterrows():
            score = 0
            for criterion, weight in criteria.items():
                if criterion == 'revenue':
                    score += weight * row.get('total_revenue_normalized', 0)
                elif criterion == 'progressivity':
                    score += weight * row.get('progressivity_index_normalized', 0)
                elif criterion == 'efficiency':
                    score += weight * row.get('revenue_efficiency_normalized', 0)
                # Add more criteria as needed
            
            composite_scores.append(score)
        
        # Add rankings
        normalized_metrics['composite_score'] = composite_scores
        normalized_metrics['rank'] = normalized_metrics['composite_score'].rank(ascending=False)
        
        return normalized_metrics.sort_values('rank')
    
    def sensitivity_analysis(self, base_policy: TaxPolicy, 
                           income_distribution: pd.DataFrame,
                           parameter_ranges: Dict[str, List[float]]) -> Dict[str, pd.DataFrame]:
        """
        Perform sensitivity analysis on policy parameters.
        
        Args:
            base_policy: Base tax policy to analyze
            income_distribution: Income distribution data
            parameter_ranges: Dictionary of parameter names and value ranges to test
            
        Returns:
            Dictionary with sensitivity analysis results
        """
        sensitivity_results = {}
        
        for param_name, param_values in parameter_ranges.items():
            results = []
            
            for param_value in param_values:
                # Create modified policy with new parameter value
                modified_policy = self._modify_policy(base_policy, param_name, param_value)
                
                # Calculate metrics for modified policy
                revenue_data = self.revenue_calculator.calculate_revenue(modified_policy, income_distribution.copy())
                progressivity_data = self.tax_burden_analyzer.calculate_tax_progressivity(
                    income_distribution.copy(), modified_policy
                )
                
                results.append({
                    'parameter': param_name,
                    'parameter_value': param_value,
                    'total_revenue': revenue_data['total_revenue'],
                    'avg_effective_rate': progressivity_data['avg_effective_rate'],
                    'progressivity_index': progressivity_data['kakwani_index'],
                    'revenue_per_capita': revenue_data['revenue_per_capita']
                })
            
            sensitivity_results[param_name] = pd.DataFrame(results)
        
        return sensitivity_results
    
    def _modify_policy(self, base_policy: TaxPolicy, param_name: str, param_value: float) -> TaxPolicy:
        """Create a modified version of the base policy with a new parameter value."""
        # This is a simplified implementation
        # In practice, you'd need to handle different policy types and parameters
        if hasattr(base_policy, 'rate') and param_name == 'rate':
            from ..models.tax_policy import FlatTax
            return FlatTax(rate=param_value, name=f"{base_policy.name} (rate={param_value})")
        else:
            return base_policy
    
    def create_policy_summary(self, policies: List[TaxPolicy], 
                            income_distribution: pd.DataFrame) -> pd.DataFrame:
        """
        Create a summary table comparing all policies.
        
        Args:
            policies: List of tax policies to compare
            income_distribution: Income distribution data
            
        Returns:
            DataFrame with policy summary
        """
        summary_data = []
        
        for policy in policies:
            # Calculate basic metrics
            revenue_data = self.revenue_calculator.calculate_revenue(policy, income_distribution.copy())
            progressivity_data = self.tax_burden_analyzer.calculate_tax_progressivity(
                income_distribution.copy(), policy
            )
            
            summary_data.append({
                'policy_name': policy.name,
                'total_revenue': revenue_data['total_revenue'],
                'revenue_per_capita': revenue_data['revenue_per_capita'],
                'avg_effective_rate': progressivity_data['avg_effective_rate'],
                'progressivity_index': progressivity_data['kakwani_index'],
                'tax_progressivity': progressivity_data['tax_progressivity']
            })
        
        return pd.DataFrame(summary_data) 