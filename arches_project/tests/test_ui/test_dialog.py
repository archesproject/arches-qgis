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


class ArchesProjectDialogTest(ArchesQGISTestCase):
    """Test resources work."""

    def test_icon_png(self):
        """Test we can click OK."""
        path = ":/plugins/ArchesProject/arches.png"
        icon = QIcon(path)
        self.assertFalse(icon.isNull())
