# eracun_validator/__main__.py

import argparse
import sys

from eracun_validator.asset_builder.cli import main as build_main
from eracun_validator.validator.cli import main as validate_main


def main():
    parser = argparse.ArgumentParser(
        prog="eracun-validator",
        description="eRacun validation toolkit (assets + validation)",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # build command
    build = sub.add_parser(
        "build",
        help="Download and prepare validation assets",
    )
    build.set_defaults(func=lambda a: build_main(a))

    # validate command
    validate = sub.add_parser(
        "validate",
        help="Validate XML invoice or credit note",
    )
    validate.add_argument(
        "args",
        nargs=argparse.REMAINDER,
        help="Arguments forwarded to validator",
    )
    validate.set_defaults(func=lambda a: validate_main(a.args))

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
