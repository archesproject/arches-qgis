from qgis.PyQt.QtGui import QIcon


class DefaultStylesheet:
    def __init__(self, dlg, dlg_resource_confirmation):
        self.dlg = dlg
        self.dlg_resource_confirmation = dlg_resource_confirmation

    def default_stylesheet(self):
        # reset stylesheets
        self.dlg.setStyleSheet("")
        self.dlg_resource_confirmation.setStyleSheet("")
        # remove icons from buttons
        self.dlg.btnConnect.setIcon(QIcon(""))
        self.dlg.btnLogout.setIcon(QIcon(""))
        self.dlg.createResButton.setIcon(QIcon(""))
        self.dlg.editResAddGeom.setIcon(QIcon(""))
        self.dlg.editResReplaceGeom.setIcon(QIcon(""))
        self.dlg.btnRefresh.setIcon(QIcon(""))
        self.dlg_resource_confirmation.confirmDialogCancel.setIcon(QIcon(""))
        self.dlg_resource_confirmation.confirmDialogConfirm.setIcon(QIcon(""))
        # nav bar
        # TODO: don't like the fact I have to add the exact strings (from qtcreator) back to the tab titles, seems like could be a better method...
        self.dlg.tabWidget.setStyleSheet(" QTabWidget {qproperty-tabPosition: North;} ")
        self.dlg.tabWidget.setStyleSheet("")

        self.dlg.tabWidget.setAutoFillBackground(False)
        self.dlg.tabWidget.setTabIcon(0, QIcon(""))
        self.dlg.tabWidget.setTabText(0, "Arches Connection")
        self.dlg.tabWidget.setTabIcon(1, QIcon(""))
        self.dlg.tabWidget.setTabText(1, "Arches Connection")
        self.dlg.tabWidget.setTabIcon(2, QIcon(""))
        self.dlg.tabWidget.setTabText(2, "Create Resource")
        self.dlg.tabWidget.setTabIcon(3, QIcon(""))
        self.dlg.tabWidget.setTabText(3, "Edit Resource")
        self.dlg.tabWidget.setTabIcon(4, QIcon(""))
        self.dlg.tabWidget.setTabText(4, "Log")
        self.dlg.tabWidget.setTabIcon(5, QIcon(""))
        self.dlg.tabWidget.setTabText(5, "Settings")
