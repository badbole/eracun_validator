"""
Global configuration for eracun_validator.

This module defines:
- default paths
- supported versions
- well-known filenames

No runtime logic is allowed here.
"""

import os


# ============================================================
# ROOTS
# ============================================================


MODULE_ROOT = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ASSETS_ROOT = os.path.join(MODULE_ROOT, "assets")

# ============================================================
# JAVA
# ============================================================

JAVA_DIR = "java"

SAXON_JAR = "Saxon-HE-11.6.jar"
XMLRESOLVER_JAR = "xmlresolver-4.6.4.jar"


# ============================================================
# SCHEMATRON
# ============================================================

SCHEMATRON_DIR = "schematron"

ISO_SCHEMATRON_DIR = os.path.join(SCHEMATRON_DIR, "iso")

ISO_SVRL_XSL = "iso_svrl_for_xslt2.xsl"
ISO_SKELETON_XSL = "iso_schematron_skeleton_for_saxon.xsl"


EN16931_DIR = os.path.join(SCHEMATRON_DIR, "en16931")
EN16931_DEFAULT_VERSION = "3.0.18"
EN16931_MAIN_SCH = "EN16931-UBL-validation.sch"


HR_CIUS_DIR = os.path.join(SCHEMATRON_DIR, "hr-cius")
HR_CIUS_DEFAULT_VERSION = "2025"
HR_CIUS_MAIN_SCH = "hr-cius.sch"


SCHEMATRON_CACHE_DIR = os.path.join("cache", "schematron")


# ============================================================
# XSD / UBL
# ============================================================

XSD_DIR = "xsd"

UBL_DIR_PREFIX = "ubl-"
UBL_DEFAULT_VERSION = "2.1"

UBL_XSD_ROOT = "xsd"
UBL_MAIN_DOC_DIR = "maindoc"
UBL_COMMON_DIR = "common"

UBL_INVOICE_XSD = "UBL-Invoice-2.1.xsd"


HR_UBL_DIR = os.path.join("hr", "ubl")

XSD_SOURCES = {
    "en16931": {
        "type": "zip",
        "url": "https://docs.oasis-open.org/ubl/os-UBL-2.1/UBL-2.1.zip",
        "extract": "xsd",
    },
    "peppol": {
        "type": "zip",
        "url": "https://github.com/OpenPEPPOL/peppol-ubl/releases/latest/download/peppol-ubl.zip",
        "extract": "xsd",
    },
    "hr-cius": {
        "type": "zip",
        "url": "https://porezna.gov.hr/fiskalizacija/api/dokumenti/96",
        "extract": "ubl.zip",  # nested ZIP
    }
}
# ============================================================
# VALIDATION
# ============================================================

DEFAULT_PROFILE = "default"

SUPPORTED_DOCUMENTS = {
    "Invoice": "UBL-Invoice",
    "CreditNote": "UBL-CreditNote",
}


# ============================================================
# LOGGING
# ============================================================

LOG_NAMESPACE = "erv"
