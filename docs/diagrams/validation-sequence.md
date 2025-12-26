
# Validation Sequence Diagram

```
User
 │
 │ validate x.xml
 ▼
CLI
 │
 ▼
Validator.validate()
 │
 │ detect_profile()
 ▼
ProfileConfig
 │
 ├─► XSD.validate()
 │     ├─ load main doc XSD
 │     └─ stop on first error
 │
 └─► Schematron.validate()
       ├─ EN16931.sch
       ├─ CIUS.sch
       └─ Policy filtering
 │
 ▼
ValidationResult
 │
 ▼
Exit code / report
```

Notes:
- Schematron runs only if XSD passes
- HR-CIUS extends EN16931, never replaces it
- Cache reused across runs
