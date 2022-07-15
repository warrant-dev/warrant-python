import requests
import json

__version__ = "0.2.1"

API_ENDPOINT = "https://api.warrant.dev"

class WarrantException(Exception):
    def __init__(self, msg, status_code=-1):
        if status_code == -1:
            message = 'Warrant error: ' + msg
        else:
            message = f"Warrant error: {status_code} " + msg
        super().__init__(message)

class Subject(object):
    def __init__(self, object_type, object_id, relation=""):
        self.objectType = object_type
        self.objectId = object_id
        self.relation = relation

class Warrant(object):
    def __init__(self, object_type, object_id, relation, subject):
        self.objectType = object_type
        self.objectId = object_id
        self.relation = relation
        self.subject = subject

class WarrantCheck(object):
    def __init__(self, warrants, op):
        self.warrants = warrants
        self.op = op

class WarrantClient(object):
    def __init__(self, api_key):
        self._apiKey = api_key

    def _make_post_request(self, uri, json={}):
        headers = { "Authorization": "ApiKey " + self._apiKey }
        resp = requests.post(url = API_ENDPOINT+uri, headers = headers, json = json)
        if resp.status_code == 200:
            return resp.json()
        else:
            raise WarrantException(msg=resp.text, status_code=resp.status_code)

    def _make_get_request(self, uri, params={}):
        headers = { "Authorization": "ApiKey " + self._apiKey }
        resp = requests.get(url = API_ENDPOINT+uri, headers = headers, params = params)
        if resp.status_code == 200:
            return resp.json()
        else:
            raise WarrantException(msg=resp.text, status_code=resp.status_code)

    def _make_delete_request(self, uri, params={}):
        headers = { "Authorization": "ApiKey " + self._apiKey }
        resp = requests.delete(url = API_ENDPOINT+uri, headers = headers, params = params)
        if resp.status_code != 200:
            raise WarrantException(msg=resp.text, status_code=resp.status_code)

    def create_user(self, user_id="", email=""):
        if user_id == "":
            payload = {}
        else:
            payload = { "userId": user_id }
        if email != "":
            payload.update({ "email": email })
        json = self._make_post_request(uri="/v1/users", json=payload)
        return json['userId']

    def delete_user(self, user_id):
        if user_id == "":
            raise WarrantException(msg="Must include a userId")
        self._make_delete_request(uri="/v1/users/"+user_id)

    def create_tenant(self, tenant_id="", name=""):
        if tenant_id == "":
            payload = {}
        else:
            payload = { "tenantId": tenant_id }
        if name != "":
            payload.update({ "name": name })
        json = self._make_post_request(uri="/v1/tenants", json=payload)
        return json['tenantId']

    def delete_tenant(self, tenant_id):
        if tenant_id == "":
            raise WarrantException(msg="Must include a tenantId")
        self._make_delete_request(uri="/v1/tenants/"+tenant_id)

    def create_role(self, role_id):
        if role_id == "":
            raise WarrantException(msg="Must include a roleId")
        payload = { "roleId": role_id }
        json = self._make_post_request(uri="/v1/roles", json=payload)
        return json['roleId']

    def delete_role(self, role_id):
        if role_id == "":
            raise WarrantException(msg="Must include a roleId")
        self._make_delete_request(uri="/v1/roles/"+role_id)

    def create_permission(self, permission_id):
        if permission_id == "":
            raise WarrantException(msg="Must include a permissionId")
        payload = { "permissionId": permission_id }
        json = self._make_post_request(uri="/v1/permissions", json=payload)
        return json['permissionId']

    def delete_permission(self, permission_id):
        if permission_id == "":
            raise WarrantException(msg="Must include a permissionId")
        self._make_delete_request(uri="/v1/permissions/"+permission_id)

    def assign_role_to_user(self, user_id, role_id):
        if user_id == "" or role_id == "":
            raise WarrantException(msg="Must include a userId and roleId")
        json = self._make_post_request(uri="/v1/users/" + user_id + "/roles/" + role_id)
        return json['roleId']

    def remove_role_from_user(self, user_id, role_id):
        if user_id == "" or role_id == "":
            raise WarrantException(msg="Must include a userId and roleId")
        self._make_delete_request(uri="/v1/users/"+user_id+"/roles/"+role_id)

    def assign_permission_to_user(self, user_id, permission_id):
        if user_id == "" or permission_id == "":
            raise WarrantException(msg="Must include a userId and permissionId")
        json = self._make_post_request(uri="/v1/users/" + user_id + "/permissions/" + permission_id)
        return json['permissionId']

    def remove_permission_from_user(self, user_id, permission_id):
        if user_id == "" or permission_id == "":
            raise WarrantException(msg="Must include a userId and permissionId")
        self._make_delete_request(uri="/v1/users/"+user_id+"/permissions/"+permission_id)

    def assign_permission_to_role(self, role_id, permission_id):
        if role_id == "" or permission_id == "":
            raise WarrantException(msg="Must include a roleId and permissionId")
        json = self._make_post_request(uri="/v1/roles/" + role_id + "/permissions/" + permission_id)
        return json['permissionId']

    def remove_permission_from_role(self, role_id, permission_id):
        if role_id == "" or permission_id == "":
            raise WarrantException(msg="Must include a roleId and permissionId")
        self._make_delete_request(uri="/v1/roles/"+role_id+"/permissions/"+permission_id)

    def create_session(self, user_id):
        if user_id == "":
            raise WarrantException(msg="Invalid userId provided")
        payload = {
            "type": "sess",
            "userId": user_id
        }
        json = self._make_post_request(uri="/v1/sessions", json=payload)
        return json['token']

    def create_warrant(self, object_type, object_id, relation, subject):
        if object_type == "" or object_id == "" or relation == "":
            raise WarrantException(msg="Invalid object_type, object_id and/or relation")
        payload = {
            "objectType": object_type,
            "objectId": object_id,
            "relation": relation
        }
        if isinstance(subject, Subject):
            payload["subject"] = subject.__dict__
        else:
            raise WarrantException(msg="Invalid type for \'subject\'. Must be of type Subject")
        resp = self._make_post_request(uri="/v1/warrants", json=payload)
        return resp['id']

    def list_warrants(self, object_type="", object_id="", relation="", user_id=""):
        filters = {
            "objectType": object_type,
            "objectId": object_id,
            "relation": relation,
            "userId": user_id,
        }
        resp = self._make_get_request(uri="/v1/warrants", params=filters)
        return resp

    def is_authorized(self, warrant_check):
        if not isinstance(warrant_check.warrants, list):
            raise WarrantException(msg="Invalid list of warrants to check")
        payload = json.dumps(warrant_check, default = lambda x: x.__dict__)
        headers = { "Authorization": "ApiKey " + self._apiKey }
        resp = requests.post(url = API_ENDPOINT+"/v2/authorize", headers = headers, data=payload)
        if resp.status_code != 200:
            raise WarrantException(msg=resp.text, status_code=resp.status_code)
        response_payload = resp.json()
        result = response_payload['code']
        if result == 200:
            return True
        else:
            return False
