import unittest

from PyQt5.QtWidgets import QDialogButtonBox, QDialog
from PyQt5.QtTest import QTest, QSignalSpy
from PyQt5.QtCore import Qt

from arches_project.ui.arches_project_dialog import ArchesProjectDialog
from arches_project.ui.create_resource_confirmation_dialog import CreateResourceConfirmation
from arches_project.ui.edit_resource_add_confirmation_dialog import EditResourceAddConfirmation
from arches_project.ui.edit_resource_replace_confirmation_dialog import EditResourceReplaceConfirmation

from arches_project.arches_project import ArchesProject
from arches_project.core.views.stylesheets import PluginStylesheets
from arches_project.tests.base_test import ArchesQGISTestCase

from utils.utilities import get_qgis_app
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