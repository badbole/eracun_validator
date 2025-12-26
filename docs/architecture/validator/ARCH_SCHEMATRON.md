# Schematron Architecture — eracun_validator (v0.3.1)

## Purpose

The Schematron subsystem enforces **semantic and business-rule validation**
after successful structural (XSD) validation.

It implements:
- EN 16931 business rules (official CEN artefacts)
- National CIUS extensions (e.g. HR-CIUS)
- ISO Schematron reference pipeline
- Deterministic rule chaining with caching

---

## Validation Order

Schematron validation **only runs if XSD validation passes**.

Execution order is fully **profile-driven**:

1. EN16931 Schematron
2. CIUS / national extension Schematron(s)
3. Optional future profiles (PEPPOL, national extensions)

---

## Directory Layout

```
assets/schematron/
├── iso/
│   ├── iso_schematron_skeleton_for_saxon.xsl
│   ├── iso_svrl_for_xslt2.xsl
│   ├── iso_abstract_expand.xsl
│   └── iso_dsdl_include.xsl
│
├── en16931/
│   ├── EN16931-UBL-validation.sch        # entry point
│   ├── abstract/
│   ├── codelist/
│   ├── UBL/
│   └── preprocessed/                     # optional upstream artefacts
│
└── hr-cius/
    ├── HR-CIUS-EXT-EN16931-UBL.sch        # entry point
    └── codelist/
```

---

## ISO Schematron Pipeline

The implementation follows the **official ISO 19757-3 pipeline**:

1. `.sch` source file
2. Compiled via `iso_schematron_skeleton_for_saxon.xsl`
3. Output: cached `.xsl`
4. Executed against XML using Saxon HE
5. Output: **SVRL XML**

The ISO pipeline is **mandatory** — raw `.sch` files are never executed directly.

---

## Java Runtime

Schematron execution requires Java:

```
assets/java/
├── Saxon-HE-12.4.jar
└── xmlresolver-4.6.4.jar
```

Runtime classpath:
```
java -cp Saxon-HE.jar:xmlresolver.jar net.sf.saxon.Transform
```

---

## Compilation Cache

Compiled Schematron stylesheets are cached to avoid recompilation:

```
assets/schematron-cache/
├── <sha256>.xsl      # compiled stylesheets
└── svrl-<hash>.xml   # temporary SVRL results
```

Cache key:
- SHA256 of source `.sch` file contents

This guarantees:
- Deterministic reuse
- Safe invalidation on artefact change

---

## SVRL Parsing

SVRL output is parsed with `lxml`:

- `failed-assert` → error
- `successful-report` → warning (optional)

Extracted fields:
- rule id
- message text
- XPath location
- profile + schematron id

---

## Profile Integration

Schematron selection is driven by **profiles**:

```python
"schematron": {
  "chain": [
    "en16931",
    "hr-cius"
  ]
}
```

Each profile defines:
- Schematron ID
- Entry `.sch` file
- Execution order
- Suppression policy (future)

---

## HR-CIUS Specific Rules

Per official guidance:

- EN16931 **must always run first**
- HR-CIUS Schematron runs **after**
- HR-CIUS `.sch` already includes EN16931 code list includes
- HR-CIUS code-only Schematrons are **not executed directly**

This behavior is enforced by configuration, not code branching.

---

## Error Semantics

Schematron errors represent **business-rule violations**, not schema errors.

Examples:
- forbidden UBL elements
- missing mandatory semantic fields
- invalid national extensions

Errors are authoritative.

---

## Extensibility

Adding a new Schematron profile requires:

1. Drop artefacts under `assets/schematron/<profile-id>`
2. Add profile entry in `profiles.py`
3. No code changes required

---

## Status

✔ Stable  
✔ Deterministic  
✔ Cache-safe  
✔ Standards-compliant  

**Frozen as of v0.3.1**
