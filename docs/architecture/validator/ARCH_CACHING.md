# Caching Architecture — eracun_validator (v0.3.1)

## Purpose

The caching subsystem ensures that validation is:

- **Fast** (no repeated compilation / parsing)
- **Deterministic** (same input → same execution plan)
- **Offline** (no network resolution)
- **Safe** (automatic invalidation on asset change)

Caching exists at multiple levels and is **transparent** to the caller.

---

## Cache Layers Overview

| Layer | Cached Object | Scope |
|-----|---------------|-------|
| XSD | XMLSchema objects | Python process |
| Schematron | Compiled XSLT | File system |
| Schematron | SVRL output | Temporary / per-run |

---

## XSD Cache

### What is cached

- `lxml.etree.XMLSchema` objects
- Keyed by **absolute XSD file path**

### Location

- In-memory (`dict`) inside `XsdValidator`

### Behavior

- Parsed once per XSD file
- Reused across documents
- Automatically cleared when process exits

### Guarantees

- No recompilation
- No disk writes
- No external entity resolution

---

## Schematron Compilation Cache

### What is cached

- Compiled Schematron XSLT (`.xsl`)

### Location

```
assets/schematron-cache/
└── <sha256>.xsl
```

### Cache Key

- SHA256 hash of:
  - Source `.sch` file contents

This guarantees:
- Cache invalidation on *any* file change
- Independence from file name or timestamp

---

## Schematron Execution Cache

### What is cached

- SVRL XML output (per validation run)

### Location

```
assets/schematron-cache/
└── svrl-<hash>.xml
```

### Lifecycle

- Created per execution
- Parsed immediately
- Deleted or overwritten on next run

SVRL files are never reused across runs.

---

## Java Runtime Considerations

- JVM startup cost dominates Schematron execution
- Caching compiled XSLT avoids ISO pipeline cost
- Runtime classpath is constant and deterministic

No JVM reuse is attempted in v0.3.1 by design.

---

## Failure Isolation

Caching does **not** cache failures:

- Invalid `.sch` → compilation fails → no cache written
- Invalid `.xsl` → execution fails → cache untouched

This prevents poisoning the cache.

---

## Concurrency Safety

Assumptions for v0.3.1:

- Single-process execution
- No concurrent writers to cache directory

Safe for:
- CLI usage
- CI pipelines
- Sequential batch validation

Future locking strategies can be added if needed.

---

## Determinism Guarantees

Given:
- Same assets
- Same input XML
- Same validator version

Caching guarantees:
- Same XSD resolution
- Same Schematron chain
- Same compiled artefacts

This is critical for compliance validation.

---

## Non-Goals

Caching deliberately avoids:
- Network fetching
- Automatic eviction
- Cross-version reuse
- Persistent runtime caches

Simplicity > cleverness.

---

## Extensibility

Future improvements may include:
- JVM process pooling
- Cross-run SVRL reuse (read-only)
- Cache eviction policies
- Parallel-safe locking

None are enabled in v0.3.1.

---

## Status

✔ Stable  
✔ Deterministic  
✔ Offline  
✔ Predictable  

**Frozen as of v0.3.1**
