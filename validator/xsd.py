import os
from lxml import etree


class XsdValidator:
    def __init__(self, assets_root):
        self.assets_root = assets_root
        self._schema_cache = {}

    def validate(self, xml_path, profile, document_type, result):
        try:
            main_xsd = self._resolve_main_xsd(profile, document_type)
            schema = self._load_schema(main_xsd)

            doc = etree.parse(xml_path)
            schema.assertValid(doc)
            return True

        except etree.DocumentInvalid as e:
            for error in e.error_log:
                result.add_entries([{
                    "level": "error",
                    "type": "xsd",
                    "message": error.message,
                    "line": error.line,
                    "source": profile["fallbacks"].get("xsd", profile["base"]),
                }])
            return False

    def _resolve_main_xsd(self, profile, document_type):
        doc_map = {
            "invoice": "UBL-Invoice-2.1.xsd",
            "creditnote": "UBL-CreditNote-2.1.xsd",
        }

        filename = doc_map[document_type]

        # ✅ ALWAYS validate against base UBL 2.1 XSDs
        return os.path.join(
            self.assets_root,
            "xsd",
            "ubl-2.1",
            "xsd",
            "maindoc",
            filename,
        )

    def _load_schema(self, xsd_path):
        if xsd_path not in self._schema_cache:
            schema_doc = etree.parse(xsd_path)
            self._schema_cache[xsd_path] = etree.XMLSchema(schema_doc)
        return self._schema_cache[xsd_path]
