from functools import partial
import json

from PyQt5.QtCore import pyqtSlot, QObject, pyqtSignal
from arches_project.core.views.components.qgis_messaging import show_message
from arches_project.core.views.components.spinner import triggerSpinner
from arches_project.core.views.components.dialog_updates import connection_reset
from arches_project.core.views.components.dialog_updates import (
    update_create_resources_tab,
)
from arches_project.core.views.components.dialog_updates import (
    update_edit_resources_tab,
)
from arches_project.core.views.components.dialog_updates import update_login_tab

from arches_project.core.arches.api import arches_api
from arches_project.core.utils.network import ArchesRequester

from qgis.core import (
    Qgis,
    QgsApplication,
    QgsMessageLog,
)


class ArchesConnection(QObject):
    """Class for Arches APIs"""

    retrieved_permissions = pyqtSignal(dict)
    finished_graphs = pyqtSignal(str)

    def __init__(self, config_id, parent=None):
        super().__init__(parent)
        self.config_id = config_id

        self.requester = ArchesRequester()
        self._total_graphs = 0
        self.setParent(QgsApplication.instance())

    @pyqtSlot(dict)
    def _process_user_permissions(self, arches_user_info, response_data):

        QgsMessageLog.logMessage(
            f"Processing User Permissions: " + str(response_data),
            "Arches Plugin",
            level=Qgis.Info,
        )
        data = json.loads(response_data)
        QgsMessageLog.logMessage(
            f"Processing User Permissions: " + str(data),
            "Arches Plugin",
            level=Qgis.Info,
        )

        try:
            arches_user_info["deletable_nodegroups"] = data["deletable_nodegroups"]
            arches_user_info["editable_nodegroups"] = data["editable_nodegroups"]
            arches_user_info["groups"] = data["groups"]
            arches_user_info["is_active"] = data["is_active"]
            arches_user_info["date_joined"] = data["date_joined"]
            arches_user_info["first_name"] = data["first_name"]
            arches_user_info["last_name"] = data["last_name"]
            arches_user_info["username"] = data["username"]
        except:
            arches_user_info["deletable_nodegroups"] = None
            arches_user_info["editable_nodegroups"] = None
            arches_user_info["is_active"] = None
            arches_user_info["groups"] = []
            arches_user_info["date_joined"] = None
            arches_user_info["first_name"] = None
            arches_user_info["last_name"] = None

        self.retrieved_permissions.emit(data)

    def get_user_permissions(self, arches_user_info):
        QgsMessageLog.logMessage(
            f"Getting Permissions",
            "Arches Plugin",
            level=Qgis.Info,
        )
        user_permissions_processor = partial(
            self._process_user_permissions, arches_user_info
        )
        self._user_permissions_processor = user_permissions_processor
        requester = ArchesRequester()
        requester.complete_signal.connect(self._user_permissions_processor)
        requester.make_authenticated_request(
            "/auth/user_profile", self.config_id, method="POST"
        )

    def _process_get_graphs(
        self, arches_graphs_list, login_updates, percent_progress, response_data
    ):
        data = json.loads(response_data)
        QgsMessageLog.logMessage(
            f"here's the data {str(data)}",
            "Arches Plugin",
            level=Qgis.Info,
        )

        graphids = [
            x["graphid"]
            for x in data
            if x["graphid"] != "ff623370-fa12-11e6-b98b-6c4008b05c4c"
            and x["isresource"]
        ]
        percent_progress.emit(True, 0, 0)
        # if self._graph_processor:
        #     self.requester.complete_signal.disconnect(self._graph_processor)a

        self._requesters = []
        self._total_graphs = len(graphids)
        for x, graph in enumerate(graphids):
            login_updates.emit(f"Fetching graphs ... ({x+1}/{len(graphids)})")
            graph_processor = partial(
                self._process_get_graph,
                arches_graphs_list,
                graph,
                x,
                percent_progress,
                len(graphids),
            )
            requester = ArchesRequester()
            requester.complete_signal.connect(graph_processor)
            requester.make_authenticated_request(f"/graphs/{graph}", self.config_id)

            self._requesters.append(requester)

    def _process_get_graph(
        self,
        arches_graphs_list,
        graph_id,
        index,
        percent_progress,
        total_graphs,
        response_data,
    ):
        QgsMessageLog.logMessage(
            f"Processing Graph {graph_id}",
            "Arches Plugin",
            level=Qgis.Info,
        )
        data = json.loads(response_data)
        geometry_node_data = {}
        contains_geom = False
        geom_node_count = 0
        if data["graph"]["publication_id"]:  # if graph is published
            for nodes in data["graph"]["nodes"]:
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
                        "graph_id": graph_id,
                        "name": data["graph"]["name"],
                        "geometry_node_data": geometry_node_data,
                        "multiple_geometry_nodes": multiple,
                    }
                )
        self._total_graphs -= 1
        if self._total_graphs == 0:
            self.finished_graphs.emit("Finished")

        percent_progress.emit(False, total_graphs - self._total_graphs, total_graphs)

    def get_graphs(self, arches_graphs_list, login_updates, percent_progress):
        login_updates.emit("Fetching graphs ...")
        _graph_processor = partial(
            self._process_get_graphs,
            arches_graphs_list,
            login_updates,
            percent_progress,
        )
        requester = ArchesRequester()
        requester.complete_signal.connect(_graph_processor)
        requester.make_authenticated_request(f"/graphs/", self.config_id)


class ConnectionProcess(QObject):
    """Connecting to Arches via QGIS task and updating the UI"""

    login_updates = pyqtSignal(str)
    percent_progress = pyqtSignal(bool, int, int)
    complete = pyqtSignal()

    def __init__(self, config_id, dlg, iface, plugin_dir):
        super().__init__()
        self.config_id = config_id
        self.dlg = dlg
        self.iface = iface
        self.plugin_dir = plugin_dir

    def _after_permissions_returned(self, payload):
        QgsMessageLog.logMessage(
            f"Processing permissions...",
            "Arches Plugin",
            level=Qgis.Info,
        )

        # re-fetch graphs before checking cache as updates may have occurred
        arches_api.arches_graphs_list = []
        arches_api.config_id = self.config_id

        if 2 not in arches_api.arches_user_info["groups"]:
            # if user does not have permissions return early and deal with in finished()
            return True

        self.arches_connection.finished_graphs.connect(self.finished)

        self.arches_connection.get_graphs(
            arches_api.arches_graphs_list,
            self.login_updates,
            self.percent_progress,
        )

        self.percent_progress.emit(True, 0, 0)

    def run(self):
        QgsMessageLog.logMessage(
            f"Connecting to Arches...",
            "Arches Plugin",
            level=Qgis.Info,
        )
        self.arches_connection = ArchesConnection(config_id=self.config_id)
        self.percent_progress.emit(True, 0, 0)

        # get/update user info on the logged in user
        arches_api.arches_user_info = {}
        self.login_updates.emit("Fetching user permissions ...")
        QgsMessageLog.logMessage(
            f"Fetching user permissions...",
            "Arches Plugin",
            level=Qgis.Info,
        )

        self.arches_connection.get_user_permissions(arches_api.arches_user_info)
        QgsMessageLog.logMessage(
            f"Fetching permissions completed...",
            "Arches Plugin",
            level=Qgis.Info,
        )

        self.arches_connection.retrieved_permissions.connect(
            self._after_permissions_returned
        )

    def finished(self, result):
        QgsMessageLog.logMessage(
            f"In finished() {result}...",
            "Arches Plugin",
            level=Qgis.Info,
        )

        triggerSpinner(dlg=self.dlg, plugin_dir=self.plugin_dir).hide_spinner()

        if result:
            if 2 in arches_api.arches_user_info["groups"]:
                # THIS IS THE RESOURCE EDITOR PERMISSION
                # This must be in result, in order to display that login failed due to permissions rather than other

                update_edit_resources_tab(dlg=self.dlg)
                update_create_resources_tab(dlg=self.dlg)
            else:
                connection_reset(hard_reset=True, dlg=self.dlg, iface=self.iface)
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
            connection_reset(hard_reset=True, dlg=self.dlg, iface=self.iface)
