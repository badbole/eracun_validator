# eRačun Validator – Command Line Interface

This document describes how to use **eRačun Validator** from the command line.

---

## Basic usage

All commands are executed via the Python module entry point:

```bash
python3 -m eracun_validator <command> [options]
```

Available commands:

- `build` – download and prepare validation assets
- `validate` – validate an XML invoice or credit note

---

## `build` command

### Purpose

Downloads and prepares all assets required for validation:

- XSD schemas
- Schematron rules
- Java dependencies (Saxon, xmlresolver)

Assets are downloaded **once** and reused.

### Usage

```bash
python3 -m eracun_validator build
```

### Behaviour

- Downloads only missing files
- Uses cached files if already present
- Safe to run multiple times

### Typical output

```text
Downloading UBL 2.1 XSD ... OK
Downloading EN16931 Schematron ... OK
Downloading HR-CIUS Schematron ... OK
Assets ready.
```

---

## `validate` command

### Purpose

Validates a single XML document according to detected profile rules.

### Usage

```bash
python3 -m eracun_validator validate <file.xml>
```

Example:

```bash
python3 -m eracun_validator validate invoice.xml
```

---

## Validation flow (CLI)

When you run `validate`, the following steps occur:

1. XML well-formedness check
2. Document type detection (Invoice / CreditNote)
3. Profile detection (EN16931, HR-CIUS, ...)
4. **XSD validation**
   - validation stops if XSD fails
5. **Schematron validation**
   - EN16931 rules
   - HR-CIUS rules (if detected)

---

## Output format

### Validation errors

Errors are printed to stderr:

```text
ERROR: [BR-CO-10] Seller VAT identifier is missing [schematron:en16931]
ERROR: [HR-EXT-01] HR fiscal extension missing [schematron:hr-cius]
```

### Successful validation

If no errors are found, the command exits silently with exit code `0`.

---

## Exit codes

| Code | Meaning |
|------|--------|
| `0` | Validation passed |
| `1` | Validation errors found |
| `2` | Technical error (configuration, assets, runtime) |

---

## CI / automation usage

Example shell usage:

```bash
python3 -m eracun_validator validate invoice.xml || exit 1
```

Example GitHub Actions step:

```yaml
- name: Validate eInvoice
  run: python3 -m eracun_validator validate invoice.xml
```

---

## Notes

- Only **one XML file** is validated per call
- Batch processing should be implemented by the caller
- Assets must be built before validation

---

## Help

To see built-in help:

```bash
python3 -m eracun_validator --help
python3 -m eracun_validator validate --help
```

---

## Version compatibility

This CLI documentation applies to:

```
v0.3.1 (frozen)