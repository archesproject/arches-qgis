import os.path as path
# import unittest

# from arches_project.arches_project import ArchesProject
# from arches_project.core.arches.connection import ArchesConnection

from qgis.core import Qgis, QgsOfflineEditing, QgsProject
from qgis.testing import start_app, unittest
from qgis.testing.mocked import get_iface

# start_app()

# class TestCore(unittest.TestCase):

#     def test_core(self):
        
#         result = MyCode(image=image, normalize=True, quotient=255).execute(constant=0.01, threshold=0.2)

#         # evaluate
#         self.assertEqual(len(result), len(image))
#         # todo it makes more sense to compare the actual content of the array, we leave this up to you

        
#         ArchesProject.arches_connection_save

class OfflineConverterTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.iface = get_iface()

    def test_first(self):
        print(Qgis.QGIS_VERSION_INT)