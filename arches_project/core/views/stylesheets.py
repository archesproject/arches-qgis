from qgis.PyQt.QtGui import QIcon, QCursor, QPixmap, QTransform
from qgis.PyQt.QtCore import QDir, QSize
from PyQt5.QtCore import Qt

import os

class PluginStylesheets:
    def __init__(self, 
                 dlg, 
                 dlg_resource_creation, 
                 dlg_edit_resource_add,
                 dlg_edit_resource_replace,
                 plugin_dir,
                 on_start):
        self.dlg = dlg
        self.dlg_resource_creation = dlg_resource_creation
        self.dlg_edit_resource_add = dlg_edit_resource_add
        self.dlg_edit_resource_replace = dlg_edit_resource_replace
        self.plugin_dir = plugin_dir
        self.on_start = on_start

        if not self.dlg.useStylesheetCheckbox.isChecked():
            self.default_stylesheet()
        elif self.dlg.useStylesheetCheckbox.isChecked():
            self.arches_stylesheet()

        if self.on_start == True:
            self.arches_stylesheet()


    def default_stylesheet(self):
        # reset stylesheets
        self.dlg.setStyleSheet("")
        self.dlg_resource_creation.setStyleSheet("")
        self.dlg_edit_resource_add.setStyleSheet("")
        self.dlg_edit_resource_replace.setStyleSheet("")
        # remove icons from buttons
        self.dlg.btnSave.setIcon(QIcon(""))
        self.dlg.btnReset.setIcon(QIcon(""))
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


    def arches_stylesheet(self):
        # try:
            self.dlg.useStylesheetCheckbox.setChecked(True)
            stylesheet_path = os.path.join(self.plugin_dir, "stylesheets", "arches_styling.qss")
            with open(stylesheet_path, "r") as f:
                arches_styling = f.read()

            # self.dlg.setAutoFillBackground(False)
            # self.dlg.setContentsMargins(0,0,0,0)
            # # self.dlg.setStyleSheet("QDialog{background-color: green;}")

            self.dlg.setStyleSheet(arches_styling)
            self.dlg_resource_creation.setStyleSheet(arches_styling)
            self.dlg_edit_resource_add.setStyleSheet(arches_styling)
            self.dlg_edit_resource_replace.setStyleSheet(arches_styling)

            QDir.addSearchPath('images', os.path.join(self.plugin_dir, "icons"))

            self.dlg.btnSave.setIcon(QIcon(os.path.join(self.plugin_dir, "icons", "ion-log-in.svg")))
            self.dlg.btnSave.setIconSize(QSize(12,12))
            self.dlg.btnSave.setCursor(QCursor(Qt.PointingHandCursor))

            self.dlg.btnReset.setIcon(QIcon(os.path.join(self.plugin_dir, "icons", "ion-arrow-undo.svg")))
            self.dlg.btnReset.setIconSize(QSize(12,12))
            self.dlg.btnReset.setCursor(QCursor(Qt.PointingHandCursor))

            self.dlg.addNewRes.setIcon(QIcon(os.path.join(self.plugin_dir, "icons", "mdi-pencil.svg")))
            self.dlg.addNewRes.setIconSize(QSize(12,12))
            self.dlg.addNewRes.setCursor(QCursor(Qt.PointingHandCursor))

            self.dlg.addEditRes.setIcon(QIcon(os.path.join(self.plugin_dir, "icons", "fa-plus.svg")))
            self.dlg.addEditRes.setIconSize(QSize(12,12))
            self.dlg.addEditRes.setCursor(QCursor(Qt.PointingHandCursor))

            self.dlg.replaceEditRes.setIcon(QIcon(os.path.join(self.plugin_dir, "icons", "mi-replace.svg")))
            self.dlg.replaceEditRes.setIconSize(QSize(12,12))
            self.dlg.replaceEditRes.setCursor(QCursor(Qt.PointingHandCursor))

            self.dlg_resource_creation.createDialogCancel.setIcon(QIcon(os.path.join(self.plugin_dir, "icons", "fa-times.svg")))
            self.dlg_resource_creation.createDialogCancel.setIconSize(QSize(12,12))
            self.dlg_resource_creation.createDialogCancel.setCursor(QCursor(Qt.PointingHandCursor))

            self.dlg_resource_creation.createDialogCreate.setIcon(QIcon(os.path.join(self.plugin_dir, "icons", "fa-plus.svg")))
            self.dlg_resource_creation.createDialogCreate.setIconSize(QSize(12,12))
            self.dlg_resource_creation.createDialogCreate.setCursor(QCursor(Qt.PointingHandCursor))

            self.dlg_edit_resource_add.editDialogCancel.setIcon(QIcon(os.path.join(self.plugin_dir, "icons", "fa-times.svg")))
            self.dlg_edit_resource_add.editDialogCancel.setIconSize(QSize(12,12))
            self.dlg_edit_resource_add.editDialogCancel.setCursor(QCursor(Qt.PointingHandCursor))

            self.dlg_edit_resource_add.editDialogCreate.setIcon(QIcon(os.path.join(self.plugin_dir, "icons", "fa-plus.svg")))
            self.dlg_edit_resource_add.editDialogCreate.setIconSize(QSize(12,12))
            self.dlg_edit_resource_add.editDialogCreate.setCursor(QCursor(Qt.PointingHandCursor))

            self.dlg_edit_resource_replace.editDialogCancel.setIcon(QIcon(os.path.join(self.plugin_dir, "icons", "fa-times.svg")))
            self.dlg_edit_resource_replace.editDialogCancel.setIconSize(QSize(12,12))
            self.dlg_edit_resource_replace.editDialogCancel.setCursor(QCursor(Qt.PointingHandCursor))

            self.dlg_edit_resource_replace.editDialogCreate.setIcon(QIcon(os.path.join(self.plugin_dir, "icons", "fa-times.svg")))
            self.dlg_edit_resource_replace.editDialogCreate.setIconSize(QSize(12,12))
            self.dlg_edit_resource_replace.editDialogCreate.setCursor(QCursor(Qt.PointingHandCursor))

            self.dlg.tabWidget.setDocumentMode(True)

            self.dlg.tabWidget.setTabIcon(0, QIcon(QPixmap(os.path.join(self.plugin_dir, "icons", "mdi-connection.svg")).transformed(QTransform().rotate(90))))
            self.dlg.tabWidget.setIconSize(QSize(16,16))
            self.dlg.tabWidget.setTabText(0, "")

            self.dlg.tabWidget.setTabIcon(1, QIcon(QPixmap(os.path.join(self.plugin_dir, "icons", "ti-home.svg")).transformed(QTransform().rotate(90))))
            self.dlg.tabWidget.setIconSize(QSize(16,16))
            self.dlg.tabWidget.setTabText(1, "")

            self.dlg.tabWidget.setTabIcon(2, QIcon(QPixmap(os.path.join(self.plugin_dir, "icons", "fa-building.svg")).transformed(QTransform().rotate(90))))
            self.dlg.tabWidget.setIconSize(QSize(16,16))
            self.dlg.tabWidget.setTabText(2, "")

            self.dlg.tabWidget.setTabIcon(3, QIcon(QPixmap(os.path.join(self.plugin_dir, "icons", "mdi-pencil.svg")).transformed(QTransform().rotate(90))))
            self.dlg.tabWidget.setIconSize(QSize(16,16))
            self.dlg.tabWidget.setTabText(3, "")

            self.dlg.tabWidget.setTabIcon(4, QIcon(QPixmap(os.path.join(self.plugin_dir, "icons", "fa-cog.svg")).transformed(QTransform().rotate(90))))
            self.dlg.tabWidget.setIconSize(QSize(16,16))
            self.dlg.tabWidget.setTabText(4, "")

            self.dlg.tabWidget.setTabIcon(5, QIcon(QPixmap(os.path.join(self.plugin_dir, "icons", "ti-ticket.svg")).transformed(QTransform().rotate(90))))
            self.dlg.tabWidget.setIconSize(QSize(16,16))
            self.dlg.tabWidget.setTabText(5, "")


        # except:
        #     # Prevent the use of the Arches stylesheet if error occurs
        #     self.default_stylesheet()
        #     self.dlg.useStylesheetCheckbox.setEnabled(False)
        #     self.dlg.useStylesheetCheckbox.setChecked(False)
