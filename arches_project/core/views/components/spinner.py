from PyQt5 import QtCore, QtGui, QtWidgets
from qgis.PyQt.QtGui import QPixmap
import os


class Spinner(QtWidgets.QLabel):
    def __init__(self, loadingWheel, *args, **kwargs):
        super(Spinner, self).__init__(*args, **kwargs)
        self._pixmap = QtGui.QPixmap()
        self._animation = QtCore.QVariantAnimation(
            self,
            startValue=0.0,
            endValue=360.0,
            duration=2000,
            valueChanged=self.on_valueChanged,
        )
        self.loadingWheel = loadingWheel

    def start(self):
        self._animation.setLoopCount(-1)
        if self._animation.state() != QtCore.QAbstractAnimation.Running:
            self._animation.start(
                QtCore.QAbstractAnimation.DeletionPolicy.KeepWhenStopped
            )

    def set_pixmap(self, pixmap):
        self._pixmap = pixmap.scaled(140, 140, QtCore.Qt.KeepAspectRatio)
        self.loadingWheel.setPixmap(self._pixmap)

    @QtCore.pyqtSlot(QtCore.QVariant)
    def on_valueChanged(self, value):
        t = QtGui.QTransform()
        t.rotate(value)
        self.loadingWheel.setPixmap((self._pixmap.transformed(t)))


class triggerSpinner(QtWidgets.QWidget):
    def __init__(self, dlg, plugin_dir, parent=None):
        super(triggerSpinner, self).__init__(parent)
        self.dlg = dlg

        self.spinner = Spinner(
            loadingWheel=self.dlg.loadingWheel,
        )
        self.dlg.loadingWheel.setFixedSize(150, 150)
        self.spinner.set_pixmap(
            QPixmap(os.path.join(plugin_dir, "icons", "spinner.svg"))
        )

    def start_spinner(self):
        self.reveal_spinner()
        self.spinner.start()

    def reveal_spinner(self):
        self.dlg.tabWidget.hide()
        self.dlg.loadingWheel.show()
        self.dlg.updateTextFrame.show()
        self.dlg.loginErrorMessageFrame.show()
        self.dlg.loadingWheelVerticalSpacerFrame.show()

    def hide_spinner(self):
        self.dlg.tabWidget.show()
        self.dlg.loadingWheel.hide()
        self.dlg.updateTextFrame.hide()
        self.dlg.loginErrorMessageFrame.hide()
        self.dlg.loadingWheelVerticalSpacerFrame.hide()
