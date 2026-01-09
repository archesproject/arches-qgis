class ArchesAPI:
    """
    Holds data fetched from the Arches API.
    """

    def __init__(self):
        """
        ARCHES PLUGIN SPECIFIC VARIABLES
        """
        # Cache connection details to prevent firing duplicate connections
        self.arches_connection_cache = {}
        # Store token data to avoid regenerating every connection
        self.arches_token = {}
        self.client_id = ""
        self.arches_graphs_list = []
        self.geometry_nodes = []  # for multiple in graph
        self.arches_user_info = {}
        # Store selected arches resource
        self.arches_selected_resource = {
            "resourceinstanceid": "",
            "nodeid": "",
            "tileid": "",
        }
        # Store selected features to send to Arches
        self.selected_features = {"features": [], "layer_crs": None}
        # TODO this only works with selections from a single layer (QGIS default), but won't work with
        # selections across layers - https://gis.stackexchange.com/questions/257474/select-features-from-different-vector-layers-at-once


# Create an instance of the Arches API class that can be used throughout the plugin.
arches_api = ArchesAPI()
