import json
from functools import partial

from qgis.core import QgsMessageLog, Qgis, QgsApplication
from PyQt5.QtCore import QObject, pyqtSignal

from arches_project.core.utils.geometry_conversion import Geometries
from arches_project.core.utils.network import ArchesRequester
from arches_project.core.views.components.qgis_messaging import show_message
from arches_project.core.arches.api import arches_api


class ArchesResources(QObject):

    resource_creation_finished = pyqtSignal(dict)

    def __init__(self, nodeid, tileid):
        super().__init__()
        self.nodeid = nodeid
        self.tileid = tileid

    def process_new_resource(self, data):
        try:
            resource_data = json.loads(data)
        except:
            self.resource_creation_finished.emit(
                {"error": f"Could not create resource {data}"}
            )
            return
        arches_created_resource = {
            "nodegroup_id": resource_data["nodegroup_id"],
            "resourceinstance_id": resource_data["resourceinstance_id"],
            "tile_id": resource_data["tileid"],
        }
        self.resource_creation_finished.emit(arches_created_resource)

    def save_to_arches(
        self, tileid, nodeid, geometry_collection, geometry_format, arches_operation
    ):
        """
        Save data to arches resource
        """

        data = {
            "tileid": tileid,
            "nodeid": nodeid,
            "data": geometry_collection,
            "format": geometry_format,
            "operation": arches_operation,
        }

        QgsMessageLog.logMessage(
            f"Getting Node Value {str(data)}",
            "Arches Plugin",
            level=Qgis.Info,
        )

        requester = ArchesRequester()
        requester.make_authenticated_request(
            f"/api/node_value/", arches_api.config_id, method="POST", payload=data
        )

        requester.complete_signal.connect(self.process_new_resource)

    def create_resource(self, dlg, dlg_resource_confirmation, iface):
        """
        Create Resource dialog and functionality
        """

        def update_ui(dlg, result):
            if not result["error"]:
                available_configs = (
                    QgsApplication.authManager().availableAuthMethodConfigs()
                )
                dlg.createResOutputBox.setText(
                    """Successfully created a new resource with the selected geometry.
                                                    \nTo continue the creation of your new resource, navigate to...\n%s/resource/%s"""
                    % (
                        available_configs[arches_api.config_id].uri(),
                        result["resourceinstance_id"],
                    )
                )
                show_message(
                    iface, "Success", "A new Arches resource has been created."
                )
                dlg_resource_creation.close()
            else:
                dlg.createResOutputBox.setText("Resource creation FAILED.")
                show_message(
                    iface,
                    "Error",
                    f"Resource creation failed. {result['error']}",
                    duration=-1,
                )
                dlg_resource_creation.close()

        def send_new_resource_to_arches():
            if (
                selectedNode["nodegroup_id"]
                in arches_api.arches_user_info["editable_nodegroups"]
            ):
                self.save_to_arches(
                    tileid=self.tileid,
                    nodeid=selectedNode["node_id"],
                    geometry_collection=geomcoll,
                    geometry_format=None,
                    arches_operation="create",
                )
                update_ui_handler = partial(update_ui, dlg)

                self.resource_creation_finished.connect(update_ui_handler)

            else:
                dlg.createResOutputBox.setText(
                    "This user does not have permission to create data for the geometry nodegroup in this resource model. An Arches resource has not been created."
                )
                show_message(
                    iface,
                    "Error",
                    "The user does not have permission to create data.",
                    duration=-1,
                )
                dlg_resource_confirmation.close()

        def close_dialog():
            dlg_resource_confirmation.close()
            dlg_resource_confirmation.messageLabel.setText("Confirmation prompt")

        # Get info on current layer and selected graph
        selectedLayerIndex = dlg.createResFeatureSelect.currentIndex()
        selectedLayer = arches_api.layers[selectedLayerIndex]
        selectedGraphIndex = dlg.createResModelSelect.currentIndex()
        selectedGraph = arches_api.arches_graphs_list[selectedGraphIndex]

        if selectedGraph["multiple_geometry_nodes"] == True:
            selectedNodeIndex = dlg.geometryNodeSelect.currentIndex()
            selectedNode = arches_api.geometry_nodes[selectedNodeIndex]

        elif selectedGraph["multiple_geometry_nodes"] == False:
            node_id = list(selectedGraph["geometry_node_data"].keys())[0]
            nodegroup_id = selectedGraph["geometry_node_data"][node_id]["nodegroup_id"]
            selectedNode = {
                "node_id": node_id,
                "nodegroup_id": nodegroup_id,
                "name": selectedGraph["geometry_node_data"][node_id]["name"],
            }

        geom_convert = Geometries(selectedLayer)
        geomcoll, geometry_type_dict = geom_convert.geometry_conversion()

        # Format text box
        dlg_resource_confirmation.infoText.viewport().setAutoFillBackground(
            False
        )  # Sets the text box to be invisible
        dlg_resource_confirmation.infoText.setText("")
        dlg_resource_confirmation.infoText.append(
            "An Arches resource will be created with the following geometries:\n"
        )
        for k, v in geometry_type_dict.items():
            dlg_resource_confirmation.infoText.append(f"{k}: {v}")

        # open dialog
        dlg_resource_confirmation.confirmDialogConfirm.setText("Create")
        dlg_resource_confirmation.messageLabel.setText(
            "Are you sure you want to CREATE an Arches resource?"
        )
        dlg_resource_confirmation.show()

        # Push button responses
        dlg_resource_confirmation.confirmDialogConfirm.clicked.connect(
            send_new_resource_to_arches
        )
        dlg_resource_confirmation.confirmDialogCancel.clicked.connect(close_dialog)

    def edit_resource(
        self,
        replace,
        dlg,
        dlg_resource_confirmation,
        iface,
    ):
        """
        Save geometries to existing resource - either replace or add
        """

        def send_edited_data_to_arches(operation_type, dialog):
            if nodegroup_value in arches_api.arches_user_info["editable_nodegroups"]:
                try:
                    self.save_to_arches(
                        tileid=self.tileid,
                        nodeid=self.nodeid,
                        geometry_collection=geomcoll,
                        geometry_format=None,
                        arches_operation=operation_type,
                    )
                    show_message(
                        iface,
                        "Success",
                        f"Resource geometry {operation_type} was successful.",
                    )
                    dialog.close()
                except:
                    print(f"Couldn't {operation_type} geometry in resource")
                    show_message(
                        iface,
                        "error",
                        f"Couldn't {operation_type} geometry in resource",
                        duration=-1,
                    )
                    dialog.close()
            else:
                show_message(
                    iface,
                    "error",
                    "This user does not have permission to update data for the geometry nodegroup in this resource model",
                    duration=-1,
                )
                print(
                    "This user does not have permission to update data for the geometry nodegroup in this resource model."
                )
                dialog.close()

        def close_dialog(dialog):
            dialog.close()
            dlg_resource_confirmation.messageLabel.setText("Confirmation prompt")

        if arches_api.arches_selected_resource:
            selectedLayerIndex = dlg.editResSelectFeatures.currentIndex()
            selectedLayer = arches_api.layers[selectedLayerIndex]

            geom_convert = Geometries(selectedLayer)
            geomcoll, geometry_type_dict = geom_convert.geometry_conversion()

            # Get nodegroup from graph
            for graph in arches_api.arches_graphs_list:
                for k, v in graph["geometry_node_data"].items():
                    if k == arches_api.arches_selected_resource["nodeid"]:
                        nodegroup_value = v["nodegroup_id"]
                        break

            # Replace geometry
            if replace == True:
                # Format text box
                dlg_resource_confirmation.infoText.viewport().setAutoFillBackground(
                    False
                )  # Sets the text box to be invisible
                dlg_resource_confirmation.infoText.setText("")
                dlg_resource_confirmation.infoText.append(
                    "The following geometries will be replace the existing Arches resource's geometries:\n"
                )
                for k, v in geometry_type_dict.items():
                    dlg_resource_confirmation.infoText.append(f"{k}: {v}")

                dlg_resource_confirmation.confirmDialogConfirm.disconnect()
                dlg_resource_confirmation.confirmDialogConfirm.clicked.connect(
                    partial(
                        send_edited_data_to_arches,
                        operation_type="create",
                        dialog=dlg_resource_confirmation,
                    )
                )
                dlg_resource_confirmation.confirmDialogCancel.disconnect()
                dlg_resource_confirmation.confirmDialogCancel.clicked.connect(
                    partial(close_dialog, dialog=dlg_resource_confirmation)
                )
                # Show confirmation dialog
                dlg_resource_confirmation.confirmDialogConfirm.setText("Replace")
                dlg_resource_confirmation.messageLabel.setText(
                    "Are you sure you want to REPLACE geometries?"
                )
                dlg_resource_confirmation.show()

            # Add geometry to the resource
            else:
                # Format text box
                dlg_resource_confirmation.infoText.viewport().setAutoFillBackground(
                    False
                )  # Sets the text box to be invisible
                dlg_resource_confirmation.infoText.setText("")
                dlg_resource_confirmation.infoText.append(
                    "The following geometries will be added to the Arches resource:\n"
                )
                for k, v in geometry_type_dict.items():
                    dlg_resource_confirmation.infoText.append(f"{k}: {v}")

                dlg_resource_confirmation.confirmDialogConfirm.disconnect()
                dlg_resource_confirmation.confirmDialogConfirm.clicked.connect(
                    partial(
                        send_edited_data_to_arches,
                        operation_type="append",
                        dialog=dlg_resource_confirmation,
                    )
                )
                dlg_resource_confirmation.confirmDialogCancel.disconnect()
                dlg_resource_confirmation.confirmDialogCancel.clicked.connect(
                    partial(close_dialog, dialog=dlg_resource_confirmation)
                )
                # Show confirmation
                dlg_resource_confirmation.confirmDialogConfirm.setText("Add")
                dlg_resource_confirmation.messageLabel.setText(
                    "Are you sure you want to ADD geometries?"
                )
                dlg_resource_confirmation.show()
