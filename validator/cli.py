# eracun_validator/validator/cli.py
import argparse
import os

from .core import Validator
from .result import write_json


def register_validate(subparsers):
    p = subparsers.add_parser(
        "validate",
        aliases=["v"],
        help="Validate XML invoice",
    )

    p.add_argument("xml", help="XML document")
    p.add_argument(
        "--assets",
        default=None,
        help="Assets root (defaults from config)",
    )
    p.add_argument(
        "--profile-only",
        action="store_true",
        help="Only detect profile, skip validation",
    )

    p.set_defaults(func=run_validate)


def run_validate(args: argparse.Namespace) -> int:
    assets_root = None
    if args.assets:
        assets_root = os.path.abspath(args.assets)
        if not os.path.isdir(assets_root):
            print(f"assets root '{args.assets}' is not a directory")
            return 1

    validator = Validator(assets_root=assets_root)
    profile, doc_type = validator.detect(args.xml)

    print(f"profile: {profile.id} doc_type: {doc_type}")

    if args.profile_only:
        return 0

    result = validator.validate(args.xml)
    print(write_json(result))

    return 0
