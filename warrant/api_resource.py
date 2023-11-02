import requests
import warrant
import json


class WarrantException(Exception):
    def __init__(self, msg, status_code=-1):
        if status_code == -1:
            message = 'Warrant error: ' + msg
        else:
            message = f"Warrant error: {status_code} " + msg
        super().__init__(message)


class APIResource(object):
    session = requests.Session()

    @classmethod
    def _get(cls, uri, params={}, opts={}, object_hook=None):
        headers = {
            "User-Agent": warrant.user_agent
        }
        if warrant.api_key != "":
            headers["Authorization"] = "ApiKey " + warrant.api_key
        if "Warrant-Token" in opts:
            headers["Warrant-Token"] = opts["Warrant-Token"]
        resp = APIResource.session.get(url=warrant.api_endpoint+uri, headers=headers, params=params)
        if resp.status_code == 200:
            return resp.json(object_hook=object_hook)
        else:
            raise WarrantException(msg=resp.text, status_code=resp.status_code)

    @classmethod
    def _post(cls, uri, json_payload={}, opts={}, object_hook=None):
        headers = {
            "User-Agent": warrant.user_agent
        }
        if warrant.api_key != "":
            headers["Authorization"] = "ApiKey " + warrant.api_key
        if "Warrant-Token" in opts:
            headers["Warrant-Token"] = opts["Warrant-Token"]
        resp = APIResource.session.post(url=warrant.api_endpoint+uri, headers=headers, json=json_payload)
        if resp.status_code == 200:
            resp_json = resp.json()
            if "Warrant-Token" in resp.headers.keys():
                if isinstance(resp_json, list):
                    for obj in resp_json:
                        obj["warrantToken"] = resp.headers["Warrant-Token"]
                else:
                    resp_json["warrantToken"] = resp.headers["Warrant-Token"]

            return json.loads(json.dumps(resp_json), object_hook=object_hook)
        else:
            raise WarrantException(msg=resp.text, status_code=resp.status_code)

    @classmethod
    def _put(cls, uri, json_payload={}, opts={}, object_hook=None):
        headers = {
            "User-Agent": warrant.user_agent
        }
        if warrant.api_key != "":
            headers["Authorization"] = "ApiKey " + warrant.api_key
        if "Warrant-Token" in opts:
            headers["Warrant-Token"] = opts["Warrant-Token"]
        resp = APIResource.session.put(url=warrant.api_endpoint+uri, headers=headers, json=json_payload)
        if resp.status_code == 200:
            resp_json = resp.json()
            if "Warrant-Token" in resp.headers.keys():
                if isinstance(resp_json, list):
                    for obj in resp_json:
                        obj["warrantToken"] = resp.headers["Warrant-Token"]
                else:
                    resp_json["warrantToken"] = resp.headers["Warrant-Token"]

            return json.loads(json.dumps(resp_json), object_hook=object_hook)
        else:
            raise WarrantException(msg=resp.text, status_code=resp.status_code)

    @classmethod
    def _delete(cls, uri, params={}, opts={}, json={}):
        headers = {
            "User-Agent": warrant.user_agent
        }
        if warrant.api_key != "":
            headers["Authorization"] = "ApiKey " + warrant.api_key
        if "Warrant-Token" in opts:
            headers["Warrant-Token"] = opts["Warrant-Token"]
        resp = APIResource.session.delete(url=warrant.api_endpoint+uri, headers=headers, params=params, json=json)
        if resp.status_code == 200:
            if "Warrant-Token" in resp.headers.keys():
                return resp.headers["Warrant-Token"]
        else:
            raise WarrantException(msg=resp.text, status_code=resp.status_code)
