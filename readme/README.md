# eRačun Validator

**eRačun Validator** is a command-line and programmatic tool for validating electronic invoices
and credit notes based on **UBL 2.1**, **EN 16931**, and **HR-CIUS** rules.

It performs:
1. **Structural validation (XSD)**
2. **Business rules validation (Schematron)**

Validation is executed in the officially defined order and uses authoritative rule sources.

---

## Supported Standards & Profiles

### Currently supported

- **UBL 2.1**
  - Invoice
  - Credit Note
- **EN 16931**
  - Semantic data model rules
- **HR-CIUS (Croatia)**
  - EN 16931 national extension (Fiskalizacija 2.0)

### Planned / extensible

- Additional national CIUS profiles
- PEPPOL-specific constraints
- Policy-based rule selection

---

## Installation

### Requirements

- Python **3.9+**
- Java **11+**
- Internet access (first run only, for asset download)

### Install (editable / development)

```bash
pip install -e .
```

---

## First-time setup (assets)

Before validating documents, you must download and prepare validation assets:

```bash
python3 -m eracun_validator build
```

This will download:
- XSD schemas (UBL, HR-CIUS)
- Schematron rules (EN 16931, HR-CIUS)
- Java dependencies (Saxon, xmlresolver)

Assets are stored locally and reused.

---

## Validate a document

### Command-line usage

```bash
python3 -m eracun_validator validate invoice.xml
```

### Example output

```text
ERROR: [BR-CO-10] Seller VAT identifier is missing [schematron:en16931]
ERROR: [HR-EXT-01] HR fiscal extension missing [schematron:hr-cius]
```

### Exit codes

| Code | Meaning |
|----|-------|
| `0` | Validation passed |
| `1` | Validation errors found |
| `2` | Technical error |

---

## What happens during validation

1. XML is parsed and checked for well-formedness
2. Document type is detected (Invoice / Credit Note)
3. Profile is detected (EN 16931, HR-CIUS, …)
4. **XSD validation** is executed
   - validation stops if XSD fails
5. **Schematron validation** is executed
   - EN 16931 first
   - HR-CIUS rules applied afterwards (if detected)

---

## Profiles & Detection

Validation **profiles are structural**, not document-specific.

Detection is based on:
- `CustomizationID`
- Namespaces
- Known CIUS extensions

You do **not** need to manually select a profile.

---

## Assets & Offline Use

Once downloaded, assets are reused:
- No repeated downloads
- Schematron compilation is cached
- Works fully offline after first build

Assets live under:

```
eracun_validator/assets/
```

---

## Documentation

### For users
- `readme/CLI.md`
- `readme/INSTALL.md`
- `readme/PROFILES.md`
- `readme/HR-CIUS.md`

### For developers
See `docs/` for full technical documentation and architecture diagrams.

---

## Versioning & Stability

- Validator behavior is **versioned and frozen**
- Changes to rules or logic always bump versions
- No silent changes

Current frozen version:
```
v0.3.1
```

---

## Disclaimer

This tool validates conformance with published standards but does not replace
legal, fiscal, or regulatory review.

Always v