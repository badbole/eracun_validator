# asset_builder/java.py

import os
import shutil

from .base import BaseDownloader
from . import config
from .utils import ensure_dir


class JavaDownloader(BaseDownloader):
    group_name = "java"

    def run(self):
        target_dir = os.path.join(self.assets_root, self.group_name)
        ensure_dir(target_dir)

        for name, cfg in config.JAVA.items():
            jar_path = self.download_file(
                name=name,
                cfg=cfg,
            )

            target_path = os.path.join(target_dir, cfg["filename"])
            if not os.path.exists(target_path):
                shutil.copyfile(jar_path, target_path)
