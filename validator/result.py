# eracun_validator/validator/result.py

import json
from datetime import datetime


class ValidationResult:
    """
    Structured validation result with full context.
    """

    def __init__(self, xml_file, profile, document_type, stack):
        self.xml_file = xml_file
        self.profile = profile
        self.document_type = document_type
        self.validation_stack = stack
        self.started_at = datetime.utcnow().isoformat() + "Z"

        self.errors = []
        self.warnings = []

    # -------------------------------------------------

    def add_entries(self, entries):
        for e in entries or []:
            if e.get("level") == "error":
                self.errors.append(e)
            else:
                self.warnings.append(e)

    def has_errors(self):
        return bool(self.errors)

    # -------------------------------------------------

    def to_dict(self):
        return {
            "xml": self.xml_file,
            "profile": self.profile,
            "document_type": self.document_type,
            "validation_stack": self.validation_stack,
            "started_at": self.started_at,
            "summary": {
                "errors": len(self.errors),
                "warnings": len(self.warnings),
            },
            "errors": self.errors,
            "warnings": self.warnings,
            "generated_at": datetime.utcnow().isoformat() + "Z",
        }

    def to_json(self, indent=2):
        return json.dumps(self.to_dict(), indent=indent)
