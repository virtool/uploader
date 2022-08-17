from requests.auth import HTTPBasicAuth
import requests


def authenticate(url, user_handle, api_key):
    auth = HTTPBasicAuth(user_handle, api_key)
    result = requests.get(url, auth=auth, params={"type": "reads"})
    if result.status_code == 401:
        print("Invalid authorization: double check the provided API key and associated username")
        exit()
    return auth
