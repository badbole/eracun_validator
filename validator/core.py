# eracun_validator/validator/core.py

from .profiles import detect_document_type
from .result import ValidationResult


class Validator:
    def __init__(self, profile, assets_root, profile_only=False):
        self.profile = profile
        self.assets_root = assets_root
        self.profile_only = profile_only

        self.schematron = SchematronValidator(assets_root)
        self.xsd = XsdValidator(assets_root)

    # -------------------------------------------------
    # Public API
    # -------------------------------------------------

    def validate(self, xml_path, profile):
        """
        Execute validation according to resolved profile.

        Returns:
            ValidationResult
        """
        document_type = detect_document_type(xml_path)

        # -------------------------------------------------
        # Build validation stack (for reporting only)
        # -------------------------------------------------
        stack = []

        if "xsd" in profile:
            stack.append("xsd")

        if "schematron" in profile:
            for stage in profile["schematron"]["stages"]:
                stack.append(stage["id"])

        # -------------------------------------------------
        # Initialize result
        # -------------------------------------------------
        result = ValidationResult(
            xml_file=xml_path,
            profile=profile["id"],
            document_type=document_type,
            stack=stack,
        )

        # -------------------------------------------------
        # XSD validation (always first)
        # -------------------------------------------------
        if "xsd" in profile:
            ok = self.xsd_validator.validate(
                xml_path,
                profile,
                document_type,
                result,
            )

            # If XSD fails → no Schematron
            if not ok:
                return result

        # -------------------------------------------------
        # Schematron validation
        # -------------------------------------------------
        if "schematron" in profile:
            self.schematron_validator.validate(
                xml_path,
                profile,
                result,
            )

        return result
