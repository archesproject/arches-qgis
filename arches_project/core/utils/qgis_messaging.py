from qgis.core import Qgis


def show_message(iface, status, message, duration=5, level=Qgis.Info):
    level_lookup = {
        "information": Qgis.Info, # Level 0
        "warning": Qgis.Warning, # Level 1
        "error": Qgis.Critical, # Level 2
        "success": Qgis.Success, # Level 3
    }

    try:
        level = level_lookup[status.lower().strip()]
    except KeyError:
        pass

    iface.messageBar().pushMessage(status, message, level=level, duration=duration)
