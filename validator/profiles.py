# eracun_validator/validator/profiles.py

import os
from lxml import etree

# =============================================================================
# Static profile registry
# =============================================================================

PROFILE_REGISTRY = {
    "en16931": {
        "id": "en16931",
        "label": "EN 16931",
        "customization_id": None,
        "required_namespaces": [],
        "xsd": {
            "path": ["xsd", "ubl-2.1", "xsd", "maindoc"],
        },
        "schematron": {
            "iso": ["schematron", "iso"],
            "stages": [
                {
                    "id": "en16931",
                    "path": ["schematron", "en16931"],
                    "driver_xsl": "EN16931-UBL-validation.xsl",
                }
            ],
        },
    },
    "hr-cius": {
        "id": "hr-cius",
        "label": "HR CIUS 2025",

        "customization_id": (
            "urn:cen.eu:en16931:2017#compliant#"
            "urn:mfin.gov.hr:cius-2025:1.0#conformant#"
            "urn:mfin.gov.hr:ext-2025:1.0"
        ),
        "required_namespaces": [
            "urn:hzn.hr:schema:xsd:HRExtensionAggregateComponents-1"
        ],

        "xsd": {
            "path": ["xsd", "hr-cius", "ubl", "maindoc"],
        },

        "schematron": {
            "iso": ["schematron", "iso"],
            "stages": [
                {
                    "id": "en16931",
                    "path": ["schematron", "en16931"],
                    # --- NEW ---
                    "driver_xsl": "EN16931-UBL-validation.xsl",
                },
                {
                    "id": "hr-cius",
                    "path": ["schematron", "hr-cius"],
                    # --- NEW ---
                    "driver_xsl": "HR-CIUS-EXT-EN16931-UBL.xsl",
                },
            ],
        },
    },
}



# =============================================================================
# Helpers
# =============================================================================

def _get_text(xpath, root, ns):
    el = root.find(xpath, namespaces=ns)
    if el is not None and el.text:
        return el.text.strip()
    return None


def detect_document_type(xml_path):
    """
    Detect document type by root element name.
    """
    tree = etree.parse(xml_path)
    root = tree.getroot()

    local = etree.QName(root.tag).localname.lower()
    if "credit" in local:
        return "creditnote"
    return "invoice"


# =============================================================================
# Profile detection
# =============================================================================

def detect_profile(xml_path):
    """
    Detect profile using deterministic scoring instead of loop short-circuiting.
    """
    tree = etree.parse(xml_path)
    root = tree.getroot()

    nsmap = root.nsmap.copy()
    nsmap.setdefault(
        "cbc",
        "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
    )

    namespaces = set(nsmap.values())
    customization_id = _get_text(".//cbc:CustomizationID", root, nsmap)

    best_profile = PROFILE_REGISTRY["en16931"]
    best_score = 0

    for profile in PROFILE_REGISTRY.values():
        score = 0

        # --- CustomizationID match ---
        cid = profile.get("customization_id")
        if cid:
            if customization_id != cid:
                continue
            score += 10

        # --- Namespace match ---
        required_ns = profile.get("required_namespaces", [])
        if required_ns:
            if not all(ns in namespaces for ns in required_ns):
                continue
            score += len(required_ns)

        # --- Prefer more specific profiles ---
        if score > best_score:
            best_score = score
            best_profile = profile

    return best_profile



# =============================================================================
# Path resolver
# =============================================================================

def resolve_profile(profile, assets_root):
    resolved = dict(profile)

    # ---------------- XSD ----------------
    resolved["xsd"] = dict(profile["xsd"])
    resolved["xsd"]["path"] = os.path.join(
        assets_root, *profile["xsd"]["path"]
    )

    # ---------------- Schematron ----------------
    resolved["schematron"] = dict(profile["schematron"])
    resolved["schematron"]["iso"] = os.path.join(
        assets_root, *profile["schematron"]["iso"]
    )

    stages = []
    for stage in profile["schematron"]["stages"]:
        s = dict(stage)

        # resolve absolute path
        s["path"] = os.path.join(assets_root, *stage["path"])

        # 🚨 ENFORCE driver_xsl
        if "driver_xsl" not in s:
            raise KeyError(
                f"Schematron stage '{s.get('id')}' "
                f"is missing required key 'driver_xsl'"
            )

        stages.append(s)

    resolved["schematron"]["stages"] = stages
    return resolved

