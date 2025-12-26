# eracun_validator/validator/xsd.py

import os
from lxml import etree


class XsdValidator:
    def __init__(self, assets_root):
        self.assets_root = assets_root
        self._schema_cache = {}

    # -------------------------------------------------
    # Public API
    # -------------------------------------------------

    def validate(self, xml_path, profile, document_type, result):
        """
        Validate XML against profile-specific XSDs.

        Returns:
            True  -> XSD valid
            False -> XSD invalid (errors added to result)
        """
        try:
            xsd_path = self._resolve_main_xsd(profile, document_type)
            schema = self._load_schema(xsd_path)

            doc = etree.parse(xml_path)
            schema.assertValid(doc)

            return True

        except etree.DocumentInvalid as e:
            for error in e.error_log:
                result.add_entries([
                    {
                        "level": "error",
                        "type": "xsd",
                        "message": error.message,
                        "line": error.line,
                        "source": profile["id"],
                    }
                ])
            return False

        except Exception as e:
            result.add_entries([
                {
                    "level": "error",
                    "type": "xsd",
                    "message": str(e),
                    "line": None,
                    "source": profile["id"],
                }
            ])
            return False

    # -------------------------------------------------
    # Internals
    # -------------------------------------------------

    def _resolve_main_xsd(self, profile, document_type):
        """
        Resolve the main XSD file for this profile and document type.
        """
        xsd_root = profile["xsd"]["path"]

        if document_type == "invoice":
            filename = "UBL-Invoice-2.1.xsd"
        elif document_type == "creditnote":
            filename = "UBL-CreditNote-2.1.xsd"
        else:
            raise ValueError(f"Unsupported document type: {document_type}")

        return os.path.join(xsd_root, filename)

    def _load_schema(self, xsd_path):
        """
        Load and cache XMLSchema objects.
        """
        if xsd_path not in self._schema_cache:
            schema_doc = etree.parse(xsd_path)
            self._schema_cache[xsd_path] = etree.XMLSchema(schema_doc)

        return self._schema_cache[xsd_path]
