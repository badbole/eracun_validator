# asset_builder/base.py

import os
import logging
import requests

from .utils import ensure_dir

log = logging.getLogger(__name__)


class BaseDownloader:
    group_name = None

    def __init__(self, assets_root, downloads_root):
        self.assets_root = assets_root
        self.downloads_root = downloads_root
        ensure_dir(self.downloads_root)

    def download_file(self, name, cfg):
        filename = cfg["filename"]
        url = cfg["url"]

        target_path = os.path.join(self.downloads_root, filename)
        if os.path.exists(target_path):
            log.info("Using cached file: %s", filename)
            return target_path

        log.info("Downloading file: %s", filename)
        self.download(url, target_path)
        return target_path

    def download_zip_group(self, name, cfg):
        filename = cfg["filename"]
        url = cfg["url"]

        target_path = os.path.join(self.downloads_root, filename)
        if os.path.exists(target_path):
            log.info("Using cached zip: %s", filename)
            return target_path

        log.info("Downloading zip: %s", filename)
        self.download(url, target_path)
        return target_path

    def download(self, url, target_path):
        """
        ORIGINAL uploaded helper – must exist.
        """
        ensure_dir(os.path.dirname(target_path))

        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(target_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
