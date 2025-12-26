# eracun_validator/validator/cli.py

import argparse
import os
import sys

from .core import Validator


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="eracun-validator validate",
        description="Validate UBL / EN16931 / CIUS e-Invoice XML documents",
    )

    parser.add_argument(
        "source",
        help="XML file path or raw XML string",
    )

    parser.add_argument(
        "--assets",
        default=os.path.join(
            os.path.dirname(__file__),
            "..",
            "assets",
        ),
        help="Assets root directory (default: eracun_validator/assets)",
    )

    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format (default: text)",
    )

    parser.add_argument(
        "--print-stack",
        action="store_true",
        help="Print applied validation stack",
    )

    args = parser.parse_args(argv)

    validator = Validator(args.assets)
    result = validator.validate(args.source)

    if args.print_stack:
        print("Validation stack:")
        for step in result.validation_stack:
            print(f" - {step}")

    if args.format == "json":
        print(result.to_json())
    else:
        _print_text(result)

    return 1 if result.has_errors() else 0


# -------------------------------------------------


def _print_text(result):
    if not result.has_errors():
        print("Validation OK")
        return

    for err in result.errors:
        loc = f" ({err.get('location')})" if err.get("location") else ""
        src = f" [{err.get('source')}]" if err.get("source") else ""
        print(f"ERROR: {err.get('message')}{loc}{src}", file=sys.stderr)

    for warn in result.warnings:
        loc = f" ({warn.get('location')})" if warn.get("location") else ""
        src = f" [{warn.get('source')}]" if warn.get("source") else ""
        print(f"WARNING: {warn.get('message')}{loc}{src}")
