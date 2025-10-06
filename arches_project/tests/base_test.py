import unittest
import os

from arches_project.ui.arches_project_dialog import ArchesProjectDialog
from arches_project.ui.create_resource_confirmation_dialog import CreateResourceConfirmation
from arches_project.ui.edit_resource_add_confirmation_dialog import EditResourceAddConfirmation
from arches_project.ui.edit_resource_replace_confirmation_dialog import EditResourceReplaceConfirmation

from arches_project.arches_project import ArchesProject
from arches_project.core.views.stylesheets import PluginStylesheets

from qgis.PyQt.QtCore import QSettings

from arches_project.tests.utils.utilities import get_qgis_app
CANVAS, PARENT, IFACE, QGIS_APP = get_qgis_app()


class ArchesQGISTestCase(unittest.TestCase):
    """
    Extended unittest TestCase including plugin setup and configuration.
    """

    def setUp(self):
        """
        Runs before each test.
        """

        QSettings().setValue('locale/userLocale', 'en')

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
        """
        Runs after each test.
        """
        self.dlg = None
        self.dlg_resource_creation = None
        self.dlg_edit_resource_add = None
        self.dlg_edit_resource_replace = None
        self.arches_project = None
        QSettings().setValue('locale/userLocale', None)