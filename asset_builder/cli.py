# # asset_builder/cli.py
#
# import logging
#
# from .java import JavaDownloader
# from .xsd import XsdDownloader
# from .schematron import SchematronDownloader
# from .samples import SampleDownloader
#
# log = logging.getLogger(__name__)
#
#
# def run(assets_root, downloads_root):
#     JavaDownloader(assets_root, downloads_root).run()
#     XsdDownloader(assets_root, downloads_root).run()
#     SchematronDownloader(assets_root, downloads_root).run()
#     SampleDownloader(assets_root, downloads_root).run()
#
#
# def main(argv):
#     """
#     CLI entrypoint expected by eracun_validator.__main__.
#     argv: list of CLI args (rest)
#     """
#
#     # Preserve uploaded defaults / behavior
#     assets_root = "eracun_validator/assets"
#     downloads_root = "eracun_validator/downloads"
#
#     if argv:
#         # allow overriding roots if upload supported it
#         if len(argv) >= 1:
#             assets_root = argv[0]
#         if len(argv) >= 2:
#             downloads_root = argv[1]
#
#     log.info("Building assets")
#     run(assets_root, downloads_root)
# eracun_validator/asset_builder/cli.py
import argparse

from .asset_builder import main as asset_builder_main


def register_build(subparsers):
    p = subparsers.add_parser(
        "build",
        aliases=["b"],
        help="Prepare assets from specs",
    )

    p.add_argument(
        "root",
        help="Destination root for built assets (schemas + schematron + java)",
    )
    p.add_argument(
        "--debug",
        action="store_true",
        help="Print debug logging for asset building",
    )

    p.set_defaults(func=run_build)


def run_build(args: argparse.Namespace) -> int:
    return asset_builder_main(args)
