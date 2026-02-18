from qgis.PyQt.QtWidgets import QLineEdit


class AutoCompleteLineEdit(QLineEdit):

    def __init__(self, parent=None):
        super().__init__(parent)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        completer = self.completer()
        if completer:
            completer.complete()
