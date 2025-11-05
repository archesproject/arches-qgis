import unittest
import os

from arches_project.arches_project import ArchesProject
from arches_project.core.views.stylesheets import PluginStylesheets

from qgis.PyQt.QtCore import QSettings

from arches_project.tests.utils.utilities import get_qgis_app

CANVAS, PARENT, IFACE, QGIS_APP = get_qgis_app()

from dotenv import load_dotenv

load_dotenv("test/arches/.env")


class ArchesQGISTestCase(unittest.TestCase):
    """
    Extended unittest TestCase including plugin setup and configuration.
    """

    def setUp(self):
        """
        Runs before each test.
        """

        QSettings().setValue("locale/userLocale", "en")

        self.arches_project = ArchesProject(IFACE)

        # Call the dialogs from within the plugin rather than establishing new ones.
        self.dlg = self.arches_project.dlg
        self.dlg_resource_creation = self.arches_project.dlg_resource_creation
        self.dlg_edit_resource_add = self.arches_project.dlg_edit_resource_add
        self.dlg_edit_resource_replace = self.arches_project.dlg_edit_resource_replace

        PluginStylesheets(
            self.dlg,
            self.dlg_resource_creation,
            self.dlg_edit_resource_add,
            self.dlg_edit_resource_replace,
            self.arches_project.plugin_dir,
            True,
        )

        self.arches_url = (
            f"http://{os.environ.get('ARCHES_HOST')}:{os.environ.get('DJANGO_PORT')}"
        )

        self.arches_project.first_start = True
        self.arches_project.initGui()

    def tearDown(self):
        """
        Runs after each test.
        """
        QSettings().setValue("locale/userLocale", None)

        self.arches_project.unload()
        self.arches_project = None

        self.dlg = None
        self.dlg_resource_creation = None
        self.dlg_edit_resource_add = None
        self.dlg_edit_resource_replace = None

        self.arches_url = None
