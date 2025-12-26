
# Validator Architecture

**Project:** `eracun_validator`  
**Scope:** XML validation engine (XSD + Schematron)  
**Version:** v0.3.1 (frozen)

---

## 1. Overview

The validator is responsible for validating **UBL 2.1 XML documents** (Invoice, CreditNote, etc.) against:

1. **XML Schema (XSD)** — structural validation  
2. **Schematron** — semantic and business rule validation

Validation behavior is driven by **profiles**, which represent *standards or local implementations* (e.g. EN16931, HR-CIUS), not by document types themselves.

The validator is:
- Profile-driven
- Asset-based (no embedded schemas)
- Deterministic (ordered validation steps)
- Extensible (future profiles via configuration)

---

## 2. High-Level Validation Flow

```
Input (file path or XML string)
        ↓
XML well-formedness check
        ↓
Profile detection
  (CustomizationID + namespaces)
        ↓
Document type detection
  (Invoice, CreditNote, …)
        ↓
XSD validation
        ↓
Schematron validation
  (only if XSD passes)
        ↓
Structured ValidationResult
```

---

## 3. Validator Package Structure

```
eracun_validator/
└── validator/
    ├── __init__.py
    ├── cli.py
    ├── core.py
    ├── profiles.py
    ├── result.py
    ├── xsd.py
    └── schematron.py
```

---

## 4. Core Components

### 4.1 `core.py` — Validation Orchestrator

**Responsibilities**
- Entry point for validation
- Controls validation order
- Coordinates profile detection, XSD and Schematron layers
- Owns validator lifecycle

**Key characteristics**
- Enforces **XSD → Schematron** order
- Schematron skipped if XSD fails
- Stateless per validation run

---

### 4.2 `profiles.py` — Profile Detection & Configuration

**Responsibilities**
- Detect validation profile from XML
- Central registry of profile configurations

Profiles define:
- CustomizationID
- Required namespaces
- XSD configuration
- Schematron configuration
- Validation order

Profiles represent **standards**, not documents.

---

### 4.3 `xsd.py` — XML Schema Validation

**Responsibilities**
- Resolve correct main XSD based on profile and document type
- Execute XSD validation
- Report structural errors

Key features:
- Config-driven paths
- Schema caching
- Hard-fail on structural errors

---

### 4.4 `schematron.py` — Schematron Engine

**Responsibilities**
- Compile Schematron → XSLT
- Cache compiled XSLT
- Execute XSLT
- Parse SVRL output

Key points:
- Saxon-HE execution
- xmlresolver support
- EN16931 runs before HR-CIUS
- Cache for performance

---

### 4.5 `result.py` — ValidationResult Model

Captures:
- Source XML
- Profile
- Document type
- Validation stack
- Errors and warnings
- Timestamps

Machine-readable and audit-friendly.

---

### 4.6 `cli.py` — CLI Interface

```
python -m eracun_validator validate <xml>
```

Delegates execution to `core.Validator`.

---

## 5. Asset Dependency Model

Validator depends on prepared assets:

```
assets/
├── xsd/
├── schematron/
├── java/
└── schematron-cache/
```

No schemas are embedded in code.

---

## 6. Design Principles

- Configuration over conditionals
- Profiles are data
- Explicit validation order
- Standards first, extensions later
- Fail fast on structure
- Asset builder isolated from validator

---

## 7. Version Freeze

This document describes **validator v0.3.1**.
