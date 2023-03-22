import requests
import warrant


class WarrantException(Exception):
    def __init__(self, msg, status_code=-1):
        if status_code == -1:
            message = 'Warrant error: ' + msg
        else:
            message = f"Warrant error: {status_code} " + msg
        super().__init__(message)


class APIResource(object):

    @classmethod
    def _get(cls, uri, params={}, object_hook=None):
        headers = {
            "User-Agent": warrant.user_agent
        }
        if warrant.api_key != "":
            headers["Authorization"] = "ApiKey " + warrant.api_key
        resp = requests.get(url=warrant.api_endpoint+uri, headers=headers, params=params)
        if resp.status_code == 200:
            return resp.json(object_hook=object_hook)
        else:
            raise WarrantException(msg=resp.text, status_code=resp.status_code)

    @classmethod
    def _post(cls, uri, json={}, object_hook=None):
        headers = {
            "User-Agent": warrant.user_agent
        }
        if warrant.api_key != "":
            headers["Authorization"] = "ApiKey " + warrant.api_key
        resp = requests.post(url=warrant.api_endpoint+uri, headers=headers, json=json)
        if resp.status_code == 200:
            return resp.json(object_hook=object_hook)
        else:
            raise WarrantException(msg=resp.text, status_code=resp.status_code)

    @classmethod
    def _put(cls, uri, json={}, object_hook=None):
        headers = {
            "User-Agent": warrant.user_agent
        }
        if warrant.api_key != "":
            headers["Authorization"] = "ApiKey " + warrant.api_key
        resp = requests.put(url=warrant.api_endpoint+uri, headers=headers, json=json)
        if resp.status_code == 200:
            resp.json(object_hook=object_hook)
        else:
            raise WarrantException(msg=resp.text, status_code=resp.status_code)

    @classmethod
    def _delete(cls, uri, params={}, json={}):
        headers = {
            "User-Agent": warrant.user_agent
        }
        if warrant.api_key != "":
            headers["Authorization"] = "ApiKey " + warrant.api_key
        resp = requests.delete(url=warrant.api_endpoint+uri, headers=headers, params=params, json=json)
        if resp.status_code != 200:
            raise WarrantException(msg=resp.text, status_code=resp.status_code)
