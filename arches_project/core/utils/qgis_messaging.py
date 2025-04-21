from qgis.core import Qgis


def show_message(iface, status, message, duration=5, level=Qgis.Info):
    """
    A simple function for consistent formatting of messages.
    """

    level_lookup = {
        "information": Qgis.Info, # Level 0
        "warning": Qgis.Warning, # Level 1
        "error": Qgis.Critical, # Level 2
        "success": Qgis.Success, # Level 3
    }
    # Use duration -1 for a message that must be dismissed by the user.

    try:
        level = level_lookup[status.lower().strip()]
    except KeyError:
        pass

    iface.messageBar().pushMessage(status, message, level=level, duration=duration)
