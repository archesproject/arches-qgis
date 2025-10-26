from qgis.core import QgsProject, QgsVectorLayer

# Note this will be removed with #8


def update_map_layers(layers, checkbox):
    """
    Function to update new vector layers dynamically
    """

    if checkbox.isChecked():
        all_current_layers = [
            l
            for l in QgsProject.instance().mapLayers().values()
            if l.type() == QgsVectorLayer.VectorLayer
            if str(l.dataProvider().name()) != "postgres"
        ]

    elif not checkbox.isChecked():
        all_current_layers = [
            l
            for l in QgsProject.instance().mapLayers().values()
            if l.type() == QgsVectorLayer.VectorLayer
        ]

    if layers != all_current_layers:
        layers = all_current_layers


def show_hide_psql_layers(layers, combobox1, combobox2, dlg):
    """
    Reflect change made by checkbox to show or hide PSQL layers from self.layers
    """
    # TODO: Not sure I like the way this works but it works

    def change_both_comboboxes(c):
        c.blockSignals(True)
        c.clear()
        c.addItems([layer.name() for layer in layers])
        c.blockSignals(False)

    if dlg.hidePostgresLayers.isChecked():
        layers = [
            l
            for l in QgsProject.instance().mapLayers().values()
            if l.type() == QgsVectorLayer.VectorLayer
            if str(l.dataProvider().name()) != "postgres"
        ]
        change_both_comboboxes(combobox1)
        change_both_comboboxes(combobox2)

    elif not dlg.hidePostgresLayers.isChecked():
        layers = [
            l
            for l in QgsProject.instance().mapLayers().values()
            if l.type() == QgsVectorLayer.VectorLayer
        ]
        change_both_comboboxes(combobox1)
        change_both_comboboxes(combobox2)
