import requests
from datetime import datetime, timedelta

from arches_project.core.views.login import LoggedIn
from arches_project.core.views.components.qgis_messaging import show_message
from arches_project.core.views.components.spinner import triggerSpinner
from arches_project.core.views.components.login_autocomplete import (
    load_saved_credentials,
)

from arches_project.core.arches.api import arches_api

from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsTask,
    QgsMessageLog,
)

from qgis.PyQt.QtCore import QSettings
from PyQt5.QtCore import pyqtSignal


class ArchesConnection:
    """Class for Arches APIs"""

    def __init__(self, url, username, password):
        self.url = url
        self.password = password
        self.username = username

    def get_client_id(self):
        try:
            files = {
                "username": (None, self.username),
                "password": (None, self.password),
            }
            response = requests.post(f"{self.url}/auth/get_client_id", data=files)
            clientid = response.json()["clientid"]
            return clientid
        except:
            return None

    def get_user_permissions(self, arches_user_info):
        try:
            files = {
                "username": (None, self.username),
                "password": (None, self.password),
            }
            response = requests.post(f"{self.url}/auth/user_profile", data=files)
            arches_user_info["deletable_nodegroups"] = response.json()[
                "deletable_nodegroups"
            ]
            arches_user_info["editable_nodegroups"] = response.json()[
                "editable_nodegroups"
            ]
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
                "username": (None, self.username),
                "password": (None, self.password),
                "client_id": (None, clientid),
                "grant_type": (None, "password"),
            }
            response = requests.post(self.url + "/o/token/", data=files)
            arches_token = response.json()
            arches_token["formatted_url"] = self.url
            arches_token["time"] = datetime.now()
            arches_token["expires_at"] = arches_token["time"] + timedelta(
                seconds=arches_token["expires_in"]
            )

            # If the token has an error status in it then break
            if "error" in arches_token.keys():
                error_msg = arches_token["error"]
                arches_token = {}  # reset token to empty
            return arches_token

        except Exception as e:
            print(f"Failed to get OAuth token: {e}")
            return arches_token

    def get_graphs(self, arches_graphs_list, login_updates, percent_progress):
        try:
            login_updates.emit("Fetching graphs ...")
            response = requests.get(f"{self.url}/graphs/")
            graphids = [
                x["graphid"]
                for x in response.json()
                if x["graphid"] != "ff623370-fa12-11e6-b98b-6c4008b05c4c"
                and x["isresource"]
            ]
            percent_progress.emit(True, 0, 0)

            for x, graph in enumerate(graphids):
                geometry_node_data = {}
                contains_geom = False
                geom_node_count = 0

                req = requests.get(f"{self.url}/graphs/{graph}")

                if req.json()["graph"]["publication_id"]:  # if graph is published
                    login_updates.emit(f"Fetching graphs ... ({x+1}/{len(graphids)})")
                    for nodes in req.json()["graph"]["nodes"]:
                        if nodes["datatype"] == "geojson-feature-collection":
                            contains_geom = True
                            geom_node_count += 1
                            nodegroupid = nodes["nodegroup_id"]
                            nodeid = nodes["nodeid"]
                            node_name = nodes["name"]
                            geometry_node_data[nodeid] = {
                                "nodegroup_id": nodegroupid,
                                "name": node_name,
                            }
                    if contains_geom == True:
                        if geom_node_count > 1:
                            multiple = True
                        else:
                            multiple = False

                        arches_graphs_list.append(
                            {
                                "graph_id": graph,
                                "name": req.json()["graph"]["name"],
                                "geometry_node_data": geometry_node_data,
                                "multiple_geometry_nodes": multiple,
                            }
                        )
                    percent_progress.emit(False, x + 1, len(graphids))
        except:
            pass
        return arches_graphs_list

    def connection_reset(self, hard_reset, dlg, iface, manual_logout=False):
        """
        Reset Arches connection
        """
        # TODO: This is all UI related, so should be moved into views/
        if hard_reset == True:
            # Reset connection inputs
            dlg.archesServerInput.setText("")
            dlg.usernameInput.setText("")
            dlg.passwordInput.setText("")
            # Reset logged in values
            dlg.displayFullNameLabel.setText("")
            dlg.displayConnectionInfoLabel.setText("")
            dlg.displayUsernameLabel.setText("")
            # Replace login tab with logged in tab
            dlg.tabWidget.setTabVisible(0, True)
            dlg.tabWidget.setTabVisible(1, False)
            dlg.tabWidget.setCurrentIndex(0)

        # Reset stored data
        arches_api.arches_user_info = {}
        arches_api.arches_connection_cache = {}
        arches_api.arches_token = {}
        arches_api.arches_graphs_list = []
        # Reset Create Resource tab as no longer useable
        dlg.createResModelSelectCombo.setEnabled(False)
        dlg.createResGeomSelectCombo.setEnabled(False)
        dlg.createResButton.setEnabled(False)
        dlg.createResOutputBoxLabel.setText("")
        dlg.createResOutputBoxFrame.hide()
        ## Set "Edit Resource" to false to begin with
        dlg.addEditRes.setEnabled(False)
        dlg.replaceEditRes.setEnabled(False)
        dlg.editResSelectFeatures.setEnabled(False)
        dlg.selectedResAttributeTable.setRowCount(0)
        dlg.selectedResAttributeTable.setEnabled(False)
        dlg.selectedResUUID.setText(
            "Connect to your Arches instance to edit resources."
        )
        # Hide multiple nodegroup dropdown
        dlg.createResNodeSelectCombo.setEnabled(False)
        # Reload saved credentials for the autocompletes
        load_saved_credentials(dlg)

        if manual_logout:
            show_message(
                iface,
                "information",
                "Logged out of Arches instance. Please reconnect to use the plugin.",
            )

    def store_auto_complete_credentials(self):

        saved_urls = QSettings().value("urls", [])
        saved_usernames = QSettings().value("usernames", [])

        if self.url not in saved_urls:
            saved_urls.append(self.url)

            if len(saved_urls) > 5:
                del saved_urls[0]

            QSettings().setValue("urls", saved_urls)

        if self.username not in saved_usernames:
            saved_usernames.append(self.username)

            if len(saved_usernames) > 5:
                del saved_usernames[0]

            QSettings().setValue("usernames", saved_usernames)


class ConnectionProcess(QgsTask):
    """Connecting to Arches via QGIS task and updating the UI"""

    login_updates = pyqtSignal(str)
    percent_progress = pyqtSignal(bool, int, int)
    complete = pyqtSignal()

    def __init__(self, url, username, password, dlg, iface, plugin_dir):
        super().__init__()
        self.url = url
        self.password = password
        self.username = username
        self.dlg = dlg
        self.iface = iface
        self.plugin_dir = plugin_dir

    def run(self):
        self.arches_connection = ArchesConnection(
            url=self.url, username=self.username, password=self.password
        )

        self.login_updates.emit("Fetching client id ...")
        arches_api.client_id = self.arches_connection.get_client_id()
        self.percent_progress.emit(True, 0, 0)
        if not arches_api.client_id:
            return False

        # get/update user info on the logged in user
        arches_api.arches_user_info = {}
        self.login_updates.emit("Fetching user permissions ...")
        arches_api.arches_user_info = self.arches_connection.get_user_permissions(
            arches_api.arches_user_info
        )
        self.percent_progress.emit(True, 0, 0)

        # re-fetch graphs before checking cache as updates may have occurred
        arches_api.arches_graphs_list = []

        if 2 not in arches_api.arches_user_info["groups"]:
            # if user does not have permissions return early and deal with in finished()
            return True

        arches_api.arches_graphs_list = self.arches_connection.get_graphs(
            arches_api.arches_graphs_list,
            self.login_updates,
            self.percent_progress,
        )

        arches_api.arches_token = self.arches_connection.get_token(
            arches_api.client_id, arches_api.arches_token
        )

        self.login_updates.emit("Fetching Oauth token ...")
        if not arches_api.arches_token:
            return False
        self.percent_progress.emit(True, 0, 0)

        # Store for preventing duplicate connection requests
        arches_api.arches_connection_cache = {
            "url": self.dlg.archesServerInput.text(),
            "username": self.dlg.usernameInput.text(),
        }

        return True

    def finished(self, result):

        def update_login_tab():
            # Replace login tab with logged in tab
            self.dlg.tabWidget.setTabVisible(0, False)
            self.dlg.tabWidget.setTabVisible(1, True)
            self.dlg.tabWidget.setCurrentIndex(1)

            logged_in_tab = LoggedIn(
                dlg=self.dlg,
                username=self.username,
                url=self.url,
                arches_user_info=arches_api.arches_user_info,
            )
            logged_in_tab.update_logged_in_view()
            # self.dlg.displayTextLabel.setText(f"Connected to {self.url} as {self.dlg.usernameInput.text()}.")
            # self.dlg.displayUrlLabel.setOpenExternalLinks(True) #TODO

        def update_create_resources_tab():
            self.dlg.createResModelSelectCombo.clear()
            self.dlg.createResGeomSelectCombo.setEnabled(True)
            self.dlg.createResGeomSelectCombo.clear()
            self.dlg.createResGeomSelectCombo.addItems(
                [layer.name() for layer in arches_api.layers]
            )

            if arches_api.arches_graphs_list:
                self.dlg.createResModelSelectCombo.setEnabled(True)
                self.dlg.createResModelSelectCombo.addItems(
                    [graph["name"] for graph in arches_api.arches_graphs_list]
                )
                self.dlg.createResButton.setEnabled(True)

        def update_edit_resources_tab():
            self.dlg.addEditRes.setEnabled(False)
            self.dlg.replaceEditRes.setEnabled(False)
            if arches_api.arches_selected_resource["resourceinstanceid"]:
                self.dlg.addEditRes.setEnabled(True)
                self.dlg.replaceEditRes.setEnabled(True)
            self.dlg.editResSelectFeatures.setEnabled(True)
            self.dlg.editResSelectFeatures.clear()
            self.dlg.editResSelectFeatures.addItems(
                [layer.name() for layer in arches_api.layers]
            )
            self.dlg.selectedResAttributeTable.setEnabled(True)
            self.dlg.selectedResUUID.setText(
                "Connected to Arches. Select an Arches resource to proceed."
            )

        triggerSpinner(dlg=self.dlg, plugin_dir=self.plugin_dir).hide_spinner()

        if result:
            if 2 in arches_api.arches_user_info["groups"]:
                # THIS IS THE RESOURCE EDITOR PERMISSION
                # This must be in result, in order to display that login failed due to permissions rather than other

                # get all vector layers
                arches_api.layers = [
                    l
                    for l in QgsProject.instance().mapLayers().values()
                    if l.type() == QgsVectorLayer.VectorLayer
                    if str(l.dataProvider().name()) != "postgres"
                ]

                self.arches_connection.store_auto_complete_credentials()
                update_login_tab()
                update_edit_resources_tab()
                update_create_resources_tab()
            else:
                ArchesConnection(None, None, None).connection_reset(
                    hard_reset=True, dlg=self.dlg, iface=self.iface
                )
                show_message(
                    self.iface,
                    "Warning",
                    "Login prevented: This user does not have the permissions to create Arches resources.",
                    duration=-1,
                )
                self.dlg.loginErrorMessageFrame.show()
                self.dlg.loginErrorMessageLabel.show()
                self.dlg.loginErrorMessageLabel.setText(
                    "Login prevented: This user does not have the permissions to create Arches resources."
                )
        else:
            show_message(
                self.iface,
                "Error",
                "Failed to connect to Arches instance.",
                duration=-1,
            )
            self.dlg.loginErrorMessageFrame.show()
            self.dlg.loginErrorMessageLabel.show()
            self.dlg.loginErrorMessageLabel.setText(
                "Failed to connect to Arches instance."
            )
            ArchesConnection(None, None, None).connection_reset(
                hard_reset=True, dlg=self.dlg, iface=self.iface
            )

    def cancel(self):
        triggerSpinner(dlg=self.dlg, plugin_dir=self.plugin_dir).hide_spinner()
        QgsMessageLog.logMessage("task was canceled")
        super().cancel()
