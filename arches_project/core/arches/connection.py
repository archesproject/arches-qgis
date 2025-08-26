import requests
from datetime import datetime
import os
from ..views.logged_in import LoggedIn
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
            arches_user_info["date_joined"] = response.json()["date_joined"]
            arches_user_info["first_name"] = response.json()["first_name"]
            arches_user_info["last_name"] = response.json()["last_name"]
        except:
            arches_user_info["deletable_nodegroups"] = None
            arches_user_info["editable_nodegroups"] = None
            arches_user_info["is_active"] = None
            arches_user_info["groups"] = []
            arches_user_info["date_joined"] = None
            arches_user_info["first_name"] = None
            arches_user_info["last_name"] = None
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
            return arches_token
        except:
            return arches_token


    def get_graphs(self, arches_graphs_list):
        try:
            response = requests.get(f"{self.url}/graphs/")
            graphids = [x["graphid"] for x in response.json() if x["graphid"] != "ff623370-fa12-11e6-b98b-6c4008b05c4c" and x["isresource"]]

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
            # Reset logged in values
            self_obj.dlg.displayFullNameLabel.setText("")
            self_obj.dlg.displayConnectionInfoLabel.setText("")
            self_obj.dlg.displayUsernameLabel.setText("")
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
        self_obj.dlg.createResButton.setEnabled(False)
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
    def __init__(self, url, username, password, archesproject):
        super().__init__()
        self.url = url
        self.password = password
        self.username = username
        self.archesproject = archesproject

    def run(self):
        arches_connection = ArchesConnection(url=self.url,
                                            username=self.username,
                                            password=self.password)

        clientid = arches_connection.get_client_id()
        
        if not clientid:
            return False
        
        # get/update user info on the logged in user
        self.archesproject.arches_user_info = {}

        self.archesproject.arches_user_info = arches_connection.get_user_permissions(self.archesproject.arches_user_info)

        # re-fetch graphs before checking cache as updates may have occurred
        self.archesproject.arches_graphs_list = []

        self.archesproject.arches_graphs_list = arches_connection.get_graphs(self.archesproject.arches_graphs_list)

        self.archesproject.arches_token = arches_connection.get_token(clientid, self.archesproject.arches_token)

        if not self.archesproject.arches_token:
            return False

        # Store for preventing duplicate connection requests
        self.archesproject.arches_connection_cache = {"url": self.archesproject.dlg.archesServerInput.text(),
                                        "username": self.archesproject.dlg.usernameInput.text()}
                            
        return True # return true for all, even if user doesn't have perms as this will be dealt with in finished()
            

    def finished(self, result):
        def update_login_tab():
            # Replace login tab with logged in tab
            self.archesproject.dlg.tabWidget.setTabVisible(0, False)
            self.archesproject.dlg.tabWidget.setTabVisible(1, True)
            self.archesproject.dlg.tabWidget.setCurrentIndex(1)

            logged_in_tab = LoggedIn(dlg = self.archesproject.dlg,
                                     username = self.username,
                                     url = self.url,
                                     arches_user_info = self.archesproject.arches_user_info)
            logged_in_tab.update_logged_in_view()
            # self.archesproject.dlg.displayTextLabel.setText(f"Connected to {self.url} as {self.archesproject.dlg.usernameInput.text()}.")
            # self.archesproject.dlg.displayUrlLabel.setOpenExternalLinks(True) #TODO

        def update_create_resources_tab():
            self.archesproject.dlg.createResModelSelect.clear()
            self.archesproject.dlg.createResFeatureSelect.setEnabled(True)
            self.archesproject.dlg.createResFeatureSelect.clear()
            self.archesproject.dlg.createResFeatureSelect.addItems([layer.name() for layer in self.archesproject.layers])
            
            if self.archesproject.arches_graphs_list:
                self.archesproject.dlg.createResModelSelect.setEnabled(True)
                self.archesproject.dlg.createResModelSelect.addItems([graph["name"] for graph in self.archesproject.arches_graphs_list])
                self.archesproject.dlg.createResButton.setEnabled(True)

        def update_edit_resources_tab():
            self.archesproject.dlg.addEditRes.setEnabled(False)
            self.archesproject.dlg.replaceEditRes.setEnabled(False)
            if self.archesproject.arches_selected_resource["resourceinstanceid"]:
                self.archesproject.dlg.addEditRes.setEnabled(True)
                self.archesproject.dlg.replaceEditRes.setEnabled(True)
            self.archesproject.dlg.editResSelectFeatures.setEnabled(True)
            self.archesproject.dlg.editResSelectFeatures.clear()
            self.archesproject.dlg.editResSelectFeatures.addItems([layer.name() for layer in self.archesproject.layers])
            self.archesproject.dlg.selectedResAttributeTable.setEnabled(True)
            self.archesproject.dlg.selectedResUUID.setText("Connected to Arches. Select an Arches resource to proceed.")

        triggerSpinner(arches_obj=self.archesproject).hide_spinner()

        if result:
            if 2 in self.archesproject.arches_user_info["groups"]:
                # THIS IS THE RESOURCE EDITOR PERMISSION

                # get all vector layers
                self.archesproject.layers = [l for l in QgsProject.instance().mapLayers().values() if l.type() == QgsVectorLayer.VectorLayer if str(l.dataProvider().name()) != "postgres"] 

                update_login_tab()
                update_edit_resources_tab()
                update_create_resources_tab()
            else:
                ArchesConnection(None,None,None).connection_reset(hard_reset=True,
                                                                self_obj=self.archesproject)
                show_message(self.archesproject.iface, "Warning", "Login prevented: This user does not have the permissions to create Arches resources.", duration=-1)
                self.archesproject.dlg.loginErrorMessageFrame.show()
                self.archesproject.dlg.loginErrorMessageLabel.show()
                self.archesproject.dlg.loginErrorMessageLabel.setText("Login prevented: This user does not have the permissions to create Arches resources.")
        else:
            show_message(self.archesproject.iface, "Error", "Failed to connect to Arches instance." , duration=-1 )
            self.archesproject.dlg.loginErrorMessageFrame.show()
            self.archesproject.dlg.loginErrorMessageLabel.show()
            self.archesproject.dlg.loginErrorMessageLabel.setText("Failed to connect to Arches instance.")
            ArchesConnection(None,None,None).connection_reset(hard_reset=True,
                                                            self_obj=self.archesproject)


    def cancel(self):
        triggerSpinner(arches_obj=self.archesproject).hide_spinner()
        QgsMessageLog.logMessage('task was canceled')
        super().cancel()
