from qgis.PyQt.QtGui import QIcon


class DefaultStylesheet:
    def __init__(
        self,
        dlg,
        dlg_resource_creation,
        dlg_edit_resource_add,
        dlg_edit_resource_replace,
    ):
        self.dlg = dlg
        self.dlg_resource_creation = dlg_resource_creation
        self.dlg_edit_resource_add = dlg_edit_resource_add
        self.dlg_edit_resource_replace = dlg_edit_resource_replace

    def default_stylesheet(self):
        # reset stylesheets
        self.dlg.setStyleSheet("")
        self.dlg_resource_creation.setStyleSheet("")
        self.dlg_edit_resource_add.setStyleSheet("")
        self.dlg_edit_resource_replace.setStyleSheet("")
        # remove icons from buttons
        self.dlg.btnConnect.setIcon(QIcon(""))
        self.dlg.btnLogout.setIcon(QIcon(""))
        self.dlg.addNewRes.setIcon(QIcon(""))
        self.dlg.addEditRes.setIcon(QIcon(""))
        self.dlg.replaceEditRes.setIcon(QIcon(""))
        self.dlg_resource_creation.createDialogCancel.setIcon(QIcon(""))
        self.dlg_resource_creation.createDialogCreate.setIcon(QIcon(""))
        self.dlg_edit_resource_add.editDialogCancel.setIcon(QIcon(""))
        self.dlg_edit_resource_add.editDialogCreate.setIcon(QIcon(""))
        self.dlg_edit_resource_replace.editDialogCancel.setIcon(QIcon(""))
        self.dlg_edit_resource_replace.editDialogCreate.setIcon(QIcon(""))
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
        self.dlg.tabWidget.setTabText(4, "Settings")
        self.dlg.tabWidget.setTabIcon(5, QIcon(""))
        self.dlg.tabWidget.setTabText(5, "Log")
