# asset_builder/config.py

# --------------------
# Java
# --------------------

JAVA = {
    "saxon-he": {
        "filename": "Saxon-HE-12.4.jar",
        "url": "https://repo1.maven.org/maven2/net/sf/saxon/Saxon-HE/12.4/Saxon-HE-12.4.jar",
    },
    "xmlresolver": {
        "filename": "xmlresolver-4.6.4.jar",
        "url": "https://repo1.maven.org/maven2/org/xmlresolver/xmlresolver/4.6.4/xmlresolver-4.6.4.jar",
    },
}

# --------------------
# XSD
# --------------------

XSD = {
    "ubl-2.1": {
        "filename": "UBL-2.1.zip",
        "url": "https://docs.oasis-open.org/ubl/os-UBL-2.1/UBL-2.1.zip",
        "required": True,
    },
    "hr-cius": {
        "filename": "HR-CIUS-XSD.zip",
        "url": "https://porezna.gov.hr/fiskalizacija/api/dokumenti/96",
        "required": True,
    },
    # "it-fatturapa": {
    #     "filename": "IT-FatturaPA-XSD.zip",
    #     "url": "https://example.org/it-fatturapa/IT-FatturaPA-XSD.zip",
    #     "required": False,
    # },
    # "de-xrechnung": {
    #     "filename": "DE-XRechnung-XSD.zip",
    #     "url": "https://example.org/de-xrechnung/DE-XRechnung-XSD.zip",
    #     "required": False,
    # },
    # "si-eslog": {
    #     "filename": "SI-eSlog-XSD.zip",
    #     "url": "https://example.org/si-eslog/SI-eSlog-XSD.zip",
    #     "required": False,
    # },
    # "peppol": {
    #     "filename": "PEPPOL-UBL-XSD.zip",
    #     "url": "https://example.org/peppol/PEPPOL-UBL-XSD.zip",
    #     "required": False,
    # },
}

# --------------------
# Schematron
# --------------------

SCHEMATRON = {
    "iso": {
        "filename": "iso-schematron-xslt2-2020-10-01.zip",
        "url": "https://github.com/Schematron/schematron/releases/download/2020-10-01/iso-schematron-xslt2.zip",
        "required": True,
    },
    "en16931": {
        "filename": "en16931-ubl-1.3.15.zip",
        "url": "https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/download/validation-1.3.15/en16931-ubl-1.3.15.zip",
        #"fallback_url": "https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/download/validation-1.3.15/en16931-ubl-1.3.15.zip",
        "required": True,
    },
    "hr-cius": {
        "filename": "HRUBLValidator.zip",
        "url": "https://porezna.gov.hr/fiskalizacija/api/dokumenti/147",
        "required": True,
    },
    # "it-fatturapa": {
    #     "filename": "IT-FatturaPA-Schematron.zip",
    #     "url": "https://example.org/it-fatturapa/IT-FatturaPA-Schematron.zip",
    #     "required": False,
    # },
    # "de-xrechnung": {
    #     "filename": "DE-XRechnung-Schematron.zip",
    #     "url": "https://example.org/de-xrechnung/DE-XRechnung-Schematron.zip",
    #     "required": False,
    # },
    # "si-eslog": {
    #     "filename": "SI-eSlog-Schematron.zip",
    #     "url": "https://example.org/si-eslog/SI-eSlog-Schematron.zip",
    #     "required": False,
    # },
    # "peppol": {
    #     "filename": "PEPPOL-Schematron.zip",
    #     "url": "https://example.org/peppol/PEPPOL-Schematron.zip",
    #     "required": False,
    # },
}

# --------------------
# Samples
# --------------------

SAMPLES = {

    "hr-cius": {
        "filename": "HR-CIUS-Samples.zip",
        "url": "https://porezna.gov.hr/fiskalizacija/api/dokumenti/158",
        "required": False,
    },
}
