class Geometries():
    def __init__(self, selectedLayer):
        self.selectedLayer = selectedLayer
        
    def geometry_conversion(self):
        """
        Convert QGIS geometries into Arches format
        """
        # Return info for the confirmation dialog text box
        geometry_type_dict = {}

        for feature in self.selectedLayer.getFeatures():
            geom = feature.geometry()
            geomtype = str(geom.type()).split(".")
            if geomtype[-1] not in geometry_type_dict:
                geometry_type_dict[geomtype[-1]] = 1
            else:
                geometry_type_dict[geomtype[-1]] += 1

        # Would use shapely to create GEOMETRYCOLLECTION but that'd require users to install the dependency themselves
        # this is the alternative        
        all_features = [feature.geometry().asWkt() for feature in self.selectedLayer.getFeatures()]
        geomcoll = "GEOMETRYCOLLECTION (%s)" % (','.join(all_features))
        
        return geomcoll, geometry_type_dict
