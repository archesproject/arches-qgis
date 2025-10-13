def missing_credentials(widget, invalid):
    """
    This turns labels, and widgets red when credentials are missing.
    Mainly used in the login view.
    Currently this only works on the Arches stylesheet.
    """
    widget.setProperty("missingCreds", invalid)
    widget.style().unpolish(widget)
    widget.style().polish(widget)
    widget.update()
