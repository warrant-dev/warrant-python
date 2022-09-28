import requests
import json

__version__ = "0.2.2"

API_ENDPOINT = "https://api.warrant.dev"
SELF_SERVICE_DASHBOARD_BASE_URL = "https://self-serve.warrant.dev"

class WarrantException(Exception):
    def __init__(self, msg, status_code=-1):
        if status_code == -1:
            message = 'Warrant error: ' + msg
        else:
            message = f"Warrant error: {status_code} " + msg
        super().__init__(message)

class Subject(object):
    def __init__(self, object_type, object_id, relation=""):
        self.object_type = object_type
        self.object_id = object_id
        self.relation = relation

class Warrant(object):
    def __init__(self, object_type, object_id, relation, subject):
        self.object_type = object_type
        self.object_id = object_id
        self.relation = relation
        self.subject = subject

class WarrantCheck(object):
    def __init__(self, warrants, op):
        self.warrants = warrants
        self.op = op

class PermissionCheck(object):
    def __init__(self, permission_id, user_id):
        self.permission_id = permission_id
        self.user_id = user_id

class AuthorizationSession(object):
    def __init__(self, user_id):
        self.type = "sess"
        self.user_id = user_id

class SelfServiceSession(object):
    def __init__(self, user_id, tenant_id):
        self.type = "ssdash"
        self.user_id = user_id
        self.tenant_id = tenant_id

class WarrantClient(object):
    def __init__(self, api_key):
        self._api_key = api_key

    def _make_post_request(self, uri, json={}):
        headers = { "Authorization": "ApiKey " + self._api_key }
        resp = requests.post(url = API_ENDPOINT+uri, headers = headers, json = json)
        if resp.status_code == 200:
            return resp.json()
        else:
            raise WarrantException(msg=resp.text, status_code=resp.status_code)

    def _make_get_request(self, uri, params={}):
        headers = { "Authorization": "ApiKey " + self._api_key }
        resp = requests.get(url = API_ENDPOINT+uri, headers = headers, params = params)
        if resp.status_code == 200:
            return resp.json()
        else:
            raise WarrantException(msg=resp.text, status_code=resp.status_code)

    def _make_delete_request(self, uri, params={}):
        headers = { "Authorization": "ApiKey " + self._api_key }
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
            raise WarrantException(msg="Must include a user_id")
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
            raise WarrantException(msg="Must include a user_id and permission_id")
        json = self._make_post_request(uri="/v1/users/" + user_id + "/permissions/" + permission_id)
        return json['permissionId']

    def remove_permission_from_user(self, user_id, permission_id):
        if user_id == "" or permission_id == "":
            raise WarrantException(msg="Must include a user_id and permission_id")
        self._make_delete_request(uri="/v1/users/"+user_id+"/permissions/"+permission_id)

    def assign_permission_to_role(self, role_id, permission_id):
        if role_id == "" or permission_id == "":
            raise WarrantException(msg="Must include a role_id and permission_id")
        json = self._make_post_request(uri="/v1/roles/" + role_id + "/permissions/" + permission_id)
        return json['permissionId']

    def remove_permission_from_role(self, role_id, permission_id):
        if role_id == "" or permission_id == "":
            raise WarrantException(msg="Must include a role_id and permission_id")
        self._make_delete_request(uri="/v1/roles/"+role_id+"/permissions/"+permission_id)

    def create_authorization_session(self, session):
        if session.user_id == "":
            raise WarrantException(msg="Must include a user_id")
        if session.type != "sess":
            raise WarrantException(msg="Invalid type provided")
        payload = { "type": session.type, "userId": session.user_id }
        json = self._make_post_request(uri="/v1/sessions", json=payload)
        return json['token']

    def create_self_service_session(self, session, redirect_url):
        if session.tenant_id == "":
            raise WarrantException(msg="Must include a tenant_id")
        if session.user_id == "":
            raise WarrantException(msg="Must include a user_id")
        if session.type != "ssdash":
            raise WarrantException(msg="Invalid type provided")
        if redirect_url == "":
            raise WarrantException(msg="Must include a redirect_url")
        payload = { "type": session.type, "userId": session.user_id, "tenantId": session.tenant_id }
        json = self._make_post_request(uri="/v1/sessions", json=payload)
        return f"{SELF_SERVICE_DASHBOARD_BASE_URL}/{json['token']}?redirectUrl={redirect_url}"

    def create_warrant(self, object_type, object_id, relation, subject):
        if object_type == "" or object_id == "" or relation == "":
            raise WarrantException(msg="Must provide object_type, object_id, and relation")
        payload = {
            "objectType": object_type,
            "objectId": object_id,
            "relation": relation
        }
        if isinstance(subject, Subject):
            payload["subject"] = {
                "objectType": subject.object_type,
                "objectId": subject.object_id,
                "relation": subject.relation
            }
        else:
            raise WarrantException(msg="Invalid type for \'subject\'. Must be of type Subject")
        resp = self._make_post_request(uri="/v1/warrants", json=payload)
        return resp

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
            raise WarrantException(msg="Must provide a list of warrants")
        payload = {
            "op": warrant_check.op,
            "warrants": list(map(lambda wnt: {
                "objectType": wnt.object_type,
                "objectId": wnt.object_id,
                "relation": wnt.relation,
                "subject": {
                    "objectType": wnt.subject.object_type,
                    "objectId": wnt.subject.object_id,
                    "relation": wnt.subject.relation
                }
            }, warrant_check.warrants))
        }
        headers = { "Authorization": "ApiKey " + self._api_key }
        resp = requests.post(url=API_ENDPOINT+"/v2/authorize", headers=headers, json=payload)
        if resp.status_code != 200:
            raise WarrantException(msg=resp.text, status_code=resp.status_code)
        response_payload = resp.json()
        result = response_payload['code']
        if result == 200:
            return True
        else:
            return False

    def has_permission(self, permission_check):
        return self.is_authorized({
            warrants: [{
                object_type: "permission",
                object_id: permission_check.permission_id,
                relation: "member",
                subject: {
                    object_type: "user",
                    object_id: permission_check.user_id
                }
            }]
        })
