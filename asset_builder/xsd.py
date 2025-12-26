import os
from .base import BaseDownloader
from . import config
from .utils import ensure_dir, extract_zip

class XsdDownloader(BaseDownloader):
    group_name = "xsd"

    def run(self):
        for name, cfg in config.XSD.items():
            zip_path = self.download_zip_group(name=name, cfg=cfg)
            target_dir = os.path.join(self.assets_root, self.group_name, name)
            ensure_dir(target_dir)
            extract_zip(zip_path, target_dir, include_ext={".xsd"}, flatten=False)
