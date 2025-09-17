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
from utils.utilities import get_qgis_app
CANVAS, PARENT, IFACE, QGIS_APP = get_qgis_app()


class SettingsTabTests(unittest.TestCase):
    """Simple test to check dialog works."""

    def setUp(self):
        """Runs before each test."""
        self.dlg = ArchesProjectDialog()            
        self.dlg_resource_creation = CreateResourceConfirmation()
        self.dlg_edit_resource_add = EditResourceAddConfirmation()
        self.dlg_edit_resource_replace = EditResourceReplaceConfirmation()
        self.arches_project = ArchesProject(IFACE)
        PluginStylesheets(self.dlg, 
                          self.dlg_resource_creation, 
                          self.dlg_edit_resource_add, 
                          self.dlg_edit_resource_replace, 
                          self.arches_project.plugin_dir, 
                          True)

    def tearDown(self):
        """Runs after each test."""
        self.dlg = None

    def test_arches_theme_button(self):
        """
        Test the Arches theme button.
        """
        button = self.dlg.useStylesheetCheckbox

        # This should be checked by default
        self.assertTrue(button.isChecked())

        QTest.mouseClick(button, Qt.LeftButton)
        self.assertFalse(button.isChecked())