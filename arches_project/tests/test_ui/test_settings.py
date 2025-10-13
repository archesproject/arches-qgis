import unittest

from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

from arches_project.tests.base_test import ArchesQGISTestCase

from arches_project.tests.utils.utilities import get_qgis_app

CANVAS, PARENT, IFACE, QGIS_APP = get_qgis_app()


class SettingsTabTests(ArchesQGISTestCase):
    """Simple test to check dialog works."""

    def test_arches_theme_button(self):
        """
        Test the Arches theme button.
        """
        button = self.dlg.useStylesheetCheckbox

        # This should be checked by default
        self.assertTrue(button.isChecked())

        QTest.mouseClick(button, Qt.LeftButton)
        self.assertFalse(button.isChecked())
