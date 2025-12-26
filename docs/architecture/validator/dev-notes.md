# eracun_validator – Developer Notes (v0.3.1)

## Purpose
This validator implements EN 16931 and HR-CIUS (Fiskalizacija 2.0) validation
for UBL 2.1 documents using XSD and Schematron.

The architecture is configuration-driven to support future profiles,
documents, and standards with minimal code change.

---

## Design Principles

- **Fail-fast**: XSD validation MUST pass before Schematron runs
- **Profile-driven**: Validation profiles describe structure, not documents
- **Config over code**: Paths, rules, and options live in profiles
- **Deterministic**: No auto-magic beyond file discovery in maindoc folders
- **Cache-aware**: Compiled Schematron XSLT is reused

---

## Validation Flow

1. Detect profile from XML (CustomizationID / namespace)
2. Load profile configuration
3. Resolve XSD maindoc directory
4. Validate XML via XSD
5. If XSD passes → run Schematron(s) in defined order
6. Aggregate results into ValidationResult

---

## Profiles

Profiles define:
- Standard code (EN16931, HR-CIUS, etc.)
- CustomizationID(s)
- XSD structure paths
- Schematron chain (ordered)

Profiles do NOT define documents explicitly.
Documents are discovered from the `maindoc/` folders.

---

## XSD Notes

- Only UBL 2.1 is currently supported
- HR-CIUS reuses UBL 2.1 schemas with CIUS-specific layout
- Each profile points to its own maindoc directory

---

## Schematron Notes

- Uses official CEN EN16931 schematron
- HR-CIUS schematron is executed AFTER EN16931
- Schematron is compiled once and cached as XSLT
- Execution uses Saxon-HE + xmlresolver

---

## Caching

- XSLT cache key = hash(schematron path + skeleton + options)
- SVRL is parsed immediately and then discarded
- Cache directory is safe to delete at any time

---

## Policy Layer

The policy layer can:
- Filter rules
- Downgrade errors → warnings
- Disable rules by ID
- Apply jurisdiction-specific behavior

Policy NEVER changes validation execution, only interpretation.

---

## Common Pitfalls

- Missing xmlresolver on Saxon classpath
- Using raw .sch without ISO skeleton compilation
- Mixing document logic into profile detection
- Running Schematron before XSD

---

## Versioning

v0.3.1 is a **frozen baseline**.
All future changes must be backward compatible or version-bumped.

---

## Recommended Next Extensions

- CreditNote support (auto via maindoc discovery)
- PEPPOL BIS profile
- JSON report output
- Parallel Schematron execution (opt-in)

