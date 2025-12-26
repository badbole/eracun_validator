import os
from .xsd import XsdValidator
from .schematron import SchematronValidator
from .profiles import detect_document_type, detect_profile
from .result import ValidationResult


class Validator:
    def __init__(self, assets_root):
        self.assets_root = assets_root
        self.xsd_validator = XsdValidator(assets_root)
        self.schematron_validator = SchematronValidator(assets_root)

    def validate(self, xml_path):
        document_type = detect_document_type(xml_path)
        profile = detect_profile(xml_path)

        result = ValidationResult(
            xml_file=xml_path,
            profile=profile["id"],
            document_type=document_type,
            stack=profile["validation_stack"],
        )

        # 1. XSD validation
        xsd_ok = self.xsd_validator.validate(
            xml_path=xml_path,
            profile=profile,
            document_type=document_type,
            result=result,
        )

        # 2. Schematron only if XSD passed
        if xsd_ok:
            schematrons = self._resolve_schematrons(profile["validation_stack"])
            self.schematron_validator.validate(
                xml_path=xml_path,
                schematrons=schematrons,
                result=result,
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
