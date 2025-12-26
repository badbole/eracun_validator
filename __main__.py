# eracun_validator/__main__.py

import argparse
import os
import sys

from eracun_validator.validator.cli import main as validate_main


# ----------------------------------------------------------------------
# Top-level CLI
# ----------------------------------------------------------------------

def build_parser():
    parser = argparse.ArgumentParser(
        prog="eracun-validator",
        description="UBL eInvoice validator (EN 16931 / HR CIUS)",
    )

    parser.add_argument(
        "--assets",
        help="Root directory containing XSD and Schematron assets",
        default=None,
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    # ------------------------------------------------------------------
    # validate
    # ------------------------------------------------------------------
    validate = subparsers.add_parser(
        "validate",
        help="Validate an invoice or credit note",
    )

    validate.add_argument(
        "xml",
        help="UBL XML file to validate",
    )

    validate.add_argument(
        "--profile-only",
        action="store_true",
        help="Only detect and print profile (no validation)",
    )

    validate.set_defaults(func=validate_main)

    return parser


# ----------------------------------------------------------------------
# Command handlers
# ----------------------------------------------------------------------

# def run_validate(args):
#     # Resolve assets root
#     assets_root = (
#         os.path.abspath(args.assets)
#         if args.assets
#         else _default_assets_root()
#     )
#
#     if not os.path.isdir(assets_root):
#         print(f"ERROR: assets root not found: {assets_root}", file=sys.stderr)
#         sys.exit(2)
#
#     # Delegate to validator CLI
#     validate_main(
#         xml_path=args.xml,
#         assets_root=assets_root,
#         profile_only=args.profile_only,
#     )


def _default_assets_root():
    """
    Default assets path relative to installed package.
    """
    here = os.path.dirname(__file__)
    return os.path.join(here, "assets")


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\nInterrupted")
        sys.exit(130)


if __name__ == "__main__":
    main()
