import sys
from .core import Validator
from .profiles import detect_profile, resolve_profile


def main(args):
    try:
        # 1. Detect profile
        profile = detect_profile(args.xml)

        # 2. Resolve profile with assets_root (MUST be string)
        profile = resolve_profile(profile, args.assets)

    except Exception as e:
        print("ERROR: Failed to detect validation profile.")
        print(str(e))
        return 2

    # Profile-only short circuit
    if getattr(args, "profile_only", False):
        print(f"Profile: {profile['id']} — {profile.get('label', '')}")
        return 0

    # 3. Build validator (no xml_path here)
    core = Validator(
        assets_root=args.assets
    )

    # 4. Execute validation
    result = core.validate(
        xml_path=args.xml,
        profile=profile,
    )

    # 5. Output
    print(result.render())

    return 0 if not result.has_errors() else 1
