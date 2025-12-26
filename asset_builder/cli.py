# asset_builder/cli.py

import logging

from .java import JavaDownloader
from .xsd import XsdDownloader
from .schematron import SchematronDownloader
from .samples import SampleDownloader

log = logging.getLogger(__name__)


def run(assets_root, downloads_root):
    JavaDownloader(assets_root, downloads_root).run()
    XsdDownloader(assets_root, downloads_root).run()
    SchematronDownloader(assets_root, downloads_root).run()
    SampleDownloader(assets_root, downloads_root).run()


def main(argv):
    """
    CLI entrypoint expected by eracun_validator.__main__.
    argv: list of CLI args (rest)
    """

    # Preserve uploaded defaults / behavior
    assets_root = "eracun_validator/assets"
    downloads_root = "eracun_validator/downloads"

    if argv:
        # allow overriding roots if upload supported it
        if len(argv) >= 1:
            assets_root = argv[0]
        if len(argv) >= 2:
            downloads_root = argv[1]

    log.info("Building assets")
    run(assets_root, downloads_root)
