import unittest

from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

from arches_project.tests.base_test import ArchesQGISTestCase

from arches_project.tests.utils.utilities import get_qgis_app

CANVAS, PARENT, IFACE, QGIS_APP = get_qgis_app()


class ConnectionTests(ArchesQGISTestCase):
    """
    Test connection to Arches UI.
    """

    def test_missing_connection_credentials(self):

        cases = [
            {
                "type": "missing password",
                "url": self.arches_url,
                "username": "admin",
                "password": "",
                "expected_msg": "Login missing password.",
            },
            {
                "type": "missing username",
                "url": self.arches_url,
                "username": "",
                "password": "admin",
                "expected_msg": "Login missing username.",
            },
            {
                "type": "missing url",
                "url": "",
                "username": "admin",
                "password": "admin",
                "expected_msg": "Login missing URL.",
            },
            {
                "type": "missing username and password",
                "url": self.arches_url,
                "username": "",
                "password": "",
                "expected_msg": "Login missing values for username and password.",
            },
            {
                "type": "missing all",
                "url": "",
                "username": "",
                "password": "",
                "expected_msg": "Login missing values for URL, username and password.",
            },
        ]

        for case in cases:
            with self.subTest(case=case):
                self.dlg.archesServerInput.setText(case["url"])
                self.dlg.usernameInput.setText(case["username"])
                self.dlg.passwordInput.setText(case["password"])
                QTest.mouseClick(self.dlg.btnConnect, Qt.LeftButton)
                self.assertEqual(
                    self.dlg.loginErrorMessageLabel.text(), case["expected_msg"]
                )

    def test_successful_arches_login(self):
        self.dlg.archesServerInput.setText(self.arches_url)
        self.dlg.usernameInput.setText("admin")
        self.dlg.passwordInput.setText("admin")

        QTest.mouseClick(self.dlg.btnConnect, Qt.LeftButton)

        # arches_connection object only exists on successful