"""
Tax policy models for economic analysis.

This module provides various tax policy implementations including progressive,
flat, regressive, and custom tax structures.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Any, Optional
import numpy as np
import pandas as pd


class TaxPolicy(ABC):
    """Abstract base class for tax policies."""
    
    def __init__(self, name: str = "Tax Policy"):
        self.name = name
    
    @abstractmethod
    def calculate_tax(self, income: float) -> float:
        """Calculate tax liability for a given income."""
        pass
    
    @abstractmethod
    def get_marginal_rate(self, income: float) -> float:
        """Get marginal tax rate at a given income level."""
        pass
    
    def calculate_effective_rate(self, income: float) -> float:
        """Calculate effective tax rate (total tax / income)."""
        if income <= 0:
            return 0.0
        return self.calculate_tax(income) / income


class ProgressiveTax(TaxPolicy):
    """Progressive tax system with multiple brackets."""
    
    def __init__(self, brackets: List[Tuple[float, float, float]], name: str = "Progressive Tax"):
        """
        Initialize progressive tax system.
        
        Args:
            brackets: List of (min_income, max_income, rate) tuples
            name: Name of the tax policy
        """
        super().__init__(name)
        self.brackets = sorted(brackets, key=lambda x: x[0])
        self._validate_brackets()
    
    def _validate_brackets(self):
        """Validate that brackets are properly formatted."""
        if not self.brackets:
            raise ValueError("At least one bracket must be provided")
        
        for i, (min_income, max_income, rate) in enumerate(self.brackets):
            if min_income < 0 or max_income < min_income or rate < 0:
                raise ValueError(f"Invalid bracket {i}: {min_income}, {max_income}, {rate}")
    
    def calculate_tax(self, income: float) -> float:
        """Calculate tax liability using progressive brackets."""
        if income <= 0:
            return 0.0
        
        total_tax = 0.0
        remaining_income = income
        
        for min_income, max_income, rate in self.brackets:
            if remaining_income <= 0:
                break
            
            bracket_income = min(remaining_income, max_income - min_income)
            if bracket_income > 0:
                total_tax += bracket_income * rate
                remaining_income -= bracket_income
        
        return total_tax
    
    def get_marginal_rate(self, income: float) -> float:
        """Get marginal tax rate at given income level."""
        if income <= 0:
            return 0.0
        
        for min_income, max_income, rate in self.brackets:
            if min_income <= income < max_income:
                return rate
        
        # If income exceeds all brackets, use the highest rate
        return self.brackets[-1][2]


class FlatTax(TaxPolicy):
    """Flat tax system with single rate."""
    
    def __init__(self, rate: float, name: str = "Flat Tax"):
        """
        Initialize flat tax system.
        
        Args:
            rate: Single tax rate (0.0 to 1.0)
            name: Name of the tax policy
        """
        super().__init__(name)
        if not 0 <= rate <= 1:
            raise ValueError("Tax rate must be between 0 and 1")
        self.rate = rate
    
    def calculate_tax(self, income: float) -> float:
        """Calculate tax liability using flat rate."""
        return max(0.0, income * self.rate)
    
    def get_marginal_rate(self, income: float) -> float:
        """Get marginal tax rate (same as flat rate)."""
        return self.rate


class RegressiveTax(TaxPolicy):
    """Regressive tax system with decreasing rates."""
    
    def __init__(self, brackets: List[Tuple[float, float, float]], name: str = "Regressive Tax"):
        """
        Initialize regressive tax system.
        
        Args:
            brackets: List of (min_income, max_income, rate) tuples with decreasing rates
            name: Name of the tax policy
        """
        super().__init__(name)
        self.brackets = sorted(brackets, key=lambda x: x[0])
        self._validate_brackets()
    
    def _validate_brackets(self):
        """Validate that brackets have decreasing rates."""
        if not self.brackets:
            raise ValueError("At least one bracket must be provided")
        
        for i, (min_income, max_income, rate) in enumerate(self.brackets):
            if min_income < 0 or max_income < min_income or rate < 0:
                raise ValueError(f"Invalid bracket {i}: {min_income}, {max_income}, {rate}")
        
        # Check that rates are decreasing
        for i in range(len(self.brackets) - 1):
            if self.brackets[i][2] < self.brackets[i + 1][2]:
                raise ValueError("Regressive tax must have decreasing rates")
    
    def calculate_tax(self, income: float) -> float:
        """Calculate tax liability using regressive brackets."""
        if income <= 0:
            return 0.0
        
        total_tax = 0.0
        remaining_income = income
        
        for min_income, max_income, rate in self.brackets:
            if remaining_income <= 0:
                break
            
            bracket_income = min(remaining_income, max_income - min_income)
            if bracket_income > 0:
                total_tax += bracket_income * rate
                remaining_income -= bracket_income
        
        return total_tax
    
    def get_marginal_rate(self, income: float) -> float:
        """Get marginal tax rate at given income level."""
        if income <= 0:
            return 0.0
        
        for min_income, max_income, rate in self.brackets:
            if min_income <= income < max_income:
                return rate
        
        # If income exceeds all brackets, use the lowest rate
        return self.brackets[-1][2]


class CustomTax(TaxPolicy):
    """Custom tax system with user-defined function."""
    
    def __init__(self, tax_function, marginal_rate_function, name: str = "Custom Tax"):
        """
        Initialize custom tax system.
        
        Args:
            tax_function: Function that takes income and returns tax liability
            marginal_rate_function: Function that takes income and returns marginal rate
            name: Name of the tax policy
        """
        super().__init__(name)
        self.tax_function = tax_function
        self.marginal_rate_function = marginal_rate_function
    
    def calculate_tax(self, income: float) -> float:
        """Calculate tax liability using custom function."""
        return self.tax_function(income)
    
    def get_marginal_rate(self, income: float) -> float:
        """Get marginal tax rate using custom function."""
        return self.marginal_rate_function(income)


# Factory function for common tax policies
def create_tax_policy(policy_type: str, **kwargs) -> TaxPolicy:
    """
    Factory function to create common tax policies.
    
    Args:
        policy_type: Type of tax policy ('progressive', 'flat', 'regressive')
        **kwargs: Parameters for the specific tax policy
    
    Returns:
        TaxPolicy instance
    """
    if policy_type.lower() == "progressive":
        return ProgressiveTax(**kwargs)
    elif policy_type.lower() == "flat":
        return FlatTax(**kwargs)
    elif policy_type.lower() == "regressive":
        return RegressiveTax(**kwargs)
    else:
        raise ValueError(f"Unknown tax policy type: {policy_type}") 