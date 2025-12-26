# asset_builder/__init__.py

"""
Asset Builder for eracun-validator

Responsible for:
- Downloading XSD assets (UBL 2.1, HR-CIUS)
- Downloading ISO Schematron engine files
- Downloading sample documents
- Providing a stable on-disk asset contract for the validator

CLI entrypoint:
    python -m eracun_validator.asset_builder
"""

__all__ = [
    "BaseDownloader",
    "SchematronDownloader",
    "XsdDownloader",
    "SampleDownloader",
]

from .base import BaseDownloader
from .schematron import SchematronDownloader
from .xsd import XsdDownloader
from .samples import SampleDownloader
