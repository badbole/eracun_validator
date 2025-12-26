# Manual Asset Download Guide

This document describes **all external assets** required by `eracun_validator`
and how to obtain them **manually**, when automatic download is unavailable
(offline, CI lockdown, audit environments).

Assets are **not bundled** with the Python package.

---

## Asset root directory

By default, assets must live inside the project at:

eracun_validator/assets


If you use a custom asset root, the **internal folder structure must remain
exactly the same**.

---

## Mandatory asset groups

The validator will refuse to run if required assets are missing.

---

## 1. ISO Schematron engine (MANDATORY)

ISO Schematron XSLT files are required to compile `.sch` rules into SVRL.

### Primary source (preferred)

GitHub releases:

https://github.com/Schematron/schematron/releases

### Recommended version

schematron-1.6.2,zip
or https://github.com/Schematron/schematron/releases/download/2020-10-01/iso-schematron-xslt2.zip
or https://github.com/Schematron/schematron/releases/download/2017-02-09/iso-schematron-xslt2.zip

(If unavailable, use the **latest 1.6.x** release.)

### Required files inside ZIP

Extract **all** XSL files from:  
schematron/code

### Target directory

assets/schematron/iso/


After extraction, at minimum, the following **must exist**:

assets/schematron/iso/
├─ iso_svrl_for_xslt2.xsl
├─ iso_abstract_expand.xsl
├─ iso_dsdl_include.xsl
├─ iso_schematron_skeleton_for_saxon.xsl


### Fallback (manual search)

If releases change structure:

1. Open repository root:  
   https://github.com/Schematron/schematron
2. Navigate to `trunk/schematron/code`
3. Download **all `.xsl` files**
4. Place them into `assets/schematron/iso/`

---

## 2. EN 16931 Schematron (MANDATORY)

Base EN16931 validation rules.

### Primary source

https://github.com/CenPC434/validation/releases

### Required file

EN16931-UBL-validation.sch


### Target directory

assets/schematron/en16931/


### Fallback

If filename changes:

1. Open: https://github.com/CenPC434/validation
2. Browse `rules/ubl/`
3. Locate the **main EN16931 UBL validation `.sch`**
4. Copy it into the target directory

Exactly **one** `.sch` file is expected here.

---

## 3. PEPPOL BIS Billing 3 Schematron

Required when validating PEPPOL invoices.

### Primary source

https://github.com/OpenPEPPOL/peppol-bis-invoice-3

### Where to look

- Repository `rules/` directory
- Or latest release assets

### Required content

All `.sch` files required by the PEPPOL BIS 3 rule set.

### Target directory

assets/schematron/peppol/


### Fallback instructions

If release ZIPs are missing or renamed:

1. Open repository:  
   https://github.com/OpenPEPPOL/peppol-bis-invoice-3
2. Navigate to:

rules/

3. Download:
- Main `.sch`
- Any included `.sch` files
4. Preserve relative includes

---

## 4. HR-CIUS Schematron (Croatia, 2025)

Mandatory for Croatian fiscalization.

### Official source (current)

https://porezna.gov.hr/fiskalizacija/api/dokumenti/147

### ZIP contents

The ZIP typically contains:
- One main `.sch` file
- Include folders
- Documentation (PDF / TXT)

### Target directory

assets/schematron/hr-cius/


### Rules

- Extract **everything**
- Exactly **one main `.sch` entry point** is expected
- Include folders must stay relative

### Fallback

If the link changes:

1. Open: https://porezna.gov.hr → Fiskalizacija
2. Search for **HR-CIUS EN16931 UBL**
3. Download the latest validation package
4. Extract as-is into target folder

---

## 5. UBL 2.1 XSD base schemas (MANDATORY)

Used for Invoice and Credit Note validation.

### Official source

https://docs.oasis-open.org/ubl/os-UBL-2.1/

### Direct ZIP

UBL-2.1.zip


### IMPORTANT

Use **only** the `xsd/` directory from the ZIP.

### Target directory

assets/xsd/ubl-2.1/


After extraction, this **must exist**:

assets/xsd/ubl-2.1/maindoc/
├─ UBL-Invoice-2.1.xsd
└─ UBL-CreditNote-2.1.xsd


---

## 6. HR-CIUS UBL localization XSD (MANDATORY for Croatia)

Croatian localization of UBL XSDs.

### Official source

https://porezna.gov.hr/fiskalizacija/api/dokumenti/96

### ZIP behavior

This ZIP may contain:
- Nested folders
- Another `ubl.zip`
- Mixed casing

### Required final result

Regardless of structure, you must end with:

assets/xsd/hr-cius/ubl/
├─ maindoc/
├─ common/


The folder **must be named exactly `ubl`** (lowercase).

### Fallback

If structure is unclear:

1. Search ZIP for folders named:
maindoc
common

2. Move their parent folder to:
assets/xsd/hr-cius/ubl


---

## 7. Sample documents (OPTIONAL)

Used for tests and development only.

---

### 7.1 PEPPOL samples

#### Source

https://github.com/OpenPEPPOL/peppol-bis-invoice-3

Search for:
- `examples`
- `sample`
- `test` folders

#### Target

assets/sample/peppol/
├─ valid/
└─ invalid/


---

### 7.2 HR-CIUS samples

#### Official source

https://porezna.gov.hr/fiskalizacija/api/dokumenti/158

#### Target

assets/sample/hr-cius/
├─ valid/
└─ invalid/


---

## Profile detection impact

Assets used depend on detected profile:

| Profile | Requires |
|------|--------|
| EN16931 | ISO + EN16931 + UBL XSD |
| PEPPOL | + PEPPOL Schematron |
| HR-CIUS | + HR Schematron + HR XSD |
| CreditNote | Same XSDs, different maindoc |

---

## Troubleshooting

### Error: `iso_svrl_for_xslt2.xsl not found`

Cause: ISO Schematron files missing or incomplete.

Fix:
- Ensure **all ISO XSL files** are present in `schematron/iso`

---

### Error: `XSD not found`

Cause:
- `assets/xsd/ubl-2.1` missing
- HR-CIUS localization missing

Fix:
- Verify `maindoc` contains Invoice and CreditNote XSDs

---

### Error: `Profile detected but XSD missing`

Cause:
- HR-CIUS profile detected
- HR XSD not installed

Fix:
- Install HR-CIUS UBL localization

---

## Validation behavior when assets missing

- **CLI**: warns and offers to download
- **Python API**: raises `AssetsNotInstalledError`

---

## Recommendation

Whenever possible, use:

```bash
python -m eracun_validator download
