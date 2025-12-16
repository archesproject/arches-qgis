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

    if features:

        if len(features) > 1:
            print("Select one feature")
            dlg.editResSelectedResAttributeTable.setRowCount(0)
            if arches_api.arches_token:
                dlg.editResSelectedResId.setText(
                    "Multiple features selected, select one feature to proceed."
                )
            else:
                dlg.editResSelectedResId.setText(
                    "Connect to your Arches instance to edit resources."
                )
            return

        else:
            print("FEATURE SELECTED")
            for f in features:
                if "resourceinstanceid" in f.attributeMap():

                    # Initialise attribute table in the plugin window if the geom is recognised as an Arches res
                    # if initialised when arches_token exists then would have to click off and back on to recognise
                    no_rows = len(f.attributes())
                    no_cols = 2
                    dlg.editResSelectedResAttributeTable.setRowCount(no_rows)
                    dlg.editResSelectedResAttributeTable.setColumnCount(no_cols)

                    # Fill table with attributes
                    for i, (k, v) in enumerate(f.attributeMap().items()):
                        feat = QTableWidgetItem(str(k))
                        val = QTableWidgetItem(str(v))
                        dlg.editResSelectedResAttributeTable.setItem(i, 0, feat)
                        dlg.editResSelectedResAttributeTable.setItem(i, 1, val)
                        dlg.editResSelectedResAttributeTable.setRowHeight(i, 5)
                        # Store current resource info
                        if k == "resourceinstanceid":
                            arches_api.arches_selected_resource[
                                "resourceinstanceid"
                            ] = v
                        elif k == "nodeid":
                            arches_api.arches_selected_resource["nodeid"] = v
                        elif k == "tileid":
                            arches_api.arches_selected_resource["tileid"] = v

                    dlg.editResSelectedResAttributeTable.setHorizontalHeaderLabels(
                        ["Feature", "Values"]
                    )
                    dlg.editResSelectedResAttributeTable.resizeColumnsToContents()

                    # if the token exists then enable the UI elements
                    if arches_api.arches_token:
                        resource_string = "Resource: %s" % (f["resourceinstanceid"])
                        dlg.editResSelectedResId.setText(resource_string)
                        dlg.editResAddGeom.setEnabled(True)
                        dlg.editResReplaceGeom.setEnabled(True)

                        # Save resource instance details once selected
                    else:
                        dlg.editResSelectedResId.setText(
                            "Connect to your Arches instance to edit resources."
                        )
                        dlg.editResAddGeom.setEnabled(False)
                        dlg.editResReplaceGeom.setEnabled(False)

                else:
                    if arches_api.arches_token:
                        dlg.editResSelectedResId.setText(
                            "The feature selected is not an Arches resource."
                        )
                    else:
                        dlg.editResSelectedResId.setText(
                            "Connect to your Arches instance to edit resources."
                        )

    elif len(features) == 0:
        print("No feature selected")
        dlg.selectedResAttributeTable.setRowCount(0)
        if arches_api.arches_token:
            dlg.selectedResUUID.setText("Select a feature to proceed.")
            dlg.addEditRes.setEnabled(False)
            dlg.replaceEditRes.setEnabled(False)
        else:
            dlg.selectedResUUID.setText(
                "Connect to your Arches instance to edit resources."
            )
        return


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
