# eracun_validator/validator/cli.py

import sys

from .core import Validator
from .xsd import XsdValidator
from .schematron import SchematronValidator
from .profiles import detect_profile, resolve_profile


def main(args):
    # -------------------------------------------------
    # Detect & resolve profile
    # -------------------------------------------------
    try:
        profile = detect_profile(args.xml)
        profile = resolve_profile(profile, args.assets)
    except Exception as e:
        print("ERROR: Failed to detect validation profile.")
        print(str(e))
        sys.exit(2)

    if getattr(args, "profile", False):
        print("Detected profile:")
        print(f"  ID:    {profile['id']}")
        print(f"  Label: {profile.get('label', '')}")
        sys.exit(0)

    # -------------------------------------------------
    # Inform user what will happen
    # -------------------------------------------------
    print("Validation profile detected:")
    print(f"  → {profile['label']} ({profile['id']})")

    if "xsd" in profile:
        print(f"  XSD root: {profile['xsd']['path']}")

    if "schematron" in profile:
        print("  Schematron stages:")
        for stage in profile["schematron"]["stages"]:
            print(f"    - {stage['id']}: {stage['main']}")

    print()

    # -------------------------------------------------
    # Build validators
    # -------------------------------------------------
    xsd_validator = XsdValidator(args.assets)
    schematron_validator = SchematronValidator(args.assets)

    validator = Validator(
        xsd_validator=xsd_validator,
        schematron_validator=schematron_validator,
    )

    # -------------------------------------------------
    # Execute validation
    # -------------------------------------------------
    result = validator.validate(
        xml_path=args.xml,
        profile=profile,
    )

    # -------------------------------------------------
    # Output result
    # -------------------------------------------------
    print(result.render())

    sys.exit(1 if result.has_errors() else 0)
