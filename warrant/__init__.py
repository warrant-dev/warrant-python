import requests
import json

__version__ = "0.2.1"

API_ENDPOINT = "https://api.warrant.dev"
API_VERSION = "/v1"

class WarrantException(Exception):
    def __init__(self, msg, status_code=-1):
        if status_code == -1:
            message = 'Warrant error: ' + msg
        else:
            message = f"Warrant error: {status_code} " + msg
        super().__init__(message)

class User(object):
    def __init__(self, object_type, object_id, relation):
        self.objectType = object_type
        self.objectId = object_id
        self.relation = relation

class Warrant(object):
    def __init__(self, api_key):
        self._apiKey = api_key

    def _make_post_request(self, uri, json={}):
        headers = { "Authorization": "ApiKey " + self._apiKey }
        resp = requests.post(url = API_ENDPOINT+API_VERSION+uri, headers = headers, json = json)
        if resp.status_code == 200:
            return resp.json()
        else:
            raise WarrantException(msg=resp.text, status_code=resp.status_code)

    def _make_get_request(self, uri, params={}):
        headers = { "Authorization": "ApiKey " + self._apiKey }
        resp = requests.get(url = API_ENDPOINT+API_VERSION+uri, headers = headers, params = params)
        if resp.status_code == 200:
            return resp.json()
        else:
            raise WarrantException(msg=resp.text, status_code=resp.status_code)

    def create_user(self, user_id=""):
        if user_id == "":
            payload = {}
        else:
            payload = { "userId": user_id }
        json = self._make_post_request(uri="/users", json=payload)
        return json['userId']

    def create_tenant(self, tenant_id=""):
        if tenant_id == "":
            payload = {}
        else:
            payload = { "tenantId": tenant_id }
        json = self._make_post_request(uri="/tenants", json=payload)
        return json['tenantId']

    def create_session(self, user_id):
        if user_id == "":
            raise WarrantException(msg="Invalid userId provided")
        json = self._make_post_request(uri="/users/"+user_id+"/sessions")
        return json['token']

    def create_warrant(self, object_type, object_id, relation, user):
        if object_type == "" or object_id == "" or relation == "":
            raise WarrantException(msg="Invalid object_type, object_id and/or relation")
        payload = {
            "objectType": object_type,
            "objectId": object_id,
            "relation": relation
        }
        if isinstance(user, str):
            payload["user"] = { "userId": user }
        elif isinstance(user, User):
            payload["user"] = json.dumps(user.__dict__)
        else:
            raise WarrantException(msg="Invalid type for \'user\'. Must be of type User or str")
        resp = self._make_post_request(uri="/warrants", json=payload)
        return resp['id']

    def list_warrants(self, object_type="", object_id="", relation="", user_id=""):
        filters = {
            "objectType": object_type,
            "objectId": object_id,
            "relation": relation,
            "userId": user_id,
        }
        resp = self._make_get_request(uri="/warrants", params=filters)
        return resp

    def is_authorized(self, object_type, object_id, relation, user_to_check):
        if object_type == "" or object_id == "" or relation == "":
            raise WarrantException(msg="Invalid object_type, object_id and/or relation")
        payload = {
            "objectType": object_type,
            "objectId": object_id,
            "relation": relation
        }
        if isinstance(user_to_check, str):
            payload["user"] = { "userId": user_to_check }
        elif isinstance(user_to_check, User):
            payload["user"] = json.dumps(user_to_check.__dict__)
        else:
            raise WarrantException(msg="Invalid type for \'user_to_check\'. Must be of type User or str")
        headers = { "Authorization": "ApiKey " + self._apiKey }
        resp = requests.post(url = API_ENDPOINT+API_VERSION+"/authorize", headers = headers, json=payload)
        if resp.status_code == 200:
            return True
        elif resp.status_code == 401:
            return False
        else:
            raise WarrantException(msg=resp.text, status_code=resp.status_code)
