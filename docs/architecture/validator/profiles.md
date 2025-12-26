# Validator Profiles Architecture

This document describes how validation profiles are structured, detected, and applied
inside the **eracun_validator** project.

Version: **v0.3.1 (frozen)**

---

## What is a Profile

A validation **profile** describes:

- Semantic standard (EN16931, HR‑CIUS, etc.)
- Required XSD layers
- Required Schematron layers
- Detection rules (CustomizationID, namespaces)
- Validation execution order

Profiles are **structure-based**, not document-type based.

Document types (Invoice, CreditNote, etc.) are detected separately
based on available XSDs inside the *maindoc* folder.

---

## Profile Detection Flow

1. XML is parsed
2. CustomizationID is extracted
3. Known namespaces are scanned
4. Matching profile is selected
5. Validation stack is built from profile config

---

## Profile Definition Model

Each profile is defined as a dictionary with the following keys:

```python
{
  "id": "hr-cius",
  "label": "HR CIUS 2025",
  "customization_id": "...",
  "base": "en16931",
  "xsd": {
      "root": "assets/xsd/hr-cius/ubl",
      "maindoc": "maindoc"
  },
  "schematron": [
      {
          "id": "en16931",
          "root": "assets/schematron/en16931",
          "main": "EN16931-UBL-validation.sch"
      },
      {
          "id": "hr-cius",
          "root": "assets/schematron/hr-cius",
          "main": "HR-CIUS-EXT-EN16931-UBL.sch"
      }
  ]
}
```

---

## Supported Profiles

### EN16931

- Base UBL 2.1 profile
- Uses official CEN schematron
- Applies to all compliant UBL invoices

### HR‑CIUS

- Extends EN16931
- Requires Croatian CIUS customization ID
- Adds HR-specific schematron rules
- Executed **after** EN16931 schematron

---

## Validation Order

For each profile:

1. XSD validation (must pass)
2. Schematron validation
   - EN16931 first
   - CIUS extensions second

Schematron is **skipped** if XSD fails.

---

## Extensibility

The profile system is designed to support:

- New national CIUS profiles
- Multiple document types per profile
- Optional validation layers

Adding a new profile requires only:

- Assets
- Profile dictionary entry

No core validator changes are required.

---

## Key Design Rules

- Profiles are deterministic
- Profiles are asset-driven
- No hardcoded paths in validator logic
- Profiles control validation stack composition

---

End of document.
