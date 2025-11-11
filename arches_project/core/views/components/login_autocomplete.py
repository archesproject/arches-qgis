from arches_project.ui.widgets.hover_list_view import HoverListView

from PyQt5.QtCore import Qt
from qgis.PyQt.QtWidgets import QCompleter
from qgis.PyQt.QtCore import QSettings


def setup_completer(input_widget, saved_list):
    if len(saved_list) > 0:
        arches_server_completer = QCompleter(saved_list, input_widget)
        arches_server_completer.setCaseSensitivity(Qt.CaseInsensitive)
        arches_server_completer.setCompletionMode(QCompleter.PopupCompletion)
        input_widget.setCompleter(arches_server_completer)

        arches_server_hover_popup = HoverListView()
        arches_server_completer.setPopup(arches_server_hover_popup)


def load_saved_credentials(dlg):
    """Loads saved urls and usernames to the autocomplete"""
    saved_urls = QSettings().value("urls", [])
    saved_usernames = QSettings().value("usernames", [])

    setup_completer(dlg.archesServerInput, saved_urls)
    setup_completer(dlg.usernameInput, saved_usernames)
