def geometry_conversion(selectedLayer):
    """
    Convert QGIS geometries into Arches
    """

    # TODO: QGIS stores all polygons named as multipolygons even though they're separate and 
    # all multipoints as individual multipoints - these should be separated 
    geom_and_count = {} # to store geom type and how many 

    # Find what type and how many we are dealing with
    # for feature in selectedLayer.getFeatures():
    #     geomtype = str(feature.geometry().type()).split(".")
    #     if geomtype[-1] not in geom_and_count:
    #         geom_and_count[geomtype[-1]] = 1
    #     else:
    #         geom_and_count[geomtype[-1]] += 1
    #     print(feature.geometry().asPolygon())

    # if "Polygon" in geom_and_count.keys():
    #     if geom_and_count["Polygon"] == 1:
    #         all_features = [feature.geometry().asWkt() for feature in selectedLayer.getFeatures()]
    #         combined_feature = (','.join(all_features))
    #         combined_feature = combined_feature.replace("MultiPolygon","Polygon")
    #         return combined_feature

    # Return info for the confirmation dialog text box
    geometry_type_dict = {}

    for feature in selectedLayer.getFeatures():
        geom = feature.geometry()
        geomtype = str(geom.type()).split(".")
        if geomtype[-1] not in geometry_type_dict:
            geometry_type_dict[geomtype[-1]] = 1
        else:
            geometry_type_dict[geomtype[-1]] += 1

    # Would use shapely to create GEOMETRYCOLLECTION but that'd require users to install the dependency themselves
    # this is the alternative        
    all_features = [feature.geometry().asWkt() for feature in selectedLayer.getFeatures()]
    geomcoll = "GEOMETRYCOLLECTION (%s)" % (','.join(all_features))
    
    return geomcoll, geometry_type_dict
