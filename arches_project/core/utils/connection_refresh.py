from arches_project.core.arches.connection import ArchesConnection
from arches_project.core.arches.api import arches_api
from arches_project.core.views.components.dialog_updates import (
    update_refresh_confirm_label,
    update_create_resources_tab,
    connection_reset,
    update_edit_resources_tab,
)
from arches_project.core.views.components.qgis_messaging import show_message
import requests


def connection_refresh(dlg, iface):
    """
    Simple function to fix any possible user input errors.
    Strips any leading/trailing whitespace and a trailing slash.
    """
    url = arches_api.arches_token["formatted_url"]
    arches_connection = ArchesConnection(url, None, None)

    try:
        arches_api.arches_graphs_list = arches_connection.get_graphs()
        update_refresh_confirm_label(dlg=dlg, connected=True)
        update_create_resources_tab(dlg=dlg)
        update_edit_resources_tab(dlg=dlg)
    except requests.exceptions.RequestException:
        update_refresh_confirm_label(dlg=dlg, connected=False)
        connection_reset(hard_reset=False, dlg=dlg, iface=iface, manual_logout=False)
        show_message(
            iface,
            "Error",
            "Failed to reconnect to Arches instance.",
            duration=-1,
        )
