# Core Validator Architecture — eracun_validator (v0.3.1)

## Purpose

The **core validator** orchestrates the complete validation lifecycle.
It is responsible for:

- Input handling (file path or XML string)
- XML parsing and sanity checks
- Profile detection
- Ordered execution of validators
- Result aggregation

The core contains **no standard-specific logic** — all behavior is
delegated to profile configuration and validator modules.

---

## High-Level Flow

```
validate(input)
 ├─ parse XML
 ├─ detect profile
 ├─ detect document type
 ├─ XSD validation (mandatory)
 ├─ Schematron validation (conditional)
 └─ return ValidationResult
```

---

## Responsibilities

### Input Handling
- Accepts file path or raw XML string
- Normalizes input into a temporary XML file
- Ensures well-formed XML before further processing

### Profile Detection
- Delegated to `profiles`
- Based on:
  - CustomizationID
  - Extension namespaces
- Result is a **single immutable profile configuration**

### Document Detection
- Structural detection
- Based on XML root element
- Mapped to available XSD documents in `maindoc/`

No document assumptions exist in code.

---

## Validator Orchestration

Execution order is **strict and enforced**:

1. XSD validator  
   - Always executed
   - Fatal on error
2. Schematron validator  
   - Executed only if XSD succeeds
   - Ordered chain from profile config

This ordering is non-negotiable.

---

## Result Aggregation

The core owns the `ValidationResult` lifecycle:

- Initialized once per validation
- Passed to validators for enrichment
- Responsible for:
  - Error/warning aggregation
  - Metadata (profile, document type, timestamps)

Validators never return raw results.

---

## Error Strategy

- XSD errors abort validation
- Schematron errors accumulate
- Tooling/runtime failures are surfaced as internal errors

This guarantees predictable outputs.

---

## File Layout

```
validator/
├── core.py        # orchestration logic
├── profiles.py    # profile detection + config
├── result.py      # validation result model
├── xsd.py         # XSD validator
└── schematron.py  # Schematron validator
```

---

## Configuration-Driven Design

The core:
- Does not contain hardcoded paths
- Does not branch on standards
- Does not know CIUS specifics

All behavior is driven by the profile dictionary.

---

## Extensibility

Adding a new validation standard requires:
1. New profile entry
2. Assets in correct folders
3. Zero core changes

This is intentional and enforced.

---

## Non-Goals

The core will **never**:
- Modify validation rules
- Interpret business semantics
- Suppress errors
- Generate invalid samples

Such logic belongs to policy or test layers.

---

## Status

✔ Stable  
✔ Deterministic  
✔ Configuration-driven  
✔ Frozen  

**Frozen as of v0.3.1**
