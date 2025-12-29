from qgis.PyQt.QtWidgets import QTableWidgetItem
from qgis.core import QgsProject, QgsVectorLayer

from arches_project.core.arches.api import arches_api


def map_selection(iface, dlg):
    """
    Feature selection from the QGIS map.
    """

    active_layer = iface.activeLayer()
    canvas = iface.mapCanvas()

    # If plugin is opened before QGIS project opened/setup selectedFeatures is None
    try:
        features = active_layer.selectedFeatures()
    except AttributeError:
        features = None

    print("\nmap selection has been fired because selection changed")
    print("layer:", active_layer, "features:", features)

    if arches_api.arches_token:
        if not features:
            default_text = "0 features selected. Select features from the map."
            dlg.createResFeatureLineEdit.setText(default_text)
            dlg.editResFeatureLineEdit.setText(default_text)
            dlg.editResSelectedResAttributeTable.setRowCount(0)
            dlg.editResAddGeom.setEnabled(False)
            dlg.editResReplaceGeom.setEnabled(False)
            dlg.createResButton.setEnabled(False)

        else:
            dlg.createResFeatureLineEdit.setText(f"{len(features)} features selected")
            dlg.createResButton.setEnabled(True)

            num_features_selected = f"{len(features)} features selected"
            dlg.createResFeatureLineEdit.setText(num_features_selected)
            dlg.editResFeatureLineEdit.setText(num_features_selected)

            arches_api.selected_features["features"].clear()  # reset list
            for feature in features:
                save_selected_features(feature, active_layer)

            # if len(features) > 1:
            #     # If features are greater than one, selected features can store but
            #     # selected Arches resource cannot

            #     dlg.editResSelectedResAttributeTable.setRowCount(0)

            # else:
            #     arches_api.selected_features["features"].clear()  # reset list

            #     for feature in features:

            #         save_selected_features(feature, active_layer)


def populate_table(dlg, feature):
    """
    Populate a QTableWidget with Arches resource attribute information.
    """
    # Initialise attribute table in the plugin window if the geom is recognised as an Arches res
    # if initialised when arches_token exists then would have to click off and back on to recognise
    no_rows = len(feature.attributes())
    no_cols = 2
    dlg.editResSelectedResAttributeTable.setRowCount(no_rows)
    dlg.editResSelectedResAttributeTable.setColumnCount(no_cols)

    # Fill table with attributes
    for i, (k, v) in enumerate(feature.attributeMap().items()):
        feat = QTableWidgetItem(str(k))
        val = QTableWidgetItem(str(v))
        dlg.editResSelectedResAttributeTable.setItem(i, 0, feat)
        dlg.editResSelectedResAttributeTable.setItem(i, 1, val)
        dlg.editResSelectedResAttributeTable.setRowHeight(i, 5)
        # Store current resource info
        if k == "resourceinstanceid":
            arches_api.arches_selected_resource["resourceinstanceid"] = v
        elif k == "nodeid":
            arches_api.arches_selected_resource["nodeid"] = v
        elif k == "tileid":
            arches_api.arches_selected_resource["tileid"] = v

    dlg.editResSelectedResAttributeTable.setHorizontalHeaderLabels(
        ["Feature", "Values"]
    )
    dlg.editResSelectedResAttributeTable.resizeColumnsToContents()

    # enable the UI elements
    dlg.editResAddGeom.setEnabled(True)
    dlg.editResReplaceGeom.setEnabled(True)


def save_selected_arches_resource(feature):
    # TODO check if nodeid and tileid are in the feature too, the three markers for checking it's an Arches resource
    if "resourceinstanceid" in feature.attributeMap():
        # TODO remove loop and get values from attributes
        for k, v in feature.attributeMap().items():
            # Store current resource info
            if k == "resourceinstanceid":
                arches_api.arches_selected_resource["resourceinstanceid"] = v
            elif k == "nodeid":
                arches_api.arches_selected_resource["nodeid"] = v
            elif k == "tileid":
                arches_api.arches_selected_resource["tileid"] = v
        return True
    else:
        return False


def save_selected_features(feature, active_layer):
    arches_api.selected_features["features"].append(feature)
    arches_api.selected_features["layer_crs"] = active_layer.crs()


def update_map_layers(checkbox):
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

    if arches_api.layers != all_current_layers:
        arches_api.layers = all_current_layers
