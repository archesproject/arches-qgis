import unittest

from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

from arches_project.tests.base_test import ArchesQGISTestCase

from arches_project.tests.utils.utilities import get_qgis_app
CANVAS, PARENT, IFACE, QGIS_APP = get_qgis_app()


class ConnectionTests(ArchesQGISTestCase):
    """
    Test connection to Arches.
    """

    def test_missing_connection_credentials(self):
        # Missing password
        self.dlg.archesServerInput.setText(self.arches_url)
        self.dlg.usernameInput.setText("admin")
        self.dlg.passwordInput.setText("") 
        QTest.mouseClick(self.dlg.btnConnect, Qt.LeftButton)
        self.assertEqual(self.dlg.loginErrorMessageLabel.text(), "Login missing password.")

        # Missing username
        self.dlg.usernameInput.setText("")
        self.dlg.passwordInput.setText("admin") 
        QTest.mouseClick(self.dlg.btnConnect, Qt.LeftButton)
        self.assertEqual(self.dlg.loginErrorMessageLabel.text(), "Login missing username.")

        # Missing URL
        self.dlg.archesServerInput.setText("")
        self.dlg.usernameInput.setText("admin")
        QTest.mouseClick(self.dlg.btnConnect, Qt.LeftButton)
        self.assertEqual(self.dlg.loginErrorMessageLabel.text(), "Login missing URL.")

        # Missing two (e.g. username and password)
        self.dlg.archesServerInput.setText(self.arches_url)
        self.dlg.usernameInput.setText("")
        self.dlg.passwordInput.setText("") 
        QTest.mouseClick(self.dlg.btnConnect, Qt.LeftButton)
        self.assertEqual(self.dlg.loginErrorMessageLabel.text(), "Login missing values for username and password.")

        # Missing all three
        self.dlg.archesServerInput.setText("")
        QTest.mouseClick(self.dlg.btnConnect, Qt.LeftButton)
        self.assertEqual(self.dlg.loginErrorMessageLabel.text(), "Login missing values for URL, username and password.")


    def test_successful_arches_login(self):
        self.dlg.archesServerInput.setText(self.arches_url)
        self.dlg.usernameInput.setText("admin")
        self.dlg.passwordInput.setText("admin")

        QTest.mouseClick(self.dlg.btnConnect, Qt.LeftButton)

        # arches_connection object only exists on successful 
        print(self.arches_project.arches_token)
