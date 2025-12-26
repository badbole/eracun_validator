# XSD Architecture — eracun_validator (v0.3.1)

## Purpose

The XSD subsystem enforces **structural and syntactic correctness**
of UBL-based XML documents.

It guarantees that:
- XML is well-formed
- Document root matches a known UBL document type
- Namespace usage is correct
- All mandatory structural elements exist

XSD validation is **always executed first** and is a hard gate:
if XSD validation fails, **Schematron validation is skipped**.

---

## Validation Flow

1. Input received (file path or XML string)
2. XML parsed and namespace validated
3. Document root detected (Invoice, CreditNote, …)
4. Validation profile selected
5. Main document XSD resolved from profile
6. XML validated against XSD set

---

## Asset Layout

```
assets/xsd/
├── ubl-2.1/
│   ├── xsd/
│   │   ├── maindoc/
│   │   │   ├── UBL-Invoice-2.1.xsd
│   │   │   └── UBL-CreditNote-2.1.xsd
│   │   └── common/
│   │       ├── UBL-CommonAggregateComponents-2.1.xsd
│   │       └── ...
│
└── hr-cius/
    └── ubl/
        ├── maindoc/
        │   ├── UBL-Invoice-2.1.xsd
        │   └── UBL-CreditNote-2.1.xsd
        └── common/
            ├── HRExtensionAggregateComponents-1.xsd
            └── ...
```

Each profile defines **its own maindoc root**, enabling extensions
without duplicating validator logic.

---

## Profile-Driven Resolution

Profiles define XSD roots using relative paths:

```python
"xsd": {
  "root": "xsd/hr-cius/ubl/maindoc",
  "fallback": "xsd/ubl-2.1/xsd/maindoc"
}
```

Resolution logic:
- Prefer profile-specific XSD
- Fallback to base UBL if missing
- Auto-detect document type by filename prefix

---

## Document Auto-Detection

The validator:
- Scans `maindoc/`
- Matches root element name to XSD filename
- Supports multiple document types per profile

This enables:
- Invoice
- CreditNote
- Future documents (Order, DebitNote, etc.)

No document-specific logic exists in code.

---

## XML Parsing & Validation

Implementation uses **lxml.etree.XMLSchema**:

- Schema objects are cached per XSD file
- External entity loading is disabled
- Resolution relies on local relative includes only

Caching guarantees:
- Performance
- Deterministic behavior
- No network access

---

## Error Semantics

XSD errors indicate **structural invalidity**:

Examples:
- Missing mandatory element
- Invalid namespace
- Wrong document root
- Incorrect data type

XSD errors are **blocking** and always fatal.

---

## Separation of Concerns

| Layer | Responsibility |
|------|---------------|
| XSD  | Structure + syntax |
| Schematron | Business rules |
| Policy (future) | Rule overrides |

XSD never inspects semantic constraints.

---

## Extensibility

Adding a new structure profile requires:
1. Adding XSD files under `assets/xsd/<profile>`
2. Defining XSD root in profile config
3. No code changes required

---

## Status

✔ Stable  
✔ Cached  
✔ Offline  
✔ Profile-driven  

**Frozen as of v0.3.1**
