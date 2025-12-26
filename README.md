# eRacun Validator

A production-grade validator for **UBL 2.1 electronic invoices and credit notes**, supporting:

- EN 16931
- PEPPOL BIS Billing 3
- Croatian HR-CIUS (2025)
- XSD + Schematron validation
- CLI and Python API

---

## Features

- Automatic profile detection (PEPPOL / HR-CIUS / EN16931)
- Phase-aware Schematron validation
- ISO Schematron (SVRL) execution via Saxon
- Effective validation stack reporting (JSON)
- Offline-capable asset management
- Credit Note support
- Designed for FINA / Croatian eRačun ecosystem

---

## Quick start

```bash
pip install eracun-validator
python -m eracun_validator download
eracun-validator validate invoice.xml
```