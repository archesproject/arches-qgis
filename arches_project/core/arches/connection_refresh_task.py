from arches_project.core.arches.connection import ArchesConnection
from arches_project.core.arches.api import arches_api
from arches_project.core.views.components.dialog_updates import (
    update_refresh_confirm_label,
    update_create_resources_tab,
    connection_reset,
    update_edit_resources_tab,
    disable_refresh_btn,
)
from arches_project.core.views.components.qgis_messaging import show_message
import requests

from qgis.core import QgsTask
from PyQt5.QtCore import pyqtSignal


class ConnectionRefreshTask(QgsTask):

    refresh_finished = pyqtSignal()

    def __init__(self, dlg, iface):
        super().__init__()
        self.dlg = dlg
        self.iface = iface
        self.url = arches_api.arches_connection_cache["url"]
        self.plugin_dir = dlg.plugin_dir
        disable_refresh_btn(dlg)

    def run(self):
        arches_connection = ArchesConnection(self.url, None, None)

        try:
            self.graphs = arches_connection.get_graphs()
            return True
        except requests.exceptions.RequestException:
            return False

    def finished(self, result):

        if result:
            arches_api.arches_graphs_list = self.graphs
            update_refresh_confirm_label(dlg=self.dlg, connected=True)
            update_create_resources_tab(dlg=self.dlg)
            update_edit_resources_tab(dlg=self.dlg)

        else:
            update_refresh_confirm_label(dlg=self.dlg, connected=False)
            connection_reset(
                hard_reset=False, dlg=self.dlg, iface=self.iface, manual_logout=False
            )
            show_message(
                self.iface,
                "Error",
                "Failed to reconnect to Arches instance.",
                duration=-1,
            )

        self.refresh_finished.emit()
