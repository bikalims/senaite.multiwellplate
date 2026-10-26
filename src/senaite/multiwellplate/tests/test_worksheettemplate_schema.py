# -*- coding: utf-8 -*-
"""The add-on must not modify schemas used by other sites."""
import os
import unittest
import xml.etree.ElementTree as ET

from plone.dexterity.fti import DexterityFTI
from plone.supermodel.interfaces import FIELDSETS_KEY
from plone.supermodel.utils import mergedTaggedValueList
from senaite.core.content.worksheettemplate import IWorksheetTemplateSchema
from senaite.multiwellplate.content.worksheettemplate import (
    IMultiWellPlateWorksheetTemplateSchema, MULTIWELLPLATE_FIELDS)


class WorksheetTemplateSchemaTest(unittest.TestCase):

    def profile_schema(self, profile):
        root = os.path.dirname(os.path.dirname(__file__))
        path = os.path.join(root, "profiles", profile,
                            "types", "WorksheetTemplate.xml")
        return ET.parse(path).find("property[@name='schema']").text

    def test_core_schema_is_not_extended(self):
        for name in MULTIWELLPLATE_FIELDS:
            self.assertNotIn(name, IWorksheetTemplateSchema)
        fieldsets = mergedTaggedValueList(IWorksheetTemplateSchema, FIELDSETS_KEY)
        self.assertNotIn("multiwellplate", [f.__name__ for f in fieldsets])

    def test_installed_schema_preserves_core_and_adds_config(self):
        schema = IMultiWellPlateWorksheetTemplateSchema
        for name in IWorksheetTemplateSchema.names(all=True):
            self.assertIn(name, schema)
        for name in MULTIWELLPLATE_FIELDS:
            self.assertIn(name, schema)
        fieldsets = mergedTaggedValueList(schema, FIELDSETS_KEY)
        names = [f.__name__ for f in fieldsets]
        self.assertEqual(names.count("multiwellplate"), 1)
        for fieldset in mergedTaggedValueList(IWorksheetTemplateSchema, FIELDSETS_KEY):
            self.assertIn(fieldset.__name__, names)

    def test_type_schema_is_isolated_and_uninstall_restores_core(self):
        installed = DexterityFTI("WorksheetTemplate")
        installed.schema = self.profile_schema("default")
        other_site = DexterityFTI("WorksheetTemplate")
        other_site.schema = self.profile_schema("uninstall")
        for unused in range(2):
            self.assertIs(installed.lookupSchema(), IMultiWellPlateWorksheetTemplateSchema)
            self.assertIs(other_site.lookupSchema(), IWorksheetTemplateSchema)
            self.assertNotIn("fields", other_site.lookupSchema())
        installed.schema = self.profile_schema("uninstall")
        self.assertIs(installed.lookupSchema(), IWorksheetTemplateSchema)


if __name__ == "__main__":
    unittest.main()
