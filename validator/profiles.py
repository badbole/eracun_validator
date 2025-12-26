from lxml import etree

# HR-CIUS full CustomizationID (Fiskalizacija 2.0 – CIUS 2025)
HR_CIUS_CUSTOMIZATION_ID = (
    "urn:cen.eu:en16931:2017#compliant#"
    "urn:mfin.gov.hr:cius-2025:1.0#conformant#"
    "urn:mfin.gov.hr:ext-2025:1.0"
)

# HR extension namespace (presence required for HR-CIUS)
HR_CIUS_NAMESPACE = "urn:hzn.hr:schema:xsd:HRExtensionAggregateComponents-1"


def _get_text(xpath, root, ns):
    """
    Safe XPath text resolver.
    """
    el = root.find(xpath, namespaces=ns)
    return el.text.strip() if el is not None and el.text else None


def detect_document_type(xml_path):
    """
    Detect UBL document type from root element.
    """
    tree = etree.parse(xml_path)
    root = tree.getroot()

    tag = etree.QName(root.tag).localname.lower()

    if "credit" in tag:
        return "creditnote"
    return "invoice"


def detect_profile(xml_path):
    """
    Detect validation profile (EN16931 or HR-CIUS).

    HR-CIUS is detected ONLY when:
    - CustomizationID matches the official HR CIUS identifier
    - HR extension namespace is present

    This prevents false positives on plain EN16931 invoices.
    """
    tree = etree.parse(xml_path)
    root = tree.getroot()

    ns = root.nsmap.copy()
    ns.setdefault(
        "cbc",
        "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
    )

    customization_id = _get_text(".//cbc:CustomizationID", root, ns)

    has_hrcius_id = customization_id == HR_CIUS_CUSTOMIZATION_ID
    has_hrcius_ns = HR_CIUS_NAMESPACE in ns.values()

    if has_hrcius_id and has_hrcius_ns:
        return {
            "id": "hr-cius",
            "label": "HR CIUS 2025",
            "base": "en16931",
            "validation_stack": [
                "xsd:ubl-2.1",
                "xsd:hr-cius",
                "schematron:en16931",
                # HR schematron MUST be executed AFTER EN16931
                "schematron:hr-cius",
            ],
            "fallbacks": {
                "xsd": "ubl-2.1",
            },
        }

    # Default EN 16931 validation profile
    return {
        "id": "en16931",
        "label": "EN 16931",
        "base": "ubl-2.1",
        "validation_stack": [
            "xsd:ubl-2.1",
            "schematron:en16931",
        ],
        "fallbacks": {},
    }
