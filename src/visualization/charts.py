"""
Charting and visualization tools for tax policy analysis.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
try:
    from ..models.tax_policy import TaxPolicy
except ImportError:
    from models.tax_policy import TaxPolicy


class TaxPolicyCharts:
    """Create various charts for tax policy analysis."""
    
    def __init__(self, style: str = "seaborn"):
        """
        Initialize the charting class.
        
        Args:
            style: Plotting style ('seaborn', 'matplotlib', 'plotly')
        """
        self.style = style
        if style == "seaborn":
            sns.set_style("whitegrid")
            plt.rcParams['figure.figsize'] = (12, 8)
    
    def plot_tax_burden_comparison(self, policies: List[TaxPolicy], 
                                  income_range: Tuple[float, float] = (0, 200000),
                                  num_points: int = 1000) -> go.Figure:
        """
        Create a plot comparing tax burden across different policies.
        
        Args:
            policies: List of tax policies to compare
            income_range: Range of incomes to plot
            num_points: Number of points to plot
            
        Returns:
            Plotly figure object
        """
        incomes = np.linspace(income_range[0], income_range[1], num_points)
        
        fig = go.Figure()
        
        for policy in policies:
            taxes = [policy.calculate_tax(income) for income in incomes]
            effective_rates = [policy.calculate_effective_rate(income) for income in incomes]
            
            # Tax burden plot
            fig.add_trace(go.Scatter(
                x=incomes,
                y=taxes,
                mode='lines',
                name=f'{policy.name} - Tax Burden',
                line=dict(width=2)
            ))
            
            # Effective rate plot
            fig.add_trace(go.Scatter(
                x=incomes,
                y=effective_rates,
                mode='lines',
                name=f'{policy.name} - Effective Rate',
                line=dict(width=2, dash='dash'),
                yaxis='y2'
            ))
        
        fig.update_layout(
            title='Tax Burden Comparison Across Policies',
            xaxis_title='Income ($)',
            yaxis_title='Tax Burden ($)',
            yaxis2=dict(
                title='Effective Tax Rate',
                overlaying='y',
                side='right',
                range=[0, 0.5]
            ),
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig
    
    def plot_revenue_comparison(self, revenue_data: pd.DataFrame) -> go.Figure:
        """
        Create a bar chart comparing revenue across policies.
        
        Args:
            revenue_data: DataFrame with revenue comparison data
            
        Returns:
            Plotly figure object
        """
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=revenue_data['policy_name'],
            y=revenue_data['total_revenue'],
            text=[f"${x:,.0f}" for x in revenue_data['total_revenue']],
            textposition='auto',
            name='Total Revenue'
        ))
        
        fig.update_layout(
            title='Total Revenue by Tax Policy',
            xaxis_title='Tax Policy',
            yaxis_title='Total Revenue ($)',
            showlegend=False
        )
        
        return fig
    
    def plot_tax_burden_by_income_groups(self, tax_burden_data: pd.DataFrame) -> go.Figure:
        """
        Create a stacked bar chart showing tax burden by income group.
        
        Args:
            tax_burden_data: DataFrame with tax burden analysis data
            
        Returns:
            Plotly figure object
        """
        policies = tax_burden_data['policy_name'].unique()
        
        fig = go.Figure()
        
        for policy in policies:
            policy_data = tax_burden_data[tax_burden_data['policy_name'] == policy]
            
            fig.add_trace(go.Bar(
                x=policy_data['income_group'],
                y=policy_data['avg_effective_rate'],
                name=policy,
                text=[f"{x:.1%}" for x in policy_data['avg_effective_rate']],
                textposition='auto'
            ))
        
        fig.update_layout(
            title='Average Effective Tax Rate by Income Group',
            xaxis_title='Income Group',
            yaxis_title='Average Effective Tax Rate',
            barmode='group'
        )
        
        return fig
    
    def plot_progressivity_comparison(self, progressivity_data: pd.DataFrame) -> go.Figure:
        """
        Create a comparison of progressivity metrics across policies.
        
        Args:
            progressivity_data: DataFrame with progressivity data
            
        Returns:
            Plotly figure object
        """
        fig = go.Figure()
        
        # Kakwani index
        fig.add_trace(go.Bar(
            x=progressivity_data['policy_name'],
            y=progressivity_data['kakwani_index'],
            name='Kakwani Index',
            marker_color='lightblue',
            text=[f"{x:.3f}" for x in progressivity_data['kakwani_index']],
            textposition='auto'
        ))
        
        fig.update_layout(
            title='Tax Progressivity Comparison (Kakwani Index)',
            xaxis_title='Tax Policy',
            yaxis_title='Kakwani Index',
            showlegend=False
        )
        
        return fig
    
    def plot_tax_incidence(self, incidence_data: pd.DataFrame) -> go.Figure:
        """
        Create a stacked bar chart showing tax incidence by income group.
        
        Args:
            incidence_data: DataFrame with tax incidence data
            
        Returns:
            Plotly figure object
        """
        policies = incidence_data['policy_name'].unique()
        
        fig = go.Figure()
        
        for policy in policies:
            policy_data = incidence_data[incidence_data['policy_name'] == policy]
            
            fig.add_trace(go.Bar(
                x=policy_data['income_group'],
                y=policy_data['share_of_total_tax'],
                name=policy,
                text=[f"{x:.1%}" for x in policy_data['share_of_total_tax']],
                textposition='auto'
            ))
        
        fig.update_layout(
            title='Share of Total Tax Burden by Income Group',
            xaxis_title='Income Group',
            yaxis_title='Share of Total Tax Burden',
            barmode='group'
        )
        
        return fig
    
    def plot_efficiency_metrics(self, efficiency_data: pd.DataFrame) -> go.Figure:
        """
        Create a radar chart showing efficiency metrics.
        
        Args:
            efficiency_data: DataFrame with efficiency metrics
            
        Returns:
            Plotly figure object
        """
        policies = efficiency_data['policy_name'].unique()
        
        # Normalize metrics for radar chart
        metrics = ['total_revenue', 'avg_effective_rate', 'progressivity_index', 'revenue_efficiency']
        
        fig = go.Figure()
        
        for policy in policies:
            policy_data = efficiency_data[efficiency_data['policy_name'] == policy].iloc[0]
            
            values = []
            for metric in metrics:
                if metric in policy_data:
                    # Normalize to 0-1 scale
                    all_values = efficiency_data[metric]
                    normalized_value = (policy_data[metric] - all_values.min()) / (all_values.max() - all_values.min())
                    values.append(normalized_value)
                else:
                    values.append(0)
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=metrics,
                fill='toself',
                name=policy
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=True,
            title='Tax Policy Efficiency Comparison'
        )
        
        return fig
    
    def plot_sensitivity_analysis(self, sensitivity_data: Dict[str, pd.DataFrame]) -> go.Figure:
        """
        Create line plots for sensitivity analysis.
        
        Args:
            sensitivity_data: Dictionary with sensitivity analysis results
            
        Returns:
            Plotly figure object
        """
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=list(sensitivity_data.keys()),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        row, col = 1, 1
        for param_name, data in sensitivity_data.items():
            if row > 2:
                break
                
            fig.add_trace(
                go.Scatter(
                    x=data['parameter_value'],
                    y=data['total_revenue'],
                    mode='lines+markers',
                    name=f'{param_name} - Revenue'
                ),
                row=row, col=col
            )
            
            fig.add_trace(
                go.Scatter(
                    x=data['parameter_value'],
                    y=data['avg_effective_rate'],
                    mode='lines+markers',
                    name=f'{param_name} - Effective Rate',
                    yaxis='y2'
                ),
                row=row, col=col
            )
            
            col += 1
            if col > 2:
                col = 1
                row += 1
        
        fig.update_layout(
            title='Sensitivity Analysis Results',
            height=800
        )
        
        return fig
    
    def create_comprehensive_dashboard(self, comparison_results: Dict[str, pd.DataFrame]) -> go.Figure:
        """
        Create a comprehensive dashboard with multiple charts.
        
        Args:
            comparison_results: Dictionary with comparison results
            
        Returns:
            Plotly figure object
        """
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=['Revenue Comparison', 'Tax Burden by Income Group', 
                          'Progressivity Comparison', 'Tax Incidence'],
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "bar"}]]
        )
        
        # Revenue comparison
        if 'revenue_comparison' in comparison_results:
            revenue_data = comparison_results['revenue_comparison']
            fig.add_trace(
                go.Bar(x=revenue_data['policy_name'], y=revenue_data['total_revenue']),
                row=1, col=1
            )
        
        # Tax burden by income group
        if 'tax_burden_analysis' in comparison_results:
            tax_burden_data = comparison_results['tax_burden_analysis']
            policies = tax_burden_data['policy_name'].unique()
            for i, policy in enumerate(policies):
                policy_data = tax_burden_data[tax_burden_data['policy_name'] == policy]
                fig.add_trace(
                    go.Bar(x=policy_data['income_group'], y=policy_data['avg_effective_rate'], name=policy),
                    row=1, col=2
                )
        
        # Progressivity comparison
        if 'progressivity_analysis' in comparison_results:
            progressivity_data = comparison_results['progressivity_analysis']
            fig.add_trace(
                go.Bar(x=progressivity_data['policy_name'], y=progressivity_data['kakwani_index']),
                row=2, col=1
            )
        
        # Tax incidence
        if 'incidence_analysis' in comparison_results:
            incidence_data = comparison_results['incidence_analysis']
            policies = incidence_data['policy_name'].unique()
            for i, policy in enumerate(policies):
                policy_data = incidence_data[incidence_data['policy_name'] == policy]
                fig.add_trace(
                    go.Bar(x=policy_data['income_group'], y=policy_data['share_of_total_tax'], name=policy),
                    row=2, col=2
                )
        
        fig.update_layout(
            title='Tax Policy Analysis Dashboard',
            height=800,
            showlegend=True
        )
        
        return fig 