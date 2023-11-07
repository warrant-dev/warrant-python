import warrant
from warrant import APIResource, Subject
from enum import Enum
from typing import Any, Dict, List, Optional, Union

class CheckOp(str, Enum):
    ANY_OF = "anyOf"
    ALL_OF = "allOf"

class Authz(APIResource):

    @classmethod
    def check(cls, object_type: str, object_id: str, relation: str, subject, context: Dict[str, Any] = {}, opts: Dict[str, Any] = {}) -> bool:
        warrantToCheck = {
            "objectType": object_type,
            "objectId": object_id,
            "relation": relation,
            "context": context
        }
        if isinstance(subject, Subject):
            warrantToCheck["subject"] = {
                "objectType": subject.object_type,
                "objectId": subject.object_id,
                "relation": subject.relation
            }
        else:
            warrantToCheck["subject"] = subject
        payload = {
            "op": "anyOf",
            "warrants": [warrantToCheck]
        }
        json_resp = cls._post(uri="/v2/check", json_payload=payload, opts=opts)
        code = json_resp["code"]
        result = json_resp["result"]
        if result == "Authorized" and code == 200:
            return True
        return False

    @classmethod
    def check_many(cls, op: CheckOp, warrants: List[Dict[str, Any]], opts: Dict[str, Any] = {}):
        payload = {
            "op": op,
            "warrants": warrants
        }
        json_resp = cls._post(uri="/v2/check", json_payload=payload, opts=opts)
        code = json_resp["code"]
        result = json_resp["result"]
        if result == "Authorized" and code == 200:
            return True
        return False

    @classmethod
    def create_authorization_session(cls, user_id: str) -> str:
        payload = {
            "type": "sess",
            "userId": user_id
        }
        json = cls._post(uri="/v2/sessions", json_payload=payload)
        return json["token"]

    @classmethod
    def create_self_service_url(cls, tenant_id: str, user_id: str, self_service_strategy: str, redirect_url: str) -> str:
        payload = {
            "type": "ssdash",
            "userId": user_id,
            "tenantId": tenant_id,
            "selfServiceStrategy": self_service_strategy,
        }
        json = cls._post(uri="/v2/sessions", json_payload=payload)
        token = json["token"]
        return f"{warrant.self_service_dashboard_base_url}/{token}?redirectUrl={redirect_url}"
