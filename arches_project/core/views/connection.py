from qgis.core import QgsMessageLog, Qgis

from arches_project.core.arches.connection import ConnectionProcess
from arches_project.core.views.login import UpdateLogin
from arches_project.core.views.login import UpdateLogin
from arches_project.core.views.components.spinner import triggerSpinner


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
        # self.error_msg = ""
        self.config_id = self.dlg.selected_config_id

        QgsMessageLog.logMessage(
            "selected config id: " + str(self.config_id),
            "Arches Plugin",
            level=Qgis.Info,
        )

        # Adding arches connection to task queue
        self.arches_connection = ConnectionProcess(
            config_id=self.config_id,
            dlg=self.dlg,
            iface=self.iface,
            plugin_dir=self.plugin_dir,
        )

        self.login_text_updater = UpdateLogin(self.dlg.updateText)
        self.login_percent_updater = UpdateLogin(self.dlg.percentProgressText)
        self.dlg.updateText.setText("")
        self.dlg.percentProgressText.setText("0%")
        self.arches_connection.login_updates.connect(
            self.login_text_updater.update_login_progress
        )
        self.arches_connection.percent_progress.connect(
            self.login_percent_updater.update_percent
        )
        self.arches_connection.run()

        self.spinner = triggerSpinner(dlg=self.dlg, plugin_dir=self.plugin_dir)
        self.spinner.start_spinner()

        # A log message (or print) is required for the task to be run.
        # It is an existing QGIS issue https://github.com/qgis/QGIS/issues/37655
        QgsMessageLog.logMessage(
            "Connection task started", "Arches Plugin", level=Qgis.Info
        )
