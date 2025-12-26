import os
import hashlib
import subprocess
from lxml import etree


class SchematronValidator:
    """
    Schematron validator using Saxon-HE.

    Execution model:
    ----------------
    1. EN16931 is executed via OFFICIAL DRIVER XSL
       (EN16931-UBL-validation.xsl)
       → provides all variables, phases, includes

    2. HR-CIUS schematron is executed AFTER EN16931
       using ISO skeleton compilation

    This matches:
    - CEN / Connecting Europe reference implementation
    - FINA HR-CIUS instructions
    """

    # ------------------------------------------------------------------ #
    # Init
    # ------------------------------------------------------------------ #
    def __init__(self, assets_root):
        self.assets_root = assets_root

        self.saxon_jar = os.path.join(
            assets_root, "java", "Saxon-HE-12.4.jar"
        )
        self.xmlresolver_jar = os.path.join(
            assets_root, "java", "xmlresolver-4.6.4.jar"
        )

        self.iso_dir = os.path.join(
            assets_root, "schematron", "iso"
        )
        self.cache_dir = os.path.join(
            assets_root, "schematron-cache"
        )
        os.makedirs(self.cache_dir, exist_ok=True)

    # ------------------------------------------------------------------ #
    # Saxon runner
    # ------------------------------------------------------------------ #
    def _run_saxon(self, source_xml, xsl_path, output_path):
        cmd = [
            "java",
            "-cp",
            f"{self.saxon_jar}:{self.xmlresolver_jar}",
            "net.sf.saxon.Transform",
            f"-s:{source_xml}",
            f"-xsl:{xsl_path}",
            f"-o:{output_path}",
        ]
        subprocess.run(cmd, check=True)

    # ------------------------------------------------------------------ #
    # EN16931 DRIVER XSL
    # ------------------------------------------------------------------ #
    def run_driver(self, xml_path, driver_xsl_path, result):
        """
        Execute official EN16931 driver XSL.
        This MUST run before any CIUS schematron.
        """

        h = hashlib.sha256(
            (xml_path + driver_xsl_path).encode("utf-8")
        ).hexdigest()

        svrl_path = os.path.join(
            self.cache_dir, f"svrl-driver-{h}.xml"
        )

        self._run_saxon(xml_path, driver_xsl_path, svrl_path)
        self._parse_svrl(
            svrl_path,
            result,
            source="EN16931",
        )

    # ------------------------------------------------------------------ #
    # Compile SCH → XSL (ISO skeleton)
    # ------------------------------------------------------------------ #
    def _compile_schematron(self, sch_path):
        """
        Compile schematron using ISO skeleton (cached).
        Used ONLY for HR-CIUS.
        """

        h = hashlib.sha256(sch_path.encode("utf-8")).hexdigest()
        xsl_path = os.path.join(self.cache_dir, f"{h}.xsl")

        if os.path.exists(xsl_path):
            return xsl_path

        skeleton = os.path.join(
            self.iso_dir,
            "iso_schematron_skeleton_for_saxon.xsl",
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
    # HR-CIUS SCHEMATRON
    # ------------------------------------------------------------------ #
    def validate(self, xml_path, schematron_list, result):
        """
        Execute HR-CIUS schematron(s) AFTER EN16931 driver.
        """

        for sch_info in schematron_list:
            sch_path = sch_info["path"]
            source = sch_info["id"]

            xsl_path = self._compile_schematron(sch_path)

            h = hashlib.sha256(
                (xml_path + sch_path).encode("utf-8")
            ).hexdigest()

            svrl_path = os.path.join(
                self.cache_dir, f"svrl-hrcius-{h}.xml"
            )

            self._run_saxon(xml_path, xsl_path, svrl_path)
            self._parse_svrl(
                svrl_path,
                result,
                source=source,
            )

    # ------------------------------------------------------------------ #
    # SVRL PARSER
    # ------------------------------------------------------------------ #
    def _parse_svrl(self, svrl_path, result, source):
        """
        Parse SVRL and add entries to ValidationResult.
        """

        # Guard against Saxon text output
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

        for failed in root.findall(
            ".//svrl:failed-assert",
            namespaces=ns,
        ):
            text = failed.findtext(
                "svrl:text",
                namespaces=ns,
            )
            location = failed.get("location")

            rule_id = None
            if text and text.startswith("["):
                rule_id = text.split("]")[0].strip("[")

            entries.append({
                "level": "error",
                "rule_id": rule_id,
                "message": text,
                "location": location,
                "source": source,
            })

        result.add_entries(entries)
