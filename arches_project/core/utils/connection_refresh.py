from qgis.core import QgsApplication
from PyQt5.QtCore import QTimer
from arches_project.core.arches.connection_refresh_task import ConnectionRefreshTask
from arches_project.core.views.components.dialog_updates import reset_refresh_btn


def connection_refresh(dlg):

    def start_reset_timer():
        QTimer.singleShot(2500, lambda: reset_refresh_btn(dlg))

    dlg.connection_refresh_task = ConnectionRefreshTask(dlg=dlg, iface=dlg.iface)
    QgsApplication.taskManager().addTask(dlg.connection_refresh_task)

    dlg.connection_refresh_task.refresh_finished.connect(start_reset_timer)
