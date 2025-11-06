from qgis.PyQt.QtGui import QIcon, QCursor, QPixmap, QTransform
from qgis.PyQt.QtCore import QDir, QSize
from PyQt5.QtCore import Qt

import os


class PluginStylesheets:
    def __init__(self, 
                 dlg,
                 dlg_resource_confirmation, 
                 plugin_dir,
                 on_start):
        self.dlg = dlg
        self.dlg_resource_confirmation = dlg_resource_confirmation
        self.plugin_dir = plugin_dir
        self.on_start = on_start

        # hide loading wheel adjustments
        self.dlg.loadingWheel.hide()  # connection wheel label
        self.dlg.updateTextFrame.hide()
        self.dlg.loginErrorMessageFrame.hide()
        self.dlg.loadingWheelVerticalSpacerFrame.hide()

        if not self.dlg.useStylesheetCheckbox.isChecked():
            self.default_stylesheet()
        elif self.dlg.useStylesheetCheckbox.isChecked():
            self.arches_stylesheet()

        if self.on_start == True:
            self.arches_stylesheet()

    def default_stylesheet(self):
        # reset stylesheets
        self.dlg.setStyleSheet("")
        self.dlg_resource_confirmation.setStyleSheet("")
        # remove icons from buttons
        self.dlg.btnConnect.setIcon(QIcon(""))
        self.dlg.btnLogout.setIcon(QIcon(""))
        self.dlg.addNewRes.setIcon(QIcon(""))
        self.dlg.addEditRes.setIcon(QIcon(""))
        self.dlg.replaceEditRes.setIcon(QIcon(""))
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
        self.dlg.tabWidget.setTabText(4, "Settings")
        self.dlg.tabWidget.setTabIcon(5, QIcon(""))
        self.dlg.tabWidget.setTabText(5, "Log")

    def arches_stylesheet(self):
        try:
            self.dlg.useStylesheetCheckbox.setChecked(True)
            stylesheet_path = os.path.join(
                self.plugin_dir, "stylesheets", "arches_styling.qss"
            )
            with open(stylesheet_path, "r") as f:
                arches_styling = f.read()

            self.dlg.setStyleSheet(arches_styling)
            self.dlg_resource_confirmation.setStyleSheet(arches_styling)

            QDir.addSearchPath("images", os.path.join(self.plugin_dir, "icons"))

            self.dlg.btnConnect.setIcon(
                QIcon(os.path.join(self.plugin_dir, "icons", "ion-log-in.svg"))
            )
            self.dlg.btnConnect.setIconSize(QSize(12, 12))
            self.dlg.btnConnect.setCursor(QCursor(Qt.PointingHandCursor))

            self.dlg.btnLogout.setIcon(
                QIcon(os.path.join(self.plugin_dir, "icons", "ion-arrow-undo.svg"))
            )
            self.dlg.btnLogout.setIconSize(QSize(12, 12))
            self.dlg.btnLogout.setCursor(QCursor(Qt.PointingHandCursor))

            self.dlg.addNewRes.setIcon(
                QIcon(os.path.join(self.plugin_dir, "icons", "mdi-pencil.svg"))
            )
            self.dlg.addNewRes.setIconSize(QSize(12, 12))
            self.dlg.addNewRes.setCursor(QCursor(Qt.PointingHandCursor))

            self.dlg.addEditRes.setIcon(
                QIcon(os.path.join(self.plugin_dir, "icons", "fa-plus.svg"))
            )
            self.dlg.addEditRes.setIconSize(QSize(12, 12))
            self.dlg.addEditRes.setCursor(QCursor(Qt.PointingHandCursor))

            self.dlg.replaceEditRes.setIcon(
                QIcon(os.path.join(self.plugin_dir, "icons", "mi-replace.svg"))
            )
            self.dlg.replaceEditRes.setIconSize(QSize(12, 12))
            self.dlg.replaceEditRes.setCursor(QCursor(Qt.PointingHandCursor))

            self.dlg_resource_confirmation.confirmDialogCancel.setIcon(QIcon(os.path.join(self.plugin_dir, "icons", "fa-times.svg")))
            self.dlg_resource_confirmation.confirmDialogCancel.setIconSize(QSize(12,12))
            self.dlg_resource_confirmation.confirmDialogCancel.setCursor(QCursor(Qt.PointingHandCursor))

            self.dlg_resource_confirmation.confirmDialogConfirm.setIcon(QIcon(os.path.join(self.plugin_dir, "icons", "fa-plus.svg")))
            self.dlg_resource_confirmation.confirmDialogConfirm.setIconSize(QSize(12,12))
            self.dlg_resource_confirmation.confirmDialogConfirm.setCursor(QCursor(Qt.PointingHandCursor))

            self.dlg.tabWidget.setDocumentMode(True)

            self.dlg.tabWidget.setTabIcon(
                0,
                QIcon(
                    QPixmap(
                        os.path.join(self.plugin_dir, "icons", "mdi-connection.svg")
                    ).transformed(QTransform().rotate(90))
                ),
            )
            self.dlg.tabWidget.setIconSize(QSize(16, 16))
            self.dlg.tabWidget.setTabText(0, "")

            self.dlg.tabWidget.setTabIcon(
                1,
                QIcon(
                    QPixmap(
                        os.path.join(self.plugin_dir, "icons", "ti-home.svg")
                    ).transformed(QTransform().rotate(90))
                ),
            )
            self.dlg.tabWidget.setIconSize(QSize(16, 16))
            self.dlg.tabWidget.setTabText(1, "")

            self.dlg.tabWidget.setTabIcon(
                2,
                QIcon(
                    QPixmap(
                        os.path.join(self.plugin_dir, "icons", "fa-building.svg")
                    ).transformed(QTransform().rotate(90))
                ),
            )
            self.dlg.tabWidget.setIconSize(QSize(16, 16))
            self.dlg.tabWidget.setTabText(2, "")

            self.dlg.tabWidget.setTabIcon(
                3,
                QIcon(
                    QPixmap(
                        os.path.join(self.plugin_dir, "icons", "mdi-pencil.svg")
                    ).transformed(QTransform().rotate(90))
                ),
            )
            self.dlg.tabWidget.setIconSize(QSize(16, 16))
            self.dlg.tabWidget.setTabText(3, "")

            self.dlg.tabWidget.setTabIcon(
                4,
                QIcon(
                    QPixmap(
                        os.path.join(self.plugin_dir, "icons", "fa-cog.svg")
                    ).transformed(QTransform().rotate(90))
                ),
            )
            self.dlg.tabWidget.setIconSize(QSize(16, 16))
            self.dlg.tabWidget.setTabText(4, "")

            self.dlg.tabWidget.setTabIcon(
                5,
                QIcon(
                    QPixmap(
                        os.path.join(self.plugin_dir, "icons", "ti-ticket.svg")
                    ).transformed(QTransform().rotate(90))
                ),
            )
            self.dlg.tabWidget.setIconSize(QSize(16, 16))
            self.dlg.tabWidget.setTabText(5, "")

            self.dlg.userProfileLabel.setFixedSize(80, 80)
            self.dlg.userProfileLabel.setPixmap(
                QPixmap(os.path.join(self.plugin_dir, "icons", "ion-user.svg")).scaled(
                    50, 50, Qt.KeepAspectRatio
                )
            )
            self.dlg.loginSuccessFrame.hide()

        except:
            # Prevent the use of the Arches stylesheet if error occurs
            self.default_stylesheet()
            self.dlg.useStylesheetCheckbox.setEnabled(False)
            self.dlg.useStylesheetCheckbox.setChecked(False)
