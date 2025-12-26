import os
import hashlib
import subprocess
from lxml import etree


class SchematronValidator:
    """
    Schematron validator using Saxon-HE and ISO Schematron skeleton.
    - Compiles .sch → cached .xsl
    - Executes XSLT to produce SVRL
    - Parses SVRL into ValidationResult entries

    Notes (per EN16931 / HR-CIUS instructions):
    - EN16931 schematron is executed first
    - HR-CIUS EXT schematron is executed AFTER EN16931
    - HR-CIUS codes.sch is NOT executed separately (already included)
    """

    def __init__(self, assets_root):
        self.assets_root = assets_root

        self.saxon_jar = os.path.join(
            assets_root, "java", "Saxon-HE-12.4.jar"
        )
        self.xmlresolver_jar = os.path.join(
            assets_root, "java", "xmlresolver-4.6.4.jar"
        )

        self.iso_dir = os.path.join(assets_root, "schematron", "iso")
        self.cache_dir = os.path.join(assets_root, "schematron-cache")
        os.makedirs(self.cache_dir, exist_ok=True)

    # ------------------------------------------------------------------ #
    # Compile .sch → .xsl (cached)
    # ------------------------------------------------------------------ #
    def _compile(self, sch_path):
        """
        Compile Schematron (.sch) to XSLT using ISO skeleton.
        Cache key = sha256(sch_path).
        """
        h = hashlib.sha256(sch_path.encode("utf-8")).hexdigest()
        xsl_path = os.path.join(self.cache_dir, f"{h}.xsl")

        if os.path.exists(xsl_path):
            return xsl_path

        skeleton = os.path.join(
            self.iso_dir, "iso_schematron_skeleton_for_saxon.xsl"
        )

        cmd = [
            "java",
            "-cp",
            f"{self.saxon_jar}:{self.xmlresolver_jar}",
            "net.sf.saxon.Transform",
            f"-s:{sch_path}",
            f"-xsl:{skeleton}",
            f"-o:{xsl_path}",
            "allow-foreign=true",
            "generate-fallback=true",
        ]

        subprocess.run(cmd, check=True)
        return xsl_path

    # ------------------------------------------------------------------ #
    # Execute compiled XSLT → SVRL
    # ------------------------------------------------------------------ #
    def _run_xslt(self, xsl_path, xml_path, svrl_path):
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
        """
        Parse SVRL file and append entries to ValidationResult.

        Guard:
        - Some broken runs output plain text instead of XML
        """
        with open(svrl_path, "rb") as f:
            head = f.read(64).lstrip()
            if not head.startswith(b"<"):
                # Not SVRL XML → treat as fatal schematron error
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
                "rule_id": (text.split("]")[0].strip("[") if text else None),
                "message": text,
                "location": location,
                "source": source,
            })

        result.add_entries(entries)

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #
    def validate(self, xml_path, profile, result):
        """
        Execute schematron validation stages defined by the profile.
        """
        schematron = profile.get("schematron")
        if not schematron:
            return

        stages = schematron.get("stages", [])

        for stage in stages:
            sch_path = os.path.join(
                stage["path"],
                stage["main"],
            )
            source = stage["id"]

            # -------------------------------------------------
            # Compile SCH → XSL (cached)
            # -------------------------------------------------
            xsl_path = self._compile(sch_path)

            # -------------------------------------------------
            # Execute XSL → SVRL
            # -------------------------------------------------
            svrl_hash = hashlib.sha256(
                (sch_path + xml_path).encode("utf-8")
            ).hexdigest()

            svrl_path = os.path.join(
                self.cache_dir, f"svrl-{svrl_hash}.xml"
            )

            self._run_xslt(xsl_path, xml_path, svrl_path)

            # -------------------------------------------------
            # Parse SVRL
            # -------------------------------------------------
            self._parse_svrl(svrl_path, result, source)

