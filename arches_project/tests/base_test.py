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

    @classmethod
    def setUpClass(cls):
        """
        Runs once at start of all testing.
        """
        QSettings().setValue("locale/userLocale", "en")
        QSettings().setValue("urls", ["http://127.0.0.1:8000"])
        QSettings().setValue("usernames", ["admin"])

        cls.iface = IFACE
        cls.arches_project = ArchesProject(cls.iface)
        cls.plugin_dir = "/tests_directory/arches_project"

        # Call the dialogs from within the plugin rather than establishing new ones.
        cls.dlg = cls.arches_project.dlg
        cls.dlg_resource_confirmation = cls.arches_project.dlg_resource_confirmation

        PluginStylesheets(
            cls.dlg,
            cls.dlg_resource_confirmation,
            cls.arches_project.plugin_dir,
            True,
        )

        cls.arches_url = (
            f"http://{os.environ.get('ARCHES_HOST')}:{os.environ.get('DJANGO_PORT')}"
        )

        cls.arches_project.first_start = True
        cls.arches_project.initGui()
        cls.arches_project.run()

    @classmethod
    def tearDownClass(cls):
        """
        Runs once after end of all testing.
        """
        QSettings().setValue("locale/userLocale", None)
        QSettings().setValue("urls", [])
        QSettings().setValue("usernames", [])

        cls.arches_project.unload()
        cls.arches_project = None

        cls.dlg = None
        cls.dlg_resource_confirmation = None
        cls.arches_url = None
