"""
Tax policy models for economic analysis.
"""

from .tax_policy import TaxPolicy, ProgressiveTax, FlatTax, RegressiveTax, CustomTax

__all__ = [
    "TaxPolicy",
    "ProgressiveTax", 
    "FlatTax",
    "RegressiveTax",
    "CustomTax"
] 