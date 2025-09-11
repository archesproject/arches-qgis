from datetime import datetime, timedelta
import requests

def refresh_token(archesproject):
    arches_token = archesproject.arches_token

    try:
        files = {
        'grant_type': (None, "refresh_token"),
        'client_id': (None, archesproject.clientid),
        'refresh_token': (None, arches_token['refresh_token']),
        }

        response = requests.post(arches_token["formatted_url"] +"/o/token/", data=files, timeout=10)
        refreshed_token = response.json()

        arches_token["time"] = datetime.now()
        arches_token['access_token'] = refreshed_token['access_token']
        arches_token["refresh_token"] = refreshed_token["refresh_token"]
        arches_token["expires_at"] = arches_token["time"] + timedelta(seconds=refreshed_token["expires_in"])

        archesproject.arches_token = arches_token

    except Exception as e:
        print(f"Failed to get OAuth token: {e}")