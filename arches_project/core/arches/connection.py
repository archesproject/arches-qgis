import requests
from datetime import datetime
import os

class ArchesConnection():
    def __init__(self, url, username, password):
        self.url = url
        self.password = password
        self.username = username


    def get_client_id(self):
        try:
            files = {
                'username': (None, self.username),
                'password': (None, self.password),
            }
            response = requests.post(f"{self.url}/auth/get_client_id", data=files)
            clientid = response.json()["clientid"]
            return clientid
        except:
            # self.dlg.connection_status.setText("Failed to connect.\n- Check URL, username and password are correct.\n- Check the Arches instance is running.\n- Check the instance has a registered Oauth application.")
            return None


    def get_user_permissions(self, arches_user_info):
        try:
            files = {
                'username': (None, self.username),
                'password': (None, self.password),
            }
            response = requests.post(f"{self.url}/auth/user_profile", data=files)
            arches_user_info["deletable_nodegroups"] = response.json()["deletable_nodegroups"]
            arches_user_info["editable_nodegroups"] = response.json()["editable_nodegroups"]
            arches_user_info["groups"] = response.json()["groups"]
            arches_user_info["is_active"] = response.json()["is_active"]
        except:
            arches_user_info["deletable_nodegroups"] = None
            arches_user_info["editable_nodegroups"] = None
            arches_user_info["is_active"] = None
            arches_user_info["groups"] = []
        return arches_user_info


    def get_token(self, clientid, arches_token):
        try:
            files = {
                'username': (None, self.username),
                'password': (None, self.password),
                'client_id': (None, clientid),
                'grant_type': (None, "password")
            }
            response = requests.post(self.url+"/o/token/", data=files)
            arches_token = response.json()
            arches_token["formatted_url"] = self.url
            arches_token["time"] = str(datetime.now())

            # If the token has an error status in it then break
            if "error" in arches_token.keys():
                error_msg = arches_token["error"]
                arches_token = {} # reset token to empty
                #self.dlg.connection_status.setText(f"Error connecting to token: {error_msg}.")
            return arches_token
        except:
            #self.dlg.connection_status.setText("Can't get Arches oauth2 token.")
            return arches_token


    def get_graphs(self, arches_graphs_list):
        try:
            response = requests.get(f"{self.url}/graphs/")
            graphids = [x["graphid"] for x in response.json() if x["graphid"] != "ff623370-fa12-11e6-b98b-6c4008b05c4c"] # sys settings

            for graph in graphids:
                geometry_node_data = {}
                contains_geom = False
                geom_node_count = 0

                req = requests.get(f"{self.url}/graphs/{graph}")

                if req.json()["graph"]["publication_id"]:   # if graph is published
                    for nodes in req.json()["graph"]["nodes"]:
                        if nodes["datatype"] == "geojson-feature-collection":
                            contains_geom = True
                            geom_node_count += 1
                            nodegroupid = nodes["nodegroup_id"]
                            nodeid = nodes["nodeid"]
                            node_name = nodes["name"]
                            geometry_node_data[nodeid] = {"nodegroup_id": nodegroupid, "name": node_name}
                    if contains_geom == True:
                        if geom_node_count > 1: multiple = True
                        else: multiple = False

                        arches_graphs_list.append({
                            "graph_id":graph,
                            "name":req.json()["graph"]["name"],
                            "geometry_node_data": geometry_node_data,
                            "multiple_geometry_nodes": multiple
                        })
        except:
            pass
        return arches_graphs_list
    

    def connection_reset(self, 
                         hard_reset, 
                         self_obj):
        """
        Reset Arches connection
        """
        if hard_reset == True:
            # Reset connection inputs
            self_obj.dlg.connection_status.setText("Logged out of Arches instance. Please reconnect to use the plugin.")
            self_obj.dlg.arches_server_input.setText("")
            self_obj.dlg.username_input.setText("")
            self_obj.dlg.password_input.setText("")
            # Replace login tab with logged in tab
            self_obj.dlg.tabWidget.setTabVisible(0, True)
            self_obj.dlg.tabWidget.setTabVisible(1, False)
            self_obj.dlg.tabWidget.setCurrentIndex(0)

        # Reset stored data
        self_obj.arches_user_info = {}
        self_obj.arches_connection_cache = {}
        self_obj.arches_token = {}
        self_obj.arches_graphs_list = []
        # Reset Create Resource tab as no longer useable
        self_obj.dlg.createResModelSelect.setEnabled(False)
        self_obj.dlg.createResFeatureSelect.setEnabled(False)
        self_obj.dlg.addNewRes.setEnabled(False)
        self_obj.dlg.createResOutputBox.setText("")
        ## Set "Edit Resource" to false to begin with
        self_obj.dlg.addEditRes.setEnabled(False)
        self_obj.dlg.replaceEditRes.setEnabled(False)
        self_obj.dlg.editResSelectFeatures.setEnabled(False)
        self_obj.dlg.selectedResAttributeTable.setRowCount(0)
        self_obj.dlg.selectedResAttributeTable.setEnabled(False)
        self_obj.dlg.selectedResUUID.setText("Connect to your Arches instance to edit resources.")
        # Hide multiple nodegroup dropdown
        self_obj.dlg.geometryNodeSelect.setEnabled(False)
