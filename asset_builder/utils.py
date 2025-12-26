import os
import zipfile
import logging
import shutil
import tempfile

log = logging.getLogger(__name__)

def ensure_dir(path):
    if path and not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def extract_zip(
    zip_path,
    target_dir,
    *,
    include_ext=None,
    exclude_top_dirs=None,
    flatten=True,
):
    exclude_top_dirs = exclude_top_dirs or set()
    extracted = 0
    skipped = 0

    log.info("Extracting zip '%s' -> '%s'", os.path.basename(zip_path), target_dir)
    ensure_dir(target_dir)

    with zipfile.ZipFile(zip_path, "r") as zf:
        for info in zf.infolist():
            if info.is_dir():
                skipped += 1
                continue

            name = info.filename
            parts = name.split("/")
            if parts and parts[0].lower() in exclude_top_dirs:
                skipped += 1
                continue

            _, ext = os.path.splitext(name.lower())

            if ext == ".zip":
                log.info("Found nested zip: %s", name)
                with tempfile.TemporaryDirectory() as tmpdir:
                    nested_zip = os.path.join(tmpdir, os.path.basename(name))
                    with zf.open(info) as src, open(nested_zip, "wb") as dst:
                        shutil.copyfileobj(src, dst)
                    extract_zip(
                        nested_zip,
                        target_dir,
                        include_ext=include_ext,
                        exclude_top_dirs=exclude_top_dirs,
                        flatten=flatten,
                    )
                continue

            if include_ext and ext not in include_ext:
                skipped += 1
                continue

            out_path = (
                os.path.join(target_dir, os.path.basename(name))
                if flatten
                else os.path.join(target_dir, name)
            )
            ensure_dir(os.path.dirname(out_path))
            with zf.open(info) as src, open(out_path, "wb") as dst:
                shutil.copyfileobj(src, dst)
            extracted += 1

    log.info("Extraction complete: %d files extracted, %d skipped", extracted, skipped)
