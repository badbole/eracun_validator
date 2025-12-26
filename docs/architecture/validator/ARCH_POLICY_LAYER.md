# Policy Layer Architecture — eracun_validator (v0.3.1)

## Purpose

The **policy layer** governs how validation findings are
**interpreted, filtered, overridden, or escalated** after raw validation.

It does **not** change:
- XSD schemas
- Schematron rules
- Validation execution order

Instead, it operates **on validation results**, applying jurisdictional
or organizational policies.

---

## Position in Validation Stack

```
XML
 ├─ XSD validation
 ├─ Schematron validation
 └─ Policy layer   ← HERE
     └─ Final result
```

The policy layer is the **last step** before results are returned.

---

## Why Policy Is Needed

Real-world regulations require flexibility:

- National CIUS overrides EN16931 rules
- Some rules are informational, not fatal
- Transitional rules may be conditionally ignored
- Authorities may reclassify rule severities

Embedding this logic in Schematron would:
- Fork standards
- Break upgrades
- Destroy traceability

Therefore, policy is applied **after validation**.

---

## Responsibilities

The policy layer can:

- Suppress specific rule IDs
- Downgrade errors → warnings
- Upgrade warnings → errors
- Apply conditional logic (per profile, version, date)
- Annotate results with explanations

The policy layer **never invents new violations**.

---

## Input & Output

### Input
- `ValidationResult`
- Profile configuration
- Optional policy configuration

### Output
- Modified `ValidationResult`
- Same structure, different interpretation

---

## Policy Configuration Model

Policies are pure data:

```python
POLICIES = {
  "hr-cius": {
    "suppress": [
      "UBL-CR-001",
      "UBL-CR-006"
    ],
    "downgrade": {
      "UBL-CR-200": "warning"
    },
    "notes": {
      "UBL-CR-001": "Allowed by HR fiscal extension"
    }
  }
}
```

Policies are:
- Profile-scoped
- Explicit
- Versionable

---

## Resolution Order

1. Identify active profile
2. Load matching policy block
3. Apply suppressions
4. Apply severity changes
5. Attach explanatory notes

Resolution is deterministic.

---

## Rule Identity

Policies match rules using:
- Schematron rule ID
- Optional XPath context
- Optional document type

No heuristic matching is allowed.

---

## HR-CIUS Example

Official guidance states:
- EN16931 rules must run first
- HR-CIUS may legally override them

Policy layer implementation:
- EN16931 violations remain detectable
- HR-CIUS policy suppresses incompatible rules
- Audit trail preserved

This satisfies both:
- EU compliance
- National law

---

## Audit & Traceability

Policy application must be auditable:

- Original rule ID preserved
- Original severity preserved
- Policy reason attached
- Suppressed rules optionally recorded

This is critical for compliance audits.

---

## Extensibility

Future extensions:
- Date-based policies
- Issuer-based policies
- Receiver-based policies
- Validation profiles per authority

All without changing validator core.

---

## Non-Goals

The policy layer will not:
- Modify Schematron artefacts
- Disable validators
- Mask structural errors
- Guess intent

Policy is explicit or not applied.

---

## Status

✔ Defined  
✔ Profile-scoped  
✔ Deterministic  
✔ Optional  

**Architecture frozen as of v0.3.1**
