from qgis.PyQt.QtWidgets import QTableWidgetItem
from qgis.core import QgsProject, QgsVectorLayer

from arches_project.core.arches.api import arches_api


def map_selection(iface, dlg):
    """
    Get the Arches Resource from the map
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
            dlg.createResFeatureLineEdit.setText(
                "0 features selected. Select features from the map."
            )
            dlg.editResSelectedResAttributeTable.setRowCount(0)
            dlg.editResSelectedResId.setText("Select a feature to proceed.")
            dlg.editResAddGeom.setEnabled(False)
            dlg.editResReplaceGeom.setEnabled(False)

        else:
            dlg.createResFeatureLineEdit.setText(f"{len(features)} features selected")

            if len(features) > 1:
                # If features are greater than one, selected features can store but
                # selected Arches resource cannot

                print("Select one feature")
                dlg.editResSelectedResAttributeTable.setRowCount(0)
                dlg.editResSelectedResId.setText(
                    "Multiple features selected, select one feature to proceed."
                )

                dlg.createResFeatureLineEdit.setText(
                    f"{len(features)} features selected"
                )
                for feature in features:
                    save_selected_features(feature)

            else:
                # TODO does this fire for 0 as well?

                for feature in features:
                    save_arches_res = save_selected_arches_resource(feature)
                    if save_arches_res:
                        populate_table(dlg, feature)
                    else:
                        dlg.editResSelectedResId.setText(
                            "The feature selected is not an Arches resource."
                        )

                    save_selected_features(feature)


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
    resource_string = "Resource: %s" % (feature["resourceinstanceid"])
    dlg.editResSelectedResId.setText(resource_string)
    dlg.editResAddGeom.setEnabled(True)
    dlg.editResReplaceGeom.setEnabled(True)


def save_selected_arches_resource(feature):
    # TODO check if nodeid and tileid are in the feature too, the three markers for checking it's an Arches resource
    if "resourceinstanceid" in feature.attributeMap():
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


def save_selected_features(feature):
    arches_api.selected_geometries.append(feature.geometry())


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
