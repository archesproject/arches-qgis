from arches_project.core.arches.resources import ArchesResources
from arches_project.core.arches.api import arches_api
from arches_project.core.views.components.map import (
    save_selected_arches_resource,
    populate_table,
)


class ResourcesView:
    """
    Resources view for Arches instance
    """

    def __init__(self, iface, dlg):
        self.dlg = dlg
        self.iface = iface

    def create_resource(self, dlg_resource_confirmation):
        """
        Create Resource dialog and functionality
        """

        arches_create_resource = ArchesResources(
            nodeid=None, tileid=None  # filled by selectedNode
        )
        arches_create_resource.create_resource(
            dlg=self.dlg,
            dlg_resource_confirmation=dlg_resource_confirmation,
            iface=self.iface,
        )

    def edit_resource(self, replace, dlg_resource_confirmation):
        """Save geometries to existing resource - either replace or add"""

        arches_edit_resource = ArchesResources(
            nodeid=arches_api.arches_selected_resource["nodeid"],
            tileid=arches_api.arches_selected_resource["tileid"],
        )
        arches_edit_resource.edit_resource(
            replace=replace,
            dlg=self.dlg,
            dlg_resource_confirmation=dlg_resource_confirmation,
            iface=self.iface,
        )

    def register_resource(self):
        """
        Button connection for registering Arches resource with the plugin.

        Only when the button is activated and successful will the rest of the edit
        UI be revealed, and the Arches resource stored until re-registered.
        """

        self.dlg.editResSelectResButton.setText("Register resource for editing")

        if not arches_api.selected_features["features"]:
            # show confirmation message
            self.dlg.editResRegisterResMessageLabel.show()
            self.dlg.editResRegisterResMessageLabel.setText(
                "No features are selected. Select an Arches feature to proceed."
            )
            # hide operation frame
            self.dlg.editResOperationFrame.hide()
        else:
            if len(arches_api.selected_features["features"]) > 1:
                self.dlg.editResRegisterResMessageLabel.show()
                self.dlg.editResRegisterResMessageLabel.setText(
                    "Multiple features are selected. Select one Arches feature to proceed."
                )
                self.dlg.editResOperationFrame.hide()
            else:
                # One in the selected features list, need to check if is Arches resource
                feat = arches_api.selected_features["features"][0]
                save_arches_res = save_selected_arches_resource(feat)
                if save_arches_res:
                    populate_table(self.dlg, feat)
                    self.dlg.editResRegisterResMessageLabel.setText("")
                    self.dlg.editResRegisterResMessageLabel.hide()
                    self.dlg.editResOperationFrame.show()

                    # rename register label and button text
                    self.dlg.editResSelectedResLabel.setText(
                        f"Selected resource: {arches_api.arches_selected_resource['resourceinstanceid']}"
                    )
                    self.dlg.editResSelectResButton.setText("Register new resource")

                    # automatically deselect the selected Arches resource
                    self.iface.activeLayer().removeSelection()
                else:
                    self.dlg.editResRegisterResMessageLabel.show()
                    self.dlg.editResRegisterResMessageLabel.setText(
                        "The selected feature is not an Arches resource. Select an Arches feature to proceed."
                    )
                    self.dlg.editResOperationFrame.hide()
