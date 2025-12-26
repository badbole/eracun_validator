import sys

from .core import Validator
from .xsd import XsdValidator
from .schematron import SchematronValidator
from .profiles import detect_profile, resolve_profile
from ..config import DEFAULT_ASSETS_ROOT


def main(args):
    assets_root = args.assets or DEFAULT_ASSETS_ROOT
    # -------------------------------------------------
    # Detect & resolve profile
    # -------------------------------------------------
    try:
        detected = detect_profile(args.xml)
        profile = resolve_profile(detected, assets_root)
    except Exception as e:
        print("ERROR: Failed to detect validation profile.")
        print(str(e))
        return 2

    if args.profile_only:
        print("Detected profile:")
        print(f"  ID:    {profile['id']}")
        print(f"  Label: {profile.get('label', '')}")
        return 0

    # -------------------------------------------------
    # Run validation
    # -------------------------------------------------
    # core = Validator(
    #     xml_path=args.xml,
    #     profile=profile,
    # )
    #
    # result = core.validate()

    if getattr(args, "profile_only", False):
        print(f"{profile['id']} – {profile.get('label', '')}")
        return 0

        # --- build validators ---
    xsd_validator = XsdValidator(assets_root)
    schematron_validator = SchematronValidator(assets_root)

    core = Validator(
        xsd_validator=xsd_validator,
        schematron_validator=schematron_validator,
    )

    # --- execute validation ---
    result = core.validate(
        xml_path=args.xml,
        profile=profile,
    )

    # -------------------------------------------------
    # Output
    # -------------------------------------------------
    print(result.render())

    return 1 if result.has_errors() else 0
