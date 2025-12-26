# asset_builder/samples.py

import os
import zipfile
import logging

from .utils import ensure_dir
from . import config

logger = logging.getLogger(__name__)


class SampleDownloader:
    def __init__(self, downloads_root, assets_root):
        self.downloads_root = downloads_root
        self.assets_root = assets_root

    def run(self):
        self._build_ubl21_samples()
        self._build_hr_cius_samples()

    # ------------------------------------------------------------------
    # UBL 2.1 samples (from UBL2.1.zip, reused from XSD source)
    # ------------------------------------------------------------------

    def _build_ubl21_samples(self):
        zip_name = config.XSD["ubl-2.1"]["filename"]
        zip_path = os.path.join(self.downloads_root, zip_name)
        if not os.path.isfile(zip_path):
            logger.warning("UBL2.1.zip not found, skipping UBL samples")
            return

        target_dir = os.path.join(self.assets_root, "samples", "ubl2.1")
        ensure_dir(target_dir)

        with zipfile.ZipFile(zip_path, "r") as zf:
            for member in zf.namelist():
                lname = member.lower()

                if not lname.endswith(".xml"):
                    continue
                if "/xml/" not in lname and not lname.startswith("xml/"):
                    continue

                fname = os.path.basename(member).lower()
                if "invoice" not in fname and "credit" not in fname:
                    continue

                target = os.path.join(target_dir, os.path.basename(member))
                if os.path.exists(target):
                    continue

                with zf.open(member) as src, open(target, "wb") as dst:
                    dst.write(src.read())

        logger.info("UBL 2.1 samples prepared: %s", target_dir)

    # ------------------------------------------------------------------
    # HR-CIUS samples (from official examples ZIP)
    # ------------------------------------------------------------------

    def _build_hr_cius_samples(self):
        cfg = getattr(config, "SAMPLES", {}).get("hr-cius")
        if not cfg:
            logger.warning("HR-CIUS samples config missing, skipping")
            return

        zip_path = os.path.join(self.downloads_root, cfg["filename"])
        if not os.path.isfile(zip_path):
            logger.warning("HR-CIUS samples ZIP not found, skipping")
            return

        target_dir = os.path.join(self.assets_root, "samples", "hr-cius")
        ensure_dir(target_dir)

        with zipfile.ZipFile(zip_path, "r") as zf:
            for member in zf.namelist():
                lname = member.lower()

                if not lname.endswith(".xml"):
                    continue

                fname = os.path.basename(member).lower()
                if "invoice" not in fname and "credit" not in fname:
                    continue

                target = os.path.join(target_dir, os.path.basename(member))
                if os.path.exists(target):
                    continue

                with zf.open(member) as src, open(target, "wb") as dst:
                    dst.write(src.read())

        logger.info("HR-CIUS samples prepared: %s", target_dir)
