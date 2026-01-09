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

    if not features:
        reset_saved_selected_features()
        default_text = "0 features selected. Select features from the map."
        dlg.createResFeatureLineEdit.setText(default_text)
        dlg.editResFeatureLineEdit.setText(default_text)
        dlg.editResAddGeom.setEnabled(False)
        dlg.editResReplaceGeom.setEnabled(False)
        dlg.createResButton.setEnabled(False)

    else:
        num_features_selected = f"{len(features)} features selected"
        dlg.createResFeatureLineEdit.setText(num_features_selected)
        dlg.editResFeatureLineEdit.setText(num_features_selected)
        dlg.createResButton.setEnabled(True)
        dlg.editResAddGeom.setEnabled(True)
        dlg.editResReplaceGeom.setEnabled(True)

        arches_api.selected_features["features"].clear()  # reset list
        for feature in features:
            save_selected_features(feature, active_layer)


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

    dlg.editResSelectedResAttributeTable.setHorizontalHeaderLabels(
        ["Feature", "Values"]
    )
    dlg.editResSelectedResAttributeTable.resizeColumnsToContents()

    # enable the UI elements
    dlg.editResAddGeom.setEnabled(True)
    dlg.editResReplaceGeom.setEnabled(True)


def save_selected_arches_resource(feature):
    required_fields = ["resourceinstanceid", "nodeid", "tileid"]

    if set(required_fields).issubset(set(feature.attributeMap().keys())):
        # Store current resource info
        arches_api.arches_selected_resource["resourceinstanceid"] = (
            feature.attributeMap()["resourceinstanceid"]
        )
        arches_api.arches_selected_resource["nodeid"] = feature.attributeMap()["nodeid"]
        arches_api.arches_selected_resource["tileid"] = feature.attributeMap()["tileid"]
        return True
    else:
        return False


def save_selected_features(feature, active_layer):
    arches_api.selected_features["features"].append(feature)
    arches_api.selected_features["layer_crs"] = active_layer.crs()


def reset_saved_selected_features():
    arches_api.selected_features["features"].clear()
    arches_api.selected_features["layer_crs"] = None
