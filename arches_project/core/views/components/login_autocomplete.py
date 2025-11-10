from arches_project.widgets.hover_list_view import HoverListView

from PyQt5.QtCore import Qt
from qgis.PyQt.QtWidgets import QCompleter
from qgis.PyQt.QtCore import QSettings

def load_saved_credentials(dlg):
        """Loads saved urls and usernames to the autocomplete"""
        saved_urls = QSettings().value("urls", [])
        saved_usernames = QSettings().value("usernames", [])

        if len(saved_urls) > 0:
            arches_server_completer = QCompleter(saved_urls, dlg.archesServerInput)
            arches_server_completer.setCaseSensitivity(Qt.CaseInsensitive)
            arches_server_completer.setCompletionMode(QCompleter.PopupCompletion)
            dlg.archesServerInput.setCompleter(arches_server_completer)

            arches_server_hover_popup = HoverListView()
            arches_server_completer.setPopup(arches_server_hover_popup)

        if len(saved_usernames) > 0:
            username_completer = QCompleter(saved_usernames, dlg.usernameInput)
            username_completer.setCaseSensitivity(Qt.CaseInsensitive)
            username_completer.setCompletionMode(QCompleter.PopupCompletion)
            dlg.usernameInput.setCompleter(username_completer)

            username_hover_popup = HoverListView()
            username_completer.setPopup(username_hover_popup)