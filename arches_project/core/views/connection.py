from arches_project.core.arches.connection import ConnectionProcess
from arches_project.core.views.components.missing_credentials import missing_credentials
from arches_project.core.views.login import UpdateLoginProgress
from arches_project.core.views.components.spinner import triggerSpinner
from arches_project.core.arches.api import arches_api

from qgis.core import QgsMessageLog, QgsApplication


class ArchesConnectionView:
    def __init__(self, dlg, plugin_dir, iface):
        self.error_msg = ""
        self.dlg = dlg
        self.plugin_dir = plugin_dir
        self.iface = iface

    def arches_connection_save(self):
        """
        Connection to Arches project server
        """
        self.error_msg = ""
        connection_information = {
            "URL": {
                "value": self.dlg.archesServerInput.text().strip(),
                "input": self.dlg.archesServerInput,
                "label": self.dlg.archesServerLabel,
            },
            "username": {
                "value": self.dlg.usernameInput.text().strip(),
                "input": self.dlg.usernameInput,
                "label": self.dlg.usernameLabel,
            },
            "password": {
                "value": self.dlg.passwordInput.text().strip(),
                "input": self.dlg.passwordInput,
                "label": self.dlg.passwordLabel,
            },
        }

        is_valid_input = True
        missing_inputs = []
        for k, v in connection_information.items():
            if not v["value"]:
                is_valid_input = False
                missing_credentials(v["input"], "True")
                missing_credentials(v["label"], "True")
                missing_inputs.append(k)
            else:
                missing_credentials(v["label"], "False")
                missing_credentials(v["input"], "False")

        if missing_inputs:
            if len(missing_inputs) > 1:
                self.error_msg = f"Login missing values for {', '.join(missing_inputs[:-1])} and {missing_inputs[-1]}."
            else:
                self.error_msg = f"Login missing {missing_inputs[0]}."
            self.dlg.loginErrorMessageLabel.setText(self.error_msg)
            self.dlg.loginErrorMessageFrame.show()
            self.dlg.loginErrorMessageLabel.show()
        else:
            self.dlg.loginErrorMessageLabel.setText("")
            self.dlg.loginErrorMessageFrame.hide()
            self.dlg.loginErrorMessageLabel.hide()

        if is_valid_input == True:
            url_input = self.dlg.archesServerInput.text()
            formatted_url = url_input.strip().rstrip("/")

            # Adding arches connection to task queue
            self.arches_connection = ConnectionProcess(
                url=formatted_url,
                username=connection_information["username"]["value"],
                password=connection_information["password"]["value"],
                dlg=self.dlg,
                iface=self.iface,
                plugin_dir=self.plugin_dir,
            )
            self.login_text_updater = UpdateLoginProgress(self.dlg.updateText)
            self.login_percent_updater = UpdateLoginProgress(
                self.dlg.percentProgressText
            )
            self.dlg.updateText.setText("")
            self.dlg.percentProgressText.setText("0%")
            self.arches_connection.login_updates.connect(
                self.login_text_updater.update_login_progress
            )
            self.arches_connection.percent_progress.connect(
                self.login_percent_updater.update_percent
            )
            QgsApplication.taskManager().addTask(self.arches_connection)

            # 24 Tasks must be assigned to self, otherwise finished() won't run
            # https://github.com/qgis/QGIS/issues/59464#issuecomment-2640165772

            self.spinner = triggerSpinner(dlg=self.dlg, plugin_dir=self.plugin_dir)
            self.spinner.start_spinner()

            # A log message (or print) is required for the task to be run.
            # It is an existing QGIS issue https://github.com/qgis/QGIS/issues/37655
            QgsMessageLog.logMessage("Connection task started")

    def update_create_resources_tab(self):
        self.dlg.createResModelSelect.clear()
        self.dlg.createResFeatureSelect.setEnabled(True)
        self.dlg.createResFeatureSelect.clear()
        self.dlg.createResFeatureSelect.addItems(
            [layer.name() for layer in arches_api.layers]
        )

        if arches_api.arches_graphs_list:
            self.dlg.createResModelSelect.setEnabled(True)
            self.dlg.createResModelSelect.addItems(
                [graph["name"] for graph in arches_api.arches_graphs_list]
            )
            self.dlg.addNewRes.setEnabled(True)

    def update_edit_resources_tab(self):
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
