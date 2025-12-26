# eracun_validator/validator/schematron.py

import os
import hashlib
import subprocess
from lxml import etree


class SchematronValidator:
    """
    Schematron validator using OFFICIAL driver XSL files
    provided by EN16931 / HR-CIUS distributions.

    IMPORTANT:
    - .sch files are NEVER compiled here
    - Driver .xsl files already:
        * include ISO skeleton
        * bind variables
        * activate correct phases
    """

    def __init__(self, assets_root):
        self.assets_root = assets_root

        self.saxon_jar = os.path.join(
            assets_root, "java", "Saxon-HE-12.4.jar"
        )
        self.xmlresolver_jar = os.path.join(
            assets_root, "java", "xmlresolver-4.6.4.jar"
        )

        self.cache_dir = os.path.join(
            assets_root, "schematron-cache"
        )
        os.makedirs(self.cache_dir, exist_ok=True)

    # ------------------------------------------------------------------ #
    # Execute DRIVER XSL → SVRL
    # ------------------------------------------------------------------ #
    def _run_driver_xsl(self, xsl_path, xml_path, svrl_path):
        cmd = [
            "java",
            "-cp",
            f"{self.saxon_jar}:{self.xmlresolver_jar}",
            "net.sf.saxon.Transform",
            f"-s:{xml_path}",
            f"-xsl:{xsl_path}",
            f"-o:{svrl_path}",
        ]
        subprocess.run(cmd, check=True)

    # ------------------------------------------------------------------ #
    # Parse SVRL
    # ------------------------------------------------------------------ #
    def _parse_svrl(self, svrl_path, result, source):
        with open(svrl_path, "rb") as f:
            head = f.read(64).lstrip()
            if not head.startswith(b"<"):
                result.add_entries([{
                    "level": "error",
                    "code": "SCHEMATRON-RUNTIME",
                    "message": head.decode(errors="ignore"),
                    "source": source,
                }])
                return

        tree = etree.parse(svrl_path)
        root = tree.getroot()

        ns = {
            "svrl": "http://purl.oclc.org/dsdl/svrl"
        }

        entries = []

        for failed in root.findall(".//svrl:failed-assert", namespaces=ns):
            text = failed.findtext("svrl:text", namespaces=ns)
            location = failed.get("location")

            entries.append({
                "level": "error",
                "rule_id": failed.get("id"),
                "message": text,
                "location": location,
                "source": source,
            })

        result.add_entries(entries)

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #
    def validate(self, xml_path, schematron_stages, result):
        """
        Execute schematron stages in order.
        Each stage MUST specify a DRIVER XSL.
        """

        for stage in schematron_stages:
            xsl_path = os.path.join(
                stage["path"],
                stage["driver"],
            )

            svrl_hash = hashlib.sha256(
                (xsl_path + xml_path).encode("utf-8")
            ).hexdigest()

            svrl_path = os.path.join(
                self.cache_dir,
                f"svrl-{svrl_hash}.xml"
            )

            self._run_driver_xsl(xsl_path, xml_path, svrl_path)
            self._parse_svrl(svrl_path, result, stage["id"])
