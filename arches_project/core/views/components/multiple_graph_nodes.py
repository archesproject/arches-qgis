from arches_project.core.arches.api import arches_api


def multiple_geometry_node_check(dlg):
    selectedGraphIndex = dlg.createResModelSelect.currentIndex()
    selectedGraph = arches_api.arches_graphs_list[selectedGraphIndex]

    geometry_nodes = []
    dlg.geometryNodeSelect.setEnabled(False)
    dlg.geometryNodeSelectFrame.hide()

    if selectedGraph:
        if selectedGraph["multiple_geometry_nodes"] == True:
            for k, v in selectedGraph["geometry_node_data"].items():
                geometry_nodes.append(
                    {
                        "node_id": k,
                        "nodegroup_id": v["nodegroup_id"],
                        "name": v["name"],
                    }
                )
            dlg.geometryNodeSelect.setEnabled(True)
            dlg.geometryNodeSelect.clear()
            dlg.geometryNodeSelect.addItems([n["name"] for n in geometry_nodes])
            dlg.geometryNodeSelectFrame.show()
