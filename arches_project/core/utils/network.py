from functools import partial
from urllib.parse import urlencode

from qgis.core import QgsApplication, QgsNetworkAccessManager, QgsMessageLog, Qgis
from qgis.PyQt.QtNetwork import QNetworkReply

from PyQt5.QtCore import QUrl, pyqtSignal, QObject, QByteArray
from PyQt5.QtNetwork import QNetworkRequest


class ArchesRequester(QObject):
    complete_signal = pyqtSignal(str)

    def make_authenticated_request(
        self, target_url, config_id, method="GET", payload={}
    ):
        auth_manager = QgsApplication.authManager()

        available_configs = auth_manager.availableAuthMethodConfigs()
        request = QNetworkRequest(
            QUrl(f"{available_configs[config_id].uri()}{target_url}")
        )
        auth_manager.updateNetworkRequest(request, authcfg=config_id)
        network_manager = QgsNetworkAccessManager.instance()

        QgsMessageLog.logMessage(
            f"Making request to URI: {available_configs[config_id].uri()}{target_url}",
            "Arches Plugin",
            level=Qgis.Info,
        )

        if method == "GET":
            self.network_reply = network_manager.get(request)
        elif method == "POST":
            filtered_payload = {k: v for k, v in payload.items() if v is not None}
            body = QByteArray(urlencode(filtered_payload).encode("utf-8"))
            request.setHeader(
                QNetworkRequest.ContentTypeHeader, "application/x-www-form-urlencoded"
            )
            self.network_reply = network_manager.post(request, body)

        handler = partial(self.handle_network_reply, self.network_reply, config_id)
        self.network_reply.finished.connect(handler)

    def handle_network_reply(self, reply, config_id):

        if reply.error() == QNetworkReply.AuthenticationRequiredError:
            QgsMessageLog.logMessage(
                f"Authentication required (OAuth flow should initiate automatically now if not already in progress).",
                "Arches Plugin",
                level=Qgis.Info,
            )

            # QGIS typically handles the authentication dialog internally when this error occurs
            # as part of the updateNetworkRequest call. If it fails here, the process stops.

        elif reply.error() == QNetworkReply.NoError:
            QgsMessageLog.logMessage(
                "Reply contained no error, request complete",
                "Arches Plugin",
                level=Qgis.Info,
            )
            data = reply.readAll().data().decode("utf-8")
            self.complete_signal.emit(data)
        else:
            error_string = reply.errorString()
            error_message = f"Network Error: {error_string}"
            QgsMessageLog.logMessage(error_message, "Arches Plugin", level=Qgis.Warning)

            self.complete_signal.emit(error_message)

        reply.deleteLater()
