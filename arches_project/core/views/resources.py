from arches_project.core.arches.resources import ArchesResources
from arches_project.core.arches.api import arches_api


class ResourcesView:
    """
    Resources view for Arches instance
    """

    def __init__(self, iface, dlg):
        self.dlg = dlg
        self.iface = iface

    def create_resource(self, dlg_resource_creation):
        """
        Create Resource dialog and functionality
        """

        arches_create_resource = ArchesResources(
            nodeid=None, tileid=None  # filled by selectedNode
        )
        arches_create_resource.create_resource(
            dlg=self.dlg,
            dlg_resource_creation=dlg_resource_creation,
            iface=self.iface,
        )

    def edit_resource(self, replace, dlg_edit_resource_replace, dlg_edit_resource_add):
        """Save geometries to existing resource - either replace or add"""

        arches_edit_resource = ArchesResources(
            nodeid=arches_api.arches_selected_resource["nodeid"],
            tileid=arches_api.arches_selected_resource["tileid"],
        )
        arches_edit_resource.edit_resource(
            replace=replace,
            dlg=self.dlg,
            dlg_edit_resource_replace=dlg_edit_resource_replace,
            dlg_edit_resource_add=dlg_edit_resource_add,
            iface=self.iface,
        )
