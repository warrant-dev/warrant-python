import warrant
from warrant import APIResource


class Authz(APIResource):

    @classmethod
    def check(cls, object_type, object_id, relation, subject, context={}):
        warrantToCheck = {
            "objectType": object_type,
            "objectId": object_id,
            "relation": relation,
            "subject": {
                "objectType": subject.object_type,
                "objectId": subject.object_id,
                "relation": subject.relation
            },
            "context": context
        }
        payload = {
            "op": "anyOf",
            "warrants": [warrantToCheck]
        }
        json_resp = cls._post(uri="/v2/authorize", json=payload)
        code = json_resp["code"]
        result = json_resp["result"]
        if result == "Authorized" and code == 200:
            return True
        return False

    @classmethod
    def create_authorization_session(cls, user_id):
        payload = {
            "type": "sess",
            "userId": user_id
        }
        json = cls._post(uri="/v1/sessions", json=payload)
        return json["token"]

    @classmethod
    def create_self_service_url(cls, tenant_id, user_id, self_service_strategy, redirect_url):
        payload = {
            "type": "ssdash",
            "userId": user_id,
            "tenantId": tenant_id,
            "selfServiceStrategy": self_service_strategy,
        }
        json = cls._post(uri="/v1/sessions", json=payload)
        token = json["token"]
        return f"{warrant.self_service_dashboard_base_url}/{token}?redirectUrl={redirect_url}"
