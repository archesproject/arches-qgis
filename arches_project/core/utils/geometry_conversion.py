from qgis.core import (QgsProject,
                       QgsCoordinateReferenceSystem,
                       QgsCoordinateTransform,
                       QgsCoordinateTransformContext,
                       )

class Geometries():
    def __init__(self, selectedLayer):
        self.selectedLayer = selectedLayer
        self.selected_layer_crs = selectedLayer.crs()
        self.arches_crs = QgsCoordinateReferenceSystem.fromEpsgId(4326)

    def coordinate_transform(self, geom):
        if self.selected_layer_crs != self.arches_crs:
            tr = QgsCoordinateTransform(self.selected_layer_crs,
                                                     self.arches_crs,
                                                     QgsProject.instance())
            
            geom.transform(tr)
            return geom
        else:
            return geom

    def geometry_conversion(self):
        """
        Convert QGIS geometries into Arches format
        """
        # Return info for the confirmation dialog text box
        geometry_type_dict = {}
        all_features = []

        for feature in self.selectedLayer.getFeatures():
            geom = feature.geometry()
            geom = self.coordinate_transform(geom)
            all_features.append(geom.asWkt())

            # Store types 
            geomtype = str(geom.type()).split(".")
            if geomtype[-1] not in geometry_type_dict:
                geometry_type_dict[geomtype[-1]] = 1
            else:
                geometry_type_dict[geomtype[-1]] += 1

        # Would use shapely to create GEOMETRYCOLLECTION but that'd require users to install the dependency themselves
        # this is the alternative        
        # all_features = [feature.geometry().asWkt() for feature in self.selectedLayer.getFeatures()] 
        # removed for conversion
        geomcoll = "GEOMETRYCOLLECTION (%s)" % (','.join(all_features))
        
        return geomcoll, geometry_type_dict
