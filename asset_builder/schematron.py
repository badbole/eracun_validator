# asset_builder/schematron.py

import os
import shutil
import logging

from .base import BaseDownloader
from . import config
from .utils import ensure_dir, extract_zip

logger = logging.getLogger(__name__)


class SchematronDownloader(BaseDownloader):
    group_name = "schematron"

    def run(self):
        for name, cfg in config.SCHEMATRON.items():
            zip_path = self.download_zip_group(name=name, cfg=cfg)

            target_dir = os.path.join(
                self.assets_root,
                self.group_name,
                name,
            )
            ensure_dir(target_dir)

            # ISO schematron → take only XSL
            if name == "iso":
                include_ext = {".xsl"}
                extract_zip(
                    zip_path,
                    target_dir,
                    include_ext=include_ext,
                    flatten=False,
                )
                logger.info("ISO schematron extracted (XSL only): %s", target_dir)
                continue

            # EN16931 special handling (fallback ZIP layout)
            if name == "en16931":
                extract_zip(
                    zip_path,
                    target_dir,
                    include_ext=None,
                    flatten=False,
                )
                self._use_schematron_subdir(target_dir)
                self._unwrap_single_root_dir(target_dir)
                logger.info("EN16931 schematron prepared: %s", target_dir)
                continue

            # Default CIUS / localisation handling
            extract_zip(
                zip_path,
                target_dir,
                include_ext={".sch"},
                flatten=False,
            )
            self._unwrap_single_root_dir(target_dir)
            logger.info("Schematron extracted: %s", target_dir)

    def _use_schematron_subdir(self, target_dir):
        """
        EN16931 fallback ZIPs contain `schematron/`, `xslt/`, `examples/`.
        Use only `schematron/` and move its contents to target root.
        """
        schematron_dir = os.path.join(target_dir, "schematron")
        if not os.path.isdir(schematron_dir):
            return

        for item in os.listdir(schematron_dir):
            src = os.path.join(schematron_dir, item)
            dst = os.path.join(target_dir, item)
            if os.path.exists(dst):
                continue
            shutil.move(src, dst)

        shutil.rmtree(schematron_dir, ignore_errors=True)

        # remove known irrelevant folders if present
        for name in ("xslt", "examples"):
            path = os.path.join(target_dir, name)
            if os.path.isdir(path):
                shutil.rmtree(path, ignore_errors=True)

    def _unwrap_single_root_dir(self, target_dir):
        """
        If files are wrapped in a single top-level directory
        (common for CIUS packages), unwrap it so the main .sch
        file is placed directly in target_dir.
        """
        try:
            entries = os.listdir(target_dir)
        except FileNotFoundError:
            return

        if len(entries) != 1:
            return

        root = os.path.join(target_dir, entries[0])
        if not os.path.isdir(root):
            return

        logger.info(
            "Unwrapping single root directory for schematron: %s",
            root,
        )

        for item in os.listdir(root):
            src = os.path.join(root, item)
            dst = os.path.join(target_dir, item)
            if os.path.exists(dst):
                continue
            shutil.move(src, dst)

        shutil.rmtree(root, ignore_errors=True)
