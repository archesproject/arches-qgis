from datetime import datetime, timedelta
import requests

from arches_project.core.arches.api import arches_api


def refresh_token():

    try:
        files = {
            "grant_type": (None, "refresh_token"),
            "client_id": (None, arches_api.clientid),
            "refresh_token": (None, arches_api.arches_token["refresh_token"]),
        }

        response = requests.post(
            arches_api.arches_token["formatted_url"] + "/o/token/",
            data=files,
            timeout=10,
        )
        refreshed_token = response.json()

        arches_api.arches_token["time"] = datetime.now()
        arches_api.arches_token["access_token"] = refreshed_token["access_token"]
        arches_api.arches_token["refresh_token"] = refreshed_token["refresh_token"]
        arches_api.arches_token["expires_at"] = arches_api.arches_token[
            "time"
        ] + timedelta(seconds=refreshed_token["expires_in"])

    except Exception as e:
        print(f"Failed to get OAuth token: {e}")
