import os
from .xsd import XsdValidator
from .schematron import SchematronValidator
from .profiles import detect_document_type, detect_profile
from .result import ValidationResult


class Validator:
    def __init__(self, xsd_validator, schematron_validator):
        self.xsd_validator = xsd_validator
        self.schematron_validator = schematron_validator

    def validate(self, xml_path, profile):
        """
        Validate XML against resolved profile:
        1. XSD
        2. Schematron stages (in order)
        """
        result = ValidationResult()

        # -------------------------------------------------
        # 1. XSD validation
        # -------------------------------------------------
        xsd_info = profile.get("xsd")
        if xsd_info:
            self.xsd_validator.validate(
                xml_path=xml_path,
                xsd_root=xsd_info["path"],
                result=result,
            )

            # If XSD failed, schematron must NOT run
            if result.has_errors():
                return result

        # -------------------------------------------------
        # 2. Schematron validation
        # -------------------------------------------------
        sch_info = profile.get("schematron")
        if sch_info:
            schematron_list = []

            for stage in sch_info.get("stages", []):
                schematron_list.append({
                    "id": stage["id"],
                    "path": os.path.join(stage["path"], stage["main"]),
                })

            self.schematron_validator.validate(
                xml_path,
                schematron_list,
                result,
            )

        return result

    def _resolve_schematrons(self, stack):
        resolved = []

        for entry in stack:
            if not entry.startswith("schematron:"):
                continue

            sid = entry.split(":", 1)[1]
            sch_path = os.path.join(
                self.assets_root,
                "schematron",
                sid,
                self._main_schematron_file(sid),
            )

            resolved.append({
                "id": sid,
                "path": sch_path,
            })

        return resolved

    def _main_schematron_file(self, sid):
        if sid == "en16931":
            return "EN16931-UBL-validation.sch"
        if sid == "hr-cius":
            return "HR-CIUS-EXT-EN16931-UBL.sch"
        raise ValueError(f"Unknown schematron id: {sid}")
