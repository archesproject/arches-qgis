from datetime import datetime
import requests

def refresh_token(archesproject):
    old_arches_token = archesproject.arches_token

    try:
        files = {
        'grant_type': (None, "refresh_token"),
        'client_id': (None, archesproject.clientid),
        'refresh_token': (None, old_arches_token['refresh_token']),
        }

        response = requests.post(old_arches_token["formatted_url"] +"/o/token/", data=files, timeout=10)
        new_arches_token = response.json()
        new_arches_token["formatted_url"] = old_arches_token['formatted_url']
        new_arches_token["time"] = str(datetime.now())

        archesproject.arches_token = new_arches_token

    except Exception as e:
        print(f"Token refresh failed: {e}")