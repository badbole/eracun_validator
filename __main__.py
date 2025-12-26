# eracun_validator/__main__.py
import argparse

from .validator.cli import register_validate
#from .asset_builder.cli import register_build


def run() -> int:
    parser = argparse.ArgumentParser("eracun-validator")

    subparsers = parser.add_subparsers(
        dest="cmd",
        required=True,
    )

    register_validate(subparsers)
 #   register_build(subparsers)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(run())
