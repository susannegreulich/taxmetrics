"""
Interactive dashboards for tax policy analysis.
"""

import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, List
try:
    from ..models.tax_policy import TaxPolicy
    from ..analysis.revenue_calculator import RevenueCalculator
    from ..analysis.policy_comparator import PolicyComparator
    from ..visualization.charts import TaxPolicyCharts
except ImportError:
    from models.tax_policy import TaxPolicy
    from analysis.revenue_calculator import RevenueCalculator
    from analysis.policy_comparator import PolicyComparator
    from visualization.charts import TaxPolicyCharts


class PolicyDashboard:
    """Interactive web dashboard for tax policy analysis."""
    
    def __init__(self):
        """Initialize the dashboard."""
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.revenue_calculator = RevenueCalculator()
        self.policy_comparator = PolicyComparator()
        self.charts = TaxPolicyCharts()
        
        self.setup_layout()
        self.setup_callbacks()
    
    def setup_layout(self):
        """Set up the dashboard layout."""
        self.app.layout = dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H1("Tax Policy Analysis Dashboard", className="text-center mb-4"),
                    html.P("Interactive analysis of tax policies and their revenue implications", 
                           className="text-center text-muted")
                ])
            ]),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Tax Policy Parameters"),
                        dbc.CardBody([
                            html.Label("Progressive Tax Brackets:"),
                            dcc.Textarea(
                                id="progressive-brackets",
                                value="0,10000,0.10\n10000,40000,0.15\n40000,80000,0.25\n80000,160000,0.30\n160000,inf,0.35",
                                rows=6,
                                style={"width": "100%"}
                            ),
                            html.Br(),
                            html.Label("Flat Tax Rate:"),
                            dcc.Slider(
                                id="flat-tax-rate",
                                min=0.05,
                                max=0.50,
                                step=0.01,
                                value=0.25,
                                marks={i/10: f"{i*10}%" for i in range(1, 6)},
                                tooltip={"placement": "bottom", "always_visible": True}
                            ),
                            html.Br(),
                            html.Label("Population Size:"),
                            dcc.Slider(
                                id="population-size",
                                min=100000,
                                max=10000000,
                                step=100000,
                                value=1000000,
                                marks={i*1000000: f"{i}M" for i in range(1, 11)},
                                tooltip={"placement": "bottom", "always_visible": True}
                            ),
                            html.Br(),
                            dbc.Button("Update Analysis", id="update-button", color="primary", className="w-100")
                        ])
                    ])
                ], width=3),
                
                dbc.Col([
                    dbc.Tabs([
                        dbc.Tab([
                            dcc.Graph(id="tax-burden-chart")
                        ], label="Tax Burden"),
                        dbc.Tab([
                            dcc.Graph(id="revenue-chart")
                        ], label="Revenue"),
                        dbc.Tab([
                            dcc.Graph(id="progressivity-chart")
                        ], label="Progressivity"),
                        dbc.Tab([
                            dcc.Graph(id="efficiency-chart")
                        ], label="Efficiency")
                    ])
                ], width=9)
            ]),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Analysis Results"),
                        dbc.CardBody([
                            html.Div(id="results-table")
                        ])
                    ])
                ])
            ], className="mt-4")
        ], fluid=True)
    
    def setup_callbacks(self):
        """Set up dashboard callbacks."""
        @self.app.callback(
            [Output("tax-burden-chart", "figure"),
             Output("revenue-chart", "figure"),
             Output("progressivity-chart", "figure"),
             Output("efficiency-chart", "figure"),
             Output("results-table", "children")],
            [Input("update-button", "n_clicks")],
            [dash.dependencies.State("progressive-brackets", "value"),
             dash.dependencies.State("flat-tax-rate", "value"),
             dash.dependencies.State("population-size", "value")]
        )
        def update_analysis(n_clicks, progressive_brackets, flat_rate, population_size):
            if n_clicks is None:
                return dash.no_update
            
            # Parse progressive brackets
            brackets = []
            for line in progressive_brackets.strip().split('\n'):
                if line.strip():
                    parts = line.split(',')
                    min_income = float(parts[0])
                    max_income = float('inf') if parts[1] == 'inf' else float(parts[1])
                    rate = float(parts[2])
                    brackets.append((min_income, max_income, rate))
            
            # Create tax policies
            progressive_tax = TaxPolicy(brackets=brackets, name="Progressive Tax")
            flat_tax = TaxPolicy(rate=flat_rate, name=f"Flat Tax ({flat_rate:.1%})")
            
            policies = [progressive_tax, flat_tax]
            
            # Generate income distribution
            income_distribution = self.revenue_calculator.generate_income_distribution(
                population_size=population_size
            )
            
            # Perform analysis
            comparison_results = self.policy_comparator.comprehensive_comparison(
                policies, income_distribution
            )
            
            # Create charts
            tax_burden_fig = self.charts.plot_tax_burden_comparison(policies)
            revenue_fig = self.charts.plot_revenue_comparison(comparison_results['revenue_comparison'])
            progressivity_fig = self.charts.plot_progressivity_comparison(comparison_results['progressivity_analysis'])
            efficiency_fig = self.charts.plot_efficiency_metrics(
                self.policy_comparator.calculate_efficiency_metrics(policies, income_distribution)
            )
            
            # Create results table
            results_table = self.create_results_table(comparison_results)
            
            return tax_burden_fig, revenue_fig, progressivity_fig, efficiency_fig, results_table
    
    def create_results_table(self, comparison_results):
        """Create a results table for display."""
        revenue_data = comparison_results['revenue_comparison']
        progressivity_data = comparison_results['progressivity_analysis']
        
        table_rows = []
        for _, row in revenue_data.iterrows():
            policy_name = row['policy_name']
            progressivity_row = progressivity_data[progressivity_data['policy_name'] == policy_name].iloc[0]
            
            table_rows.append(html.Tr([
                html.Td(policy_name),
                html.Td(f"${row['total_revenue']:,.0f}"),
                html.Td(f"{row['average_effective_rate']:.1%}"),
                html.Td(f"{progressivity_row['kakwani_index']:.3f}"),
                html.Td(progressivity_row['tax_progressivity'])
            ]))
        
        return dbc.Table([
            html.Thead([
                html.Tr([
                    html.Th("Policy"),
                    html.Th("Total Revenue"),
                    html.Th("Avg Tax Rate"),
                    html.Th("Kakwani Index"),
                    html.Th("Progressivity")
                ])
            ]),
            html.Tbody(table_rows)
        ], bordered=True, hover=True, responsive=True, striped=True)
    
    def run(self, debug=True, port=8050):
        """Run the dashboard."""
        self.app.run_server(debug=debug, port=port)


def create_dashboard():
    """Create and return a dashboard instance."""
    return PolicyDashboard() 