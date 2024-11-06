from ..utils.geometry_conversion import geometry_conversion

import requests

class ArchesResources:
    def __init__(self, nodeid, tileid, arches_token, layers, arches_graphs_list, geometry_nodes, arches_user_info):
        ## Should probably just pass self into this rather than each var
        self.nodeid = nodeid
        self.tileid = tileid
        self.arches_token = arches_token
        self.layers = layers
        self.arches_graphs_list = arches_graphs_list
        self.geometry_nodes = geometry_nodes
        self.arches_user_info = arches_user_info



    def save_to_arches(self, tileid, nodeid, geometry_collection, geometry_format, arches_operation):
        """
        Save data to arches resource
        """
        if self.arches_token:
            try:
                files = {
                    'tileid': (None, tileid),
                    'nodeid': (None, nodeid),
                    'data': (None, geometry_collection),
                    'format': (None, geometry_format),
                    'operation': (None, arches_operation),
                }
                headers = {"Authorization": "Bearer %s" % (self.arches_token["access_token"])}
                response = requests.post("%s/api/node_value/" % (self.arches_token["formatted_url"]), headers=headers, data=files)
                if response.ok == True:
                    arches_created_resource = {"nodegroup_id": response.json()["nodegroup_id"],
                                                "resourceinstance_id": response.json()["resourceinstance_id"],
                                                "tile_id": response.json()["tileid"]}
                    return arches_created_resource
                else:
                    print("Resource creation faiiled with response code:%s" % (response.status_code))
                    return None
            except:
                print("Cannot create new resource")
        return None



    def create_resource(self, dlg, dlg_resource_creation):
        """
        Create Resource dialog and functionality
        """

        def send_new_resource_to_arches():
            if selectedNode["nodegroup_id"] in self.arches_user_info["editable_nodegroups"]:
                try:
                    results = self.save_to_arches(tileid=self.tileid,
                                                nodeid = selectedNode["node_id"],
                                                geometry_collection=geomcoll,
                                                geometry_format=None,
                                                arches_operation="create")
                    print(results, self.arches_token)
                    dlg.createResOutputBox.setText("""Successfully created a new resource with the selected geometry.
                                                        \nTo continue the creation of your new resource, navigate to...\n%s/resource/%s""" % 
                                                    (self.arches_token["formatted_url"], results["resourceinstance_id"]))
                    dlg_resource_creation.close()
                except:
                    dlg.createResOutputBox.setText("Resource creation FAILED.")
                    dlg_resource_creation.close()
            else:
                dlg.createResOutputBox.setText("This user does not have permission to create data for the geometry nodegroup in this resource model. An Arches resource has not been created.")
                dlg_resource_creation.close()

        def close_dialog():
            dlg_resource_creation.close()

        # Get info on current layer and selected graph
        selectedLayerIndex = dlg.createResFeatureSelect.currentIndex()
        selectedLayer = self.layers[selectedLayerIndex]
        selectedGraphIndex = dlg.createResModelSelect.currentIndex()
        selectedGraph = self.arches_graphs_list[selectedGraphIndex]

        if selectedGraph["multiple_geometry_nodes"] == True:
            selectedNodeIndex = dlg.geometryNodeSelect.currentIndex()
            selectedNode = self.geometry_nodes[selectedNodeIndex]

        elif selectedGraph["multiple_geometry_nodes"] == False:
            node_id = list(selectedGraph["geometry_node_data"].keys())[0]
            nodegroup_id = selectedGraph["geometry_node_data"][node_id]["nodegroup_id"]
            selectedNode = {"node_id": node_id, "nodegroup_id": nodegroup_id, "name": selectedGraph["geometry_node_data"][node_id]["name"]}

        geomcoll, geometry_type_dict = geometry_conversion(selectedLayer)
     
        # Format text box
        dlg_resource_creation.infoText.viewport().setAutoFillBackground(False) # Sets the text box to be invisible
        dlg_resource_creation.infoText.setText("")
        dlg_resource_creation.infoText.append("An Arches resource will be created with the following geometries:\n")
        for k,v in geometry_type_dict.items():
            dlg_resource_creation.infoText.append(f"{k}: {v}")

        # open dialog
        dlg_resource_creation.show()

        # Push button responses    
        dlg_resource_creation.createDialogCreate.clicked.connect(send_new_resource_to_arches)
        dlg_resource_creation.createDialogCancel.clicked.connect(close_dialog)



    def edit_resource(self, 
                      replace, 
                      arches_selected_resource,
                      dlg, 
                      dlg_edit_resource_replace, 
                      dlg_edit_resource_add):
        """
        Save geometries to existing resource - either replace or add
        """

        def send_edited_data_to_arches(operation_type, dialog):
            if nodegroup_value in self.arches_user_info["editable_nodegroups"]:
                try:
                    results = self.save_to_arches(tileid=self.tileid,
                                                    nodeid = self.nodeid,
                                                    geometry_collection=geomcoll,
                                                    geometry_format=None,
                                                    arches_operation=operation_type)
                    dialog.close()
                except:
                    print(f"Couldn't {operation_type} geometry in resource")
                    dialog.close()
            else:
                print("This user does not have permission to update data for the geometry nodegroup in this resource model.")
                dialog.close()

        def close_dialog(dialog):
            dialog.close()


        if arches_selected_resource:
            selectedLayerIndex = dlg.editResSelectFeatures.currentIndex()
            selectedLayer = self.layers[selectedLayerIndex]

            geomcoll, geometry_type_dict = geometry_conversion(selectedLayer)

            # Get nodegroup from graph
            for graph in self.arches_graphs_list:
                for k,v in graph["geometry_node_data"].items():
                    if k == arches_selected_resource["nodeid"]:
                        nodegroup_value = v["nodegroup_id"]
                        break

            # Replace geometry
            if replace == True:
                # Format text box
                dlg_edit_resource_replace.infoText.viewport().setAutoFillBackground(False) # Sets the text box to be invisible
                dlg_edit_resource_replace.infoText.setText("")
                dlg_edit_resource_replace.infoText.append("The following geometries will be replace the existing Arches resource's geometries:\n")
                for k,v in geometry_type_dict.items():
                    dlg_edit_resource_replace.infoText.append(f"{k}: {v}")

                dlg_edit_resource_replace.editDialogCreate.disconnect()
                dlg_edit_resource_replace.editDialogCreate.clicked.connect(lambda: send_edited_data_to_arches(operation_type="create",
                                                                                        dialog=dlg_edit_resource_replace))
                dlg_edit_resource_replace.editDialogCancel.disconnect()
                dlg_edit_resource_replace.editDialogCancel.clicked.connect(lambda: close_dialog(dialog=dlg_edit_resource_replace))
                # Show confirmation dialog
                dlg_edit_resource_replace.show()

            # Add geometry to the resource
            else:
                # Format text box
                dlg_edit_resource_add.infoText.viewport().setAutoFillBackground(False) # Sets the text box to be invisible
                dlg_edit_resource_add.infoText.setText("")
                dlg_edit_resource_add.infoText.append("The following geometries will be added to the Arches resource:\n")
                for k,v in geometry_type_dict.items():
                    dlg_edit_resource_add.infoText.append(f"{k}: {v}")

                dlg_edit_resource_add.editDialogCreate.disconnect()
                dlg_edit_resource_add.editDialogCreate.clicked.connect(lambda: send_edited_data_to_arches(operation_type="append",
                                                                                    dialog=dlg_edit_resource_add))
                dlg_edit_resource_add.editDialogCancel.disconnect()
                dlg_edit_resource_add.editDialogCancel.clicked.connect(lambda: close_dialog(dialog=dlg_edit_resource_add))
                # Show confirmation dialog
                dlg_edit_resource_add.show()
