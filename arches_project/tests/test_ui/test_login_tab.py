# coding=utf-8
"""Resources test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = "samuel.scandrett@k-int.co.uk"
__date__ = "2023-09-15"
__copyright__ = "Copyright 2023, Knowledge Integration"

import unittest

from arches_project.tests.base_test import ArchesQGISTestCase

from qgis.PyQt.QtGui import QIcon
from PyQt5.QtCore import Qt


class LoginTabTests(ArchesQGISTestCase):
    """Test resources work."""

    def test_server_completer_exists(self):
        completer = self.dlg.archesServerInput.completer()
        self.assertIsNotNone(completer)

    def test_username_completer_exists(self):
        completer = self.dlg.usernameInput.completer()
        self.assertIsNotNone(completer)

    def test_server_first_autocomplete_value(self):
        completer = self.dlg.archesServerInput.completer()
        model = completer.model()
        index = model.index(0, 0)
        value = model.data(index, Qt.DisplayRole)
        self.assertEqual(value, "http://127.0.0.1:8000")

    def test_username_first_autocomplete_value(self):
        completer = self.dlg.usernameInput.completer()
        model = completer.model()
        index = model.index(0, 0)
        value = model.data(index, Qt.DisplayRole)
        self.assertEqual(value, "admin")
