from qgis.PyQt.QtWidgets import QTableWidgetItem
from qgis.core import QgsProject, QgsVectorLayer, QgsMessageLog, Qgis

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

    QgsMessageLog.logMessage(
        "Map selection has been fired because selection changed",
        "Arches Plugin",
        level=Qgis.Info,
    )
    QgsMessageLog.logMessage(
        f"layer: {str(active_layer)}, features: {str(features)}",
        "Arches Plugin",
        level=Qgis.Info,
    )

    if features:
        if len(features) > 1:
            QgsMessageLog.logMessage(
                "Select one feature",
                "Arches Plugin",
                level=Qgis.Info,
            )
            dlg.selectedResAttributeTable.setRowCount(0)
            if arches_api.arches_user_info:
                dlg.selectedResUUID.setText(
                    "Multiple features selected, select one feature to proceed."
                )
            else:
                dlg.selectedResUUID.setText(
                    "Connect to your Arches instance to edit resources."
                )
            return

        elif len(features) == 0:
            QgsMessageLog.logMessage(
                "No feature selected",
                "Arches Plugin",
                level=Qgis.Info,
            )
            dlg.selectedResAttributeTable.setRowCount(0)
            if arches_api.arches_user_info:
                dlg.selectedResUUID.setText("Select a feature to proceed.")
                dlg.addEditRes.setEnabled(False)
                dlg.replaceEditRes.setEnabled(False)
            else:
                dlg.selectedResUUID.setText(
                    "Connect to your Arches instance to edit resources."
                )
            return

        else:
            QgsMessageLog.logMessage(
                "A feature was selected",
                "Arches Plugin",
                level=Qgis.Info,
            )
            for f in features:
                if "resourceinstanceid" in f.attributeMap():

                    # Initialise attribute table in the plugin window if the geom is recognised as an Arches res
                    # if initialised when arches_user_info exists then would have to click off and back on to recognise
                    no_rows = len(f.attributes())
                    no_cols = 2
                    dlg.selectedResAttributeTable.setRowCount(no_rows)
                    dlg.selectedResAttributeTable.setColumnCount(no_cols)

                    # Fill table with attributes
                    for i, (k, v) in enumerate(f.attributeMap().items()):
                        feat = QTableWidgetItem(str(k))
                        val = QTableWidgetItem(str(v))
                        dlg.selectedResAttributeTable.setItem(i, 0, feat)
                        dlg.selectedResAttributeTable.setItem(i, 1, val)
                        dlg.selectedResAttributeTable.setRowHeight(i, 5)
                        # Store current resource info
                        if k == "resourceinstanceid":
                            arches_api.arches_selected_resource[
                                "resourceinstanceid"
                            ] = v
                        elif k == "nodeid":
                            arches_api.arches_selected_resource["nodeid"] = v
                        elif k == "tileid":
                            arches_api.arches_selected_resource["tileid"] = v

                    dlg.selectedResAttributeTable.setHorizontalHeaderLabels(
                        ["Feature", "Values"]
                    )
                    dlg.selectedResAttributeTable.resizeColumnsToContents()

                    # if the arches_user_info exists then enable the UI elements
                    if arches_api.arches_user_info:
                        resource_string = "Resource: %s" % (f["resourceinstanceid"])
                        dlg.selectedResUUID.setText(resource_string)
                        dlg.addEditRes.setEnabled(True)
                        dlg.replaceEditRes.setEnabled(True)

                        # Save resource instance details once selected
                    else:
                        dlg.selectedResUUID.setText(
                            "Connect to your Arches instance to edit resources."
                        )
                        dlg.addEditRes.setEnabled(False)
                        dlg.replaceEditRes.setEnabled(False)

                else:
                    if arches_api.arches_user_info:
                        dlg.selectedResUUID.setText(
                            "The feature selected is not an Arches resource."
                        )
                    else:
                        dlg.selectedResUUID.setText(
                            "Connect to your Arches instance to edit resources."
                        )


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
