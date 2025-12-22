from qgis.core import QgsApplication
from arches_project.core.arches.ConnectionRefreshTask import ConnectionRefreshTask


def connection_refresh(dlg):
    dlg.connection_refresh_task = ConnectionRefreshTask(dlg=dlg, iface=dlg.iface)
    QgsApplication.taskManager().addTask(dlg.connection_refresh_task)
