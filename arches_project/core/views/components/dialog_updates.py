from arches_project.core.views.components.qgis_messaging import show_message
from arches_project.core.views.components.login_autocomplete import (
    load_saved_credentials,
)
from arches_project.core.views.login import LoggedIn

from arches_project.core.arches.api import arches_api


def connection_reset(hard_reset, dlg, iface, manual_logout=False):
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
    dlg.editResAddGeom.setEnabled(False)
    dlg.editResReplaceGeom.setEnabled(False)
    dlg.editResGeomSelectCombo.setEnabled(False)
    dlg.editResOutputBoxLabel.setText("")
    dlg.editResOutputBoxFrame.hide()
    dlg.editResSelectedResAttributeTable.setRowCount(0)
    dlg.editResSelectedResAttributeTable.setEnabled(False)
    dlg.editResSelectedResId.setText(
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


def update_login_tab(dlg, username, url):
    """
    Run the two functions from LoggedIn to update the tabs
    """
    logged_in_tab = LoggedIn(
        dlg=dlg,
        username=username,
        url=url,
        arches_user_info=arches_api.arches_user_info,
    )
    logged_in_tab.update_logged_in_view()
    logged_in_tab.hide_login_tab()


def update_create_resources_tab(dlg):
    dlg.createResModelSelectCombo.clear()
    dlg.createResGeomSelectCombo.setEnabled(True)
    dlg.createResGeomSelectCombo.clear()
    dlg.createResGeomSelectCombo.addItems([layer.name() for layer in arches_api.layers])

    if arches_api.arches_graphs_list:
        dlg.createResModelSelectCombo.setEnabled(True)
        dlg.createResModelSelectCombo.addItems(
            [graph["name"] for graph in arches_api.arches_graphs_list]
        )
        dlg.createResButton.setEnabled(True)


def update_edit_resources_tab(dlg):
    dlg.editResAddGeom.setEnabled(False)
    dlg.editResReplaceGeom.setEnabled(False)
    if arches_api.arches_selected_resource["resourceinstanceid"]:
        dlg.editResAddGeom.setEnabled(True)
        dlg.editResReplaceGeom.setEnabled(True)
    dlg.editResGeomSelectCombo.setEnabled(True)
    dlg.editResGeomSelectCombo.clear()
    dlg.editResGeomSelectCombo.addItems([layer.name() for layer in arches_api.layers])
    dlg.editResSelectedResAttributeTable.setEnabled(True)
    dlg.editResSelectedResId.setText(
        "Connected to Arches. Select an Arches resource to proceed."
    )
