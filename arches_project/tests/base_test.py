import unittest
import os

from arches_project.arches_project import ArchesProject

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
        QSettings().setValue("urls", ["http://127.0.0.1:8000"])
        QSettings().setValue("usernames", ["admin"])

        self.arches_project = ArchesProject(IFACE)

        # Call the dialogs from within the plugin rather than establishing new ones.
        self.dlg = self.arches_project.dlg
        self.dlg_resource_confirmation = self.arches_project.dlg_resource_confirmation

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
        QSettings().setValue("urls", [])
        QSettings().setValue("usernames", [])

        self.arches_project.unload()
        self.arches_project = None

        self.dlg = None
        self.dlg_resource_confirmation = None
        self.arches_url = None
