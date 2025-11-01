from arches_project.core.arches.resources import ArchesResources
from arches_project.core.arches.api import arches_api


class ResourcesView:
    """
    Resources view for Arches instance
    """

    def __init__(self, iface, dlg, dlg_resource_creation):
        self.dlg = dlg
        self.dlg_resource_creation = dlg_resource_creation
        self.iface = iface

    def create_resource(self):
        """
        Create Resource dialog and functionality
        """

        arches_create_resource = ArchesResources(
            nodeid=None, tileid=None  # filled by selectedNode
        )
        arches_create_resource.create_resource(
            dlg=self.dlg,
            dlg_resource_creation=self.dlg_resource_creation,
            iface=self.iface,
        )
