# eracun_validator/__main__.py

import argparse
import sys

from .validator.cli import main as validate_main
from .config import DEFAULT_ASSETS_ROOT

def build_parser():
    parser = argparse.ArgumentParser(
        prog="eracun-validator",
        description="UBL invoice validator (EN 16931 / HR CIUS)",
    )

    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    # -------------------------------------------------
    # validate command
    # -------------------------------------------------
    validate = subparsers.add_parser(
        "validate",
        help="Validate an invoice XML file",
    )

    validate.add_argument(
        "xml",
        help="Path to UBL Invoice or CreditNote XML",
    )

    validate.add_argument(
        "--assets",
        default=DEFAULT_ASSETS_ROOT,
        help="Path to validator assets directory",
    )

    validate.add_argument(
        "--profile-only",
        action="store_true",
        help="Detect profile and exit without validation",
    )

    # IMPORTANT: main(args) — args already parsed
    validate.set_defaults(func=lambda a: validate_main(a))

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        args.func(args)
    except AttributeError:
        parser.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main()
