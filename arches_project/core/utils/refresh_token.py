from datetime import datetime, timedelta
import requests

def refresh_token(archesproject):

    try:
        files = {
        'grant_type': (None, "refresh_token"),
        'client_id': (None, archesproject.clientid),
        'refresh_token': (None, archesproject.arches_token['refresh_token']),
        }

        response = requests.post(archesproject.arches_token["formatted_url"] +"/o/token/", data=files, timeout=10)
        refreshed_token = response.json()

        archesproject.arches_token["time"] = datetime.now()
        archesproject.arches_token['access_token'] = refreshed_token['access_token']
        archesproject.arches_token["refresh_token"] = refreshed_token["refresh_token"]
        archesproject.arches_token["expires_at"] = archesproject.arches_token["time"] + timedelta(seconds=refreshed_token["expires_in"])

    except Exception as e:
        print(f"Failed to get OAuth token: {e}")