from PyQt5 import QtCore, QtGui, QtWidgets
from qgis.PyQt.QtGui import QPixmap
import os


class Spinner(QtWidgets.QLabel):
    def __init__(self, arches_obj, *args, **kwargs):
        super(Spinner, self).__init__(*args, **kwargs)
        self._pixmap = QtGui.QPixmap()
        self._animation = QtCore.QVariantAnimation(
            self,
            startValue=0.0,
            endValue=360.0,
            duration=2000,
            valueChanged=self.on_valueChanged
        )
        self.arches_obj = arches_obj
    
    def start(self):
        self._animation.setLoopCount(-1)        
        if self._animation.state() != QtCore.QAbstractAnimation.Running:
            self._animation.start(QtCore.QAbstractAnimation.DeletionPolicy.KeepWhenStopped)

    def set_pixmap(self, pixmap):
        self._pixmap = pixmap.scaled(140, 140, QtCore.Qt.KeepAspectRatio)
        self.arches_obj.dlg.loadingWheel.setPixmap(self._pixmap)

    @QtCore.pyqtSlot(QtCore.QVariant)
    def on_valueChanged(self, value):
        t = QtGui.QTransform()
        t.rotate(value)
        self.arches_obj.dlg.loadingWheel.setPixmap((self._pixmap.transformed(t)))



class triggerSpinner(QtWidgets.QWidget):
    def __init__(self, parent=None, arches_obj=None):
        super(triggerSpinner, self).__init__(parent)
        self.arches_obj = arches_obj
        self.spinner = Spinner(arches_obj, arches_obj.dlg.loadingWheel, )
        self.arches_obj.dlg.loadingWheel.setFixedSize(150, 150)
        self.spinner.set_pixmap(QPixmap(os.path.join(arches_obj.plugin_dir, "icons", "spinner.svg")))

    def start_spinner(self):
        self.reveal_spinner()
        self.spinner.start()
    
    def reveal_spinner(self):
        self.arches_obj.dlg.tabWidget.hide()
        self.arches_obj.dlg.loadingWheel.show()
        self.arches_obj.dlg.updateTextFrame.show()
        self.arches_obj.dlg.loginErrorMessageFrame.show()
        self.arches_obj.dlg.loadingWheelVerticalSpacerFrame.show()

    def hide_spinner(self):
        self.arches_obj.dlg.tabWidget.show()
        self.arches_obj.dlg.loadingWheel.hide()
        self.arches_obj.dlg.updateTextFrame.hide()
        self.arches_obj.dlg.loginErrorMessageFrame.hide()
        self.arches_obj.dlg.loadingWheelVerticalSpacerFrame.hide()

