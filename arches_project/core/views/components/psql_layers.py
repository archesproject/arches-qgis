from qgis.core import QgsProject, QgsVectorLayer

from arches_project.core.arches.api import arches_api

# Note this will be removed with #8


def show_hide_psql_layers(combobox1, combobox2, dlg):
    """
    Reflect change made by checkbox to show or hide PSQL layers from self.layers
    """
    # TODO: Not sure I like the way this works but it works

    def change_both_comboboxes(c):
        c.blockSignals(True)
        c.clear()
        c.addItems([layer.name() for layer in arches_api.layers])
        c.blockSignals(False)

    if dlg.hidePostgresLayers.isChecked():
        arches_api.layers = [
            l
            for l in QgsProject.instance().mapLayers().values()
            if l.type() == QgsVectorLayer.VectorLayer
            if str(l.dataProvider().name()) != "postgres"
        ]
        change_both_comboboxes(combobox1)
        change_both_comboboxes(combobox2)

    elif not dlg.hidePostgresLayers.isChecked():
        arches_api.layers = [
            l
            for l in QgsProject.instance().mapLayers().values()
            if l.type() == QgsVectorLayer.VectorLayer
        ]
        change_both_comboboxes(combobox1)
        change_both_comboboxes(combobox2)
