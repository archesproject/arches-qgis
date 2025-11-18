import unittest
from unittest.mock import MagicMock, patch

from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

from arches_project.tests.base_test import ArchesQGISTestCase
from arches_project.core.arches.connection import ConnectionProcess
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

    def test_changes_to_ui_after_connection(self):
        self.arches_connection = ConnectionProcess(
            url=self.arches_url,
            username="admin",
            password="admin",
            dlg=self.dlg,
            iface=IFACE,
            plugin_dir=self.arches_project.plugin_dir,
        )

        result = self.arches_connection.run()
        self.arches_connection.finished(result)

        self.assertTrue(
            result,
            "ConnectionProcess.run() should return True when given valid credentials",
        )

        self.assertEqual(
            self.dlg.tabWidget.currentIndex(), 1, "Logged-in tab should be current tab"
        )
        self.assertTrue(
            self.dlg.tabWidget.isTabVisible(1), "Logged-in tab should be visible"
        )
        self.assertFalse(
            self.dlg.tabWidget.isTabVisible(0), "Log-in tab should not be visible"
        )

        # Logged-in tab display changes (when user has no fullname stored)
        self.assertEqual(
            self.dlg.displayFullNameLabel.text(), "admin", "Full name label is username"
        )
        self.assertFalse(
            self.dlg.displayUsernameLabel.isVisible(), "Username label should be hidden"
        )
        self.assertFalse(
            self.dlg.displayUsernameFrame.isVisible(), "Username frame should be hidden"
        )

        # TODO: add tests for Create and Edit resource tab UIs once test layers are available in test Arches and QGIS instances
