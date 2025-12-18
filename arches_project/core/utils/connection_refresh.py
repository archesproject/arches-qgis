from arches_project.core.arches.connection import ArchesConnection
from arches_project.core.arches.api import arches_api
from arches_project.core.views.components.dialog_updates import (
    update_refresh_confirm_label,
)
from arches_project.core.views.components.dialog_updates import (
    update_create_resources_tab,
)


def connection_refresh(dlg):
    """
    Simple function to fix any possible user input errors.
    Strips any leading/trailing whitespace and a trailing slash.
    """
    url = arches_api.arches_token["formatted_url"]
    arches_connection = ArchesConnection(url, None, None)

    arches_api.arches_graphs_list = arches_connection.get_graphs()
    update_create_resources_tab(dlg=dlg)
    update_refresh_confirm_label(dlg=dlg)
