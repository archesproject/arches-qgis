from datetime import datetime
from qgis.core import QgsProject
from PyQt5.QtCore import Qt

import requests
from functools import partial

from arches_project.core.utils.geometry_conversion import Geometries
from arches_project.core.views.components.qgis_messaging import show_message
from arches_project.core.views.components.dialog_updates import (
    update_confirmation_dialog,
)
from arches_project.core.utils.refresh_token import refresh_token
from arches_project.core.arches.api import arches_api


class ArchesResources:
    def __init__(self, nodeid, tileid):
        self.nodeid = nodeid
        self.tileid = tileid

    def save_to_arches(
        self, tileid, nodeid, geometry_collection, geometry_format, arches_operation
    ):
        """
        Save data to arches resource
        """
        if arches_api.arches_token:
            try:
                files = {
                    "tileid": (None, tileid),
                    "nodeid": (None, nodeid),
                    "data": (None, geometry_collection),
                    "format": (None, geometry_format),
                    "operation": (None, arches_operation),
                }

                headers = {
                    "Authorization": "Bearer %s"
                    % (arches_api.arches_token["access_token"])
                }
                response = requests.post(
                    f"{arches_api.arches_token['formatted_url']}/api/node_value/",
                    headers=headers,
                    data=files,
                )

                if arches_api.arches_token["expires_at"] < datetime.now():
                    refresh_token()
                    headers = {
                        "Authorization": "Bearer %s"
                        % (arches_api.arches_token["access_token"])
                    }
                    response = requests.post(
                        f"{arches_api.arches_token['formatted_url']}/api/node_value/",
                        headers=headers,
                        data=files,
                    )

                if response.ok == True:
                    arches_created_resource = {
                        "nodegroup_id": response.json()["nodegroup_id"],
                        "resourceinstance_id": response.json()["resourceinstance_id"],
                        "tile_id": response.json()["tileid"],
                    }
                    return arches_created_resource

                else:
                    print(
                        "Resource creation failed with response code:%s"
                        % (response.status_code)
                    )
                    return None
            except Exception as e:
                print(f"Cannot create new resource: {e}")
        return None

    def create_resource(self, dlg, dlg_resource_confirmation, iface):
        """
        Create Resource dialog and functionality
        """

        def send_new_resource_to_arches():
            if (
                selectedNode["nodegroup_id"]
                in arches_api.arches_user_info["editable_nodegroups"]
            ):
                try:
                    results = self.save_to_arches(
                        tileid=self.tileid,
                        nodeid=selectedNode["node_id"],
                        geometry_collection=geomcoll,
                        geometry_format=None,
                        arches_operation="create",
                    )
                    dlg.createResOutputBoxFrame.show()
                    created_resource_url = f"{arches_api.arches_token['formatted_url']}/resource/{results['resourceinstance_id']}"
                    dlg.createResOutputBoxLabel.setText(
                        f'Successfully created a new resource with the selected geometry.<br>To continue the creation of your new resource, navigate to...<br><a href="{created_resource_url}">{created_resource_url}</a>'
                    )
                    show_message(
                        iface, "Success", "A new Arches resource has been created."
                    )
                    dlg_resource_confirmation.close()
                except:
                    dlg.createResOutputBoxFrame.show()
                    dlg.createResOutputBoxLabel.setText("Resource creation FAILED.")
                    show_message(
                        iface, "Error", "Resource creation failed.", duration=-1
                    )
                    dlg_resource_confirmation.close()
            else:
                dlg.createResOutputBoxFrame.show()
                dlg.createResOutputBoxLabel.setText(
                    "This user does not have permission to create data for the geometry nodegroup in this resource model. An Arches resource has not been created."
                )
                show_message(
                    iface,
                    "Error",
                    "The user does not have permission to create data.",
                    duration=-1,
                )
                dlg_resource_confirmation.close()

        # Get info on current layer and selected graph
        selectedLayerIndex = dlg.createResGeomSelectCombo.currentIndex()
        selectedLayer = arches_api.layers[selectedLayerIndex]
        selectedGraphIndex = dlg.createResModelSelectCombo.currentIndex()
        selectedGraph = arches_api.arches_graphs_list[selectedGraphIndex]

        if selectedGraph["multiple_geometry_nodes"] == True:
            selectedNodeIndex = dlg.createResNodeSelectCombo.currentIndex()
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

        basemap = QgsProject.instance().mapLayersByName("OpenStreetMap")[0]
        snapshot_image = geom_convert.geometry_snapshot(basemap)

        update_confirmation_dialog(
            dlg_resource_confirmation,
            geometry_type_dict,
            snapshot_image,
            "create",
            send_new_resource_to_arches,
        )

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
                    results = self.save_to_arches(
                        tileid=self.tileid,
                        nodeid=self.nodeid,
                        geometry_collection=geomcoll,
                        geometry_format=None,
                        arches_operation=operation_type,
                    )
                    dlg.editResOutputBoxFrame.show()
                    edited_resource_url = f"{arches_api.arches_token['formatted_url']}/resource/{results['resourceinstance_id']}"
                    dlg.editResOutputBoxLabel.setText(
                        f'Successfully edited the selected resource with the selected geometry.<br>To continue editing the resource navigate to...<br><a href="{edited_resource_url}">{edited_resource_url}</a>'
                    )
                    show_message(
                        iface,
                        "Success",
                        f"Resource geometry {operation_type} was successful.",
                    )
                    dialog.close()
                except:
                    dlg.editResOutputBoxFrame.show()
                    dlg.editResOutputBoxLabel.setText(
                        f"Couldn't {operation_type} geometry in resource"
                    )
                    show_message(
                        iface,
                        "error",
                        f"Couldn't {operation_type} geometry in resource",
                        duration=-1,
                    )
                    dialog.close()
            else:
                dlg.editResOutputBoxFrame.show()
                dlg.editResOutputBoxLabel.setText(
                    "This user does not have permission to update data for the geometry nodegroup in this resource model."
                )
                show_message(
                    iface,
                    "error",
                    "This user does not have permission to update data for the geometry nodegroup in this resource model",
                    duration=-1,
                )
                dialog.close()

        if arches_api.arches_selected_resource:
            selectedLayerIndex = dlg.editResGeomSelectCombo.currentIndex()
            selectedLayer = arches_api.layers[selectedLayerIndex]

            geom_convert = Geometries(selectedLayer)
            geomcoll, geometry_type_dict = geom_convert.geometry_conversion()

            basemap = QgsProject.instance().mapLayersByName("OpenStreetMap")[0]
            snapshot_image = geom_convert.geometry_snapshot(basemap)

            # Get nodegroup from graph
            for graph in arches_api.arches_graphs_list:
                for k, v in graph["geometry_node_data"].items():
                    if k == arches_api.arches_selected_resource["nodeid"]:
                        nodegroup_value = v["nodegroup_id"]
                        break

            # Replace geometry
            operation_type = "replace" if replace else "append"

            update_confirmation_dialog(
                dlg_resource_confirmation,
                geometry_type_dict,
                snapshot_image,
                operation_type,
                send_edited_data_to_arches,
            )
