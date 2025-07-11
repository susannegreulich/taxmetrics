"""
Data collection tools for economic analysis.
"""

from .oecd_data_collector import OECDDataCollector
from .tax_data_processor import TaxDataProcessor

__all__ = [
    "OECDDataCollector",
    "TaxDataProcessor"
] 