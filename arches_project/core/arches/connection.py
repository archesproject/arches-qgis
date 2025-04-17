import requests
from datetime import datetime
import os
from ..utils.qgis_messaging import show_message

from qgis.core import (QgsProject, 
                       QgsVectorLayer,
                       QgsApplication, 
                       QgsTask, 
                       QgsMessageLog, 
                       Qgis
                       )
from ..utils.spinner import triggerSpinner

class ArchesConnection():
    """ Class for Arches APIs """
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
                         self_obj,
                         manual_logout=False):
        """
        Reset Arches connection
        """
        if hard_reset == True:
            # Reset connection inputs
            self_obj.dlg.archesServerInput.setText("")
            self_obj.dlg.usernameInput.setText("")
            self_obj.dlg.passwordInput.setText("")
            self_obj.dlg.displayUser.setText("")
            self_obj.dlg.displayArchesURL.setText("")
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

        if manual_logout:
            show_message(self_obj.iface, "information", "Logged out of Arches instance. Please reconnect to use the plugin.")

class ConnectionProcess(QgsTask):
    """ Connecting to Arches via QGIS task and updating the UI """
    def __init__(self, url, username, password, arch_obj):
        super().__init__()
        self.url = url
        self.password = password
        self.username = username
        self.arch_obj = arch_obj

    def run(self):
        arches_connection = ArchesConnection(url=self.url,
                                            username=self.username,
                                            password=self.password)

        clientid = arches_connection.get_client_id()
        
        if not clientid:
            return False
        
        # If client id NOT None then connection has been made
        # check cache first before firing connection again

        # get/update user info on the logged in user
        self.arch_obj.arches_user_info = {}

        self.arch_obj.arches_user_info = arches_connection.get_user_permissions(self.arch_obj.arches_user_info)

        # re-fetch graphs before checking cache as updates may have occurred
        self.arch_obj.arches_graphs_list = []

        self.arch_obj.arches_graphs_list = arches_connection.get_graphs(self.arch_obj.arches_graphs_list)

        if self.arch_obj.arches_connection_cache:
            # IF THE CACHE IS UNCHANGED THEN DON'T REFIRE CONNECTION
            if (self.arch_obj.dlg.archesServerInput.text() == self.arch_obj.arches_connection_cache["url"] and
                self.arch_obj.dlg.usernameInput.text() == self.arch_obj.arches_connection_cache["username"]):
                print("Connection reattempt prevented as login details remain unchanged. \nGraphs have been refetched to reflect changed made on Arches.")   
                # Re-fetch the graphs with updated list
                if self.arch_obj.arches_graphs_list:
                    self.arch_obj.dlg.createResModelSelect.clear()
                    self.arch_obj.dlg.createResModelSelect.addItems([graph["name"] for graph in self.arches_graphs_list])
                # Re-fill the comboboxes
                self.arch_obj.layers = [l for l in QgsProject.instance().mapLayers().values() if l.type() == QgsVectorLayer.VectorLayer if str(l.dataProvider().name()) != "postgres"] 
                self.arch_obj.dlg.createResFeatureSelect.clear()
                self.arch_obj.dlg.createResFeatureSelect.addItems([layer.name() for layer in self.arch_obj.layers])
                self.arch_obj.dlg.editResSelectFeatures.clear()
                self.arch_obj.dlg.editResSelectFeatures.addItems([layer.name() for layer in self.arch_obj.layers])
                return            

        self.arch_obj.arches_token = arches_connection.get_token(clientid, self.arch_obj.arches_token)

        if self.arch_obj.arches_token:
            
            # Store for preventing duplicate connection requests
            self.arch_obj.arches_connection_cache = {"url": self.arch_obj.dlg.archesServerInput.text(),
                                            "username": self.arch_obj.dlg.usernameInput.text()}
                                
            return True # return true for all, even if user doesn't have perms as this will be dealt with in finished()
        else:
            return False
            

    def finished(self, result):
        def update_login_tab():
            # Replace login tab with logged in tab
            self.arch_obj.dlg.tabWidget.setTabVisible(0, False)
            self.arch_obj.dlg.tabWidget.setTabVisible(1, True)
            self.arch_obj.dlg.tabWidget.setCurrentIndex(1)

            self.arch_obj.dlg.displayUser.setText(f"You are logged in as user: {self.arch_obj.dlg.usernameInput.text()}")
            self.arch_obj.dlg.displayArchesURL.setText(f"Visit your Arches instance: {self.url}")
            self.arch_obj.dlg.displayArchesURL.setOpenExternalLinks(True) #TODO: doesnt work

        def update_create_resources_tab():
            self.arch_obj.dlg.createResModelSelect.clear()
            self.arch_obj.dlg.createResFeatureSelect.setEnabled(True)
            self.arch_obj.dlg.createResFeatureSelect.clear()
            self.arch_obj.dlg.createResFeatureSelect.addItems([layer.name() for layer in self.arch_obj.layers])
            
            if self.arch_obj.arches_graphs_list:
                self.arch_obj.dlg.createResModelSelect.setEnabled(True)
                self.arch_obj.dlg.createResModelSelect.addItems([graph["name"] for graph in self.arch_obj.arches_graphs_list])
                self.arch_obj.dlg.addNewRes.setEnabled(True)

        def update_edit_resources_tab():
            self.arch_obj.dlg.addEditRes.setEnabled(False)
            self.arch_obj.dlg.replaceEditRes.setEnabled(False)
            if self.arch_obj.arches_selected_resource["resourceinstanceid"]:
                self.arch_obj.dlg.addEditRes.setEnabled(True)
                self.arch_obj.dlg.replaceEditRes.setEnabled(True)
            self.arch_obj.dlg.editResSelectFeatures.setEnabled(True)
            self.arch_obj.dlg.editResSelectFeatures.clear()
            self.arch_obj.dlg.editResSelectFeatures.addItems([layer.name() for layer in self.arch_obj.layers])
            self.arch_obj.dlg.selectedResAttributeTable.setEnabled(True)
            self.arch_obj.dlg.selectedResUUID.setText("Connected to Arches. Select an Arches resource to proceed.")

        triggerSpinner(arches_obj=self.arch_obj).hide_spinner()

        if result:
            if 2 in self.arch_obj.arches_user_info["groups"]:
                # THIS IS THE RESOURCE EDITOR PERMISSION

                # get all vector layers
                self.arch_obj.layers = [l for l in QgsProject.instance().mapLayers().values() if l.type() == QgsVectorLayer.VectorLayer if str(l.dataProvider().name()) != "postgres"] 

                update_login_tab()
                update_edit_resources_tab()
                update_create_resources_tab()
            else:
                ArchesConnection(None,None,None).connection_reset(hard_reset=True,
                                                                self_obj=self.arch_obj)
                show_message(self.arch_obj.iface, "Warning", "Login prevented: This user does not have the permissions to create Arches resources.")
                self.arch_obj.dlg.loginErrorMessageFrame.show()
                self.arch_obj.dlg.loginErrorMessageLabel.show()
                self.arch_obj.dlg.loginErrorMessageLabel.setText("Login prevented: This user does not have the permissions to create Arches resources.")
        else:
            show_message(self.arch_obj.iface, "Error", "Failed to connect to Arches instance." )
            self.arch_obj.dlg.loginErrorMessageFrame.show()
            self.arch_obj.dlg.loginErrorMessageLabel.show()
            self.arch_obj.dlg.loginErrorMessageLabel.setText("Failed to connect to Arches instance.")
            ArchesConnection(None,None,None).connection_reset(hard_reset=True,
                                                            self_obj=self.arch_obj)


    def cancel(self):
        triggerSpinner(arches_obj=self.arch_obj).hide_spinner()
        QgsMessageLog.logMessage('task was canceled')
        super().cancel()
