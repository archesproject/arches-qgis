import unittest
import requests

from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

from arches_project.tests.base_test import ArchesQGISTestCase

from arches_project.tests.utils.utilities import get_qgis_app

CANVAS, PARENT, IFACE, QGIS_APP = get_qgis_app()


class ConnectionTests(ArchesQGISTestCase):
    """
    Test connection to Arches.
    """

    def test_get_clientid(self):

        files = {
            "username": (None, "admin"),
            "password": (None, "admin"),
        }
        response = requests.post(f"{self.arches_url}/auth/get_client_id", data=files)
        self.assertEqual(response.status_code, 200)