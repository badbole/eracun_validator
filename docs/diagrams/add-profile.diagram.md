
# How to Add a New Validation Profile (Diagram-first)

## 1. Conceptual placement

```
assets/
 ├─ xsd/<profile>/<syntax>/{common,maindoc}
 ├─ schematron/<profile>/
validator/
 ├─ profiles.py   <- register profile config
 ├─ core.py       <- no change
```

## 2. Steps

1. Add XSD assets
2. Add Schematron assets
3. Register profile dictionary
4. (Optional) add policy overrides

## 3. Minimal profile config

```python
PROFILE = {
  "id": "example-cius",
  "customization_id": "...",
  "xsd": {
    "root": "xsd/example/ubl/maindoc"
  },
  "schematron": {
    "en16931": {...},
    "example-cius": {...}
  }
}
```
