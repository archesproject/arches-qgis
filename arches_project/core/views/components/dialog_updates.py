from arches_project.core.views.components.qgis_messaging import show_message
from arches_project.core.views.components.login_autocomplete import (
    load_saved_credentials,
)
from arches_project.core.views.login import LoggedIn
from arches_project.core.arches.api import arches_api
from qgis.PyQt.QtWidgets import QTableWidgetItem, QLabel
from PyQt5.QtCore import Qt
from datetime import datetime

from PyQt5.QtCore import QTimer, QPropertyAnimation, QEasingCurve
from qgis.PyQt.QtGui import QIcon

import os


def connection_reset(hard_reset, dlg, iface, manual_logout=False):
    """
    Reset Arches connection
    """
    if hard_reset == True:
        # Reset logged in values
        dlg.displayFullNameLabel.setText("")
        dlg.displayConnectionInfoLabel.setText("")
        dlg.displayUsernameLabel.setText("")
        # Replace login tab with logged in tab
        dlg.tabWidget.setTabVisible(0, True)
        dlg.tabWidget.setTabVisible(1, False)
        # Reset stored data
        arches_api.arches_user_info = {}
        arches_api.arches_connection_cache = {}
        arches_api.arches_token = {}
        arches_api.arches_graphs_list = []
        # Reload saved credentials for the autocompletes
        load_saved_credentials(dlg)
        # Return to login page
        dlg.tabWidget.setCurrentIndex(0)
        # Reset connection inputs
        if manual_logout == True:
            dlg.archesServerInput.setText("")
            dlg.usernameInput.setText("")
            dlg.passwordInput.setText("")

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

    if manual_logout == True:
        dlg.refreshConfirmFrame.hide()
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


def update_refresh_confirm_label(dlg, connected):
    def fade_out():
        dlg.fade_animation = QPropertyAnimation(dlg.opacity_effect, b"opacity")
        dlg.fade_animation.setDuration(1000)
        dlg.fade_animation.setStartValue(1)
        dlg.fade_animation.setEndValue(0)
        dlg.fade_animation.setEasingCurve(QEasingCurve.OutCubic)

        dlg.fade_animation.finished.connect(dlg.refreshConfirmFrame.hide)

        dlg.fade_animation.start()

    dlg.opacity_effect.setOpacity(1.0)
    dlg.refreshConfirmFrame.show()
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    if connected:
        dlg.refreshConfirmLabel.setStyleSheet("color: #666;")
        dlg.refreshConfirmLabel.setText(f"Refreshed at {formatted_datetime}")
        QTimer.singleShot(6000, fade_out)
    else:
        dlg.refreshConfirmLabel.setStyleSheet("color: red;")
        dlg.refreshConfirmLabel.setText(
            f"Refresh failed at {formatted_datetime}. Check connection."
        )


def disable_refresh_btn(dlg):
    dlg.btnRefresh.setEnabled(False)
    dlg.btnRefresh.setText("Loading...")
    dlg.btnRefresh.setIcon(QIcon(""))


def reset_refresh_btn(dlg):
    dlg.btnRefresh.setEnabled(True)
    dlg.btnRefresh.setText("Refresh models and nodes")
    dlg.btnRefresh.setIcon(
        QIcon(
            os.path.join(dlg.plugin_dir, "icons", "arrows-rotate-solid-full-white.svg")
        )
    )


def update_activity_log(dlg, action, resource_url, resourceinstance_id):
    resource_link = f"<a href='{resource_url}'>{resourceinstance_id}</a>"
    link_label = QLabel(resource_link)
    link_label.setOpenExternalLinks(True)

    dlg.activityLogTable.insertRow(0)

    action_task_widget = QTableWidgetItem(action)
    action_task_widget.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)

    action_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    action_datetime_widget = QTableWidgetItem(action_datetime)
    action_datetime_widget.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)

    dlg.activityLogTable.setItem(0, 0, action_task_widget)
    dlg.activityLogTable.setItem(0, 1, action_datetime_widget)
    dlg.activityLogTable.setCellWidget(0, 2, link_label)

    dlg.activityLogTable.scrollToTop()
