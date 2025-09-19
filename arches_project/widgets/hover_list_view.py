from qgis.PyQt.QtWidgets import QListView

class HoverListView(QListView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        index = self.indexAt(event.pos())
        if index.isValid():
            self.setCurrentIndex(index)
        super().mouseMoveEvent(event)