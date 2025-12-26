import argparse
from .validator.cli import main as validate_main


def run_validate():
    parser = argparse.ArgumentParser("eracun-validator")

    sub = parser.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("validate", help="Validate XML invoice")
    v.add_argument("xml", help="XML document")
    v.add_argument(
        "--assets",
        default=None,
        help="Assets root (defaults from config)",
    )
    v.add_argument(
        "--profile-only",
        action="store_true",
        help="Only detect profile, skip validation",
    )

    args = parser.parse_args()
    return validate_main(args)


if __name__ == "__main__":
    raise SystemExit(run_validate())
