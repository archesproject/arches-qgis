from unittest.mock import patch, MagicMock
import requests

from arches_project.tests.base_test import ArchesQGISTestCase

from arches_project.tests.utils.utilities import get_qgis_app
from arches_project.core.arches.connection import ConnectionProcess

CANVAS, PARENT, IFACE, QGIS_APP = get_qgis_app()


class ConnectionTests(ArchesQGISTestCase):
    """
    Test connection to Arches server.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client_id = "ZmRsVUmUtwas8lmgX40PmgAQacESxxv9EPQdIm8S"

    def test_get_clientid(self):
        files = {
            "username": (None, "admin"),
            "password": (None, "admin"),
        }
        response = requests.post(f"{self.arches_url}/auth/get_client_id", data=files)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["clientid"], self.client_id)

    def test_access_token(self):
        files = {
            "username": (None, "admin"),
            "password": (None, "admin"),
            "client_id": (None, self.client_id),
            "grant_type": (None, "password"),
        }
        response = requests.post(self.arches_url + "/o/token/", data=files)
        self.assertEqual(response.status_code, 200)

    @patch('qgis.core.QgsApplication.taskManager')
    def test_connection_task_is_added_on_save(self, mock_task_manager):
        mock_add_task = MagicMock()
        mock_task_manager.return_value.addTask = mock_add_task

        self.dlg.archesServerInput.setText(self.arches_url)
        self.dlg.usernameInput.setText("admin")
        self.dlg.passwordInput.setText("admin")

        self.dlg.arches_connection.arches_connection_save()

        mock_add_task.assert_called_once()
        added_task = mock_add_task.call_args[0][0]

        self.assertIsInstance(added_task, ConnectionProcess)
        self.assertEqual(added_task.url, self.arches_url)
        self.assertEqual(added_task.username, "admin")
        self.assertEqual(added_task.password, "admin")
        self.assertEqual(added_task.dlg, self.dlg)

