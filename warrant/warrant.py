from warrant import APIResource, WarrantException, ListResult
from typing import Any, Dict, List, Optional

class Subject(object):
    def __init__(self, object_type, object_id, relation=""):
        self.object_type = object_type
        self.object_id = object_id
        self.relation = relation

    """
    JSON serialization/deserialization
    """
    @staticmethod
    def from_json(obj):
        relation = ""
        if "relation" in obj.keys():
            relation = obj["relation"]
        return Subject(obj["objectType"], obj["objectId"], relation)


class QueryResult:
    def __init__(self, object_type: str, object_id: str, warrant: Dict[str, Any], is_implicit: bool, meta: Dict[str, Any] = {}):
        self.object_type = object_type
        self.object_id = object_id
        self.warrant = warrant
        self.is_implicit = is_implicit
        self.meta = meta

    @staticmethod
    def from_json(obj):
        print(f"queryResult obj: {obj}")
        if "objectType" in obj and "objectId" and "warrant" in obj:
            if "meta" in obj:
                return QueryResult(obj["objectType"], obj["objectId"], obj["warrant"], obj["isImplicit"], obj["meta"])
            else:
                return QueryResult(obj["objectType"], obj["objectId"], obj["warrant"], obj["isImplicit"])
        else:
            return obj



class Warrant(APIResource):
    object_type: str
    object_id: str
    relation: str
    subject: Subject
    warrant_token: Optional[str]

    def __init__(self, obj):
        self.object_type = obj["objectType"]
        self.object_id = obj["objectId"]
        self.relation = obj["relation"]
        self.subject = obj["subject"]
        self.warrant_token = obj["warrantToken"]

    @classmethod
    def create(cls, object_type, object_id, relation, subject, policy="", opts: Dict[str, Any] = {}) -> "Warrant":
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
            payload["subject"] = subject
        if policy != "":
            payload["policy"] = policy
        return cls._post(uri="/v2/warrants", json_payload=payload, opts=opts, object_hook=Warrant.from_json)

    @classmethod
    def batch_create(cls, warrants, opts: Dict[str, Any] = {}):
        return cls._post(uri="/v2/warrants", json_payload=warrants, opts=opts, object_hook=Warrant.from_json)

    @classmethod
    def query(cls, query, list_params={}, opts: Dict[str, Any] = {}) -> ListResult[QueryResult]:
        params = {
            "q": query,
        } | list_params
        query_result = cls._get(uri="/v2/query", params=params, opts=opts, object_hook=QueryResult.from_json)
        print(f"queryResult: {query_result}")
        if "prevCursor" in query_result and "nextCursor" in query_result:
            return ListResult[QueryResult](query_result['results'], query_result['prevCursor'], query_result['nextCursor'])
        elif "prevCursor" in query_result:
            return ListResult[QueryResult](query_result['results'], query_result['prevCursor'])
        elif "nextCursor" in query_result:
            return ListResult[QueryResult](query_result['results'], next_cursor=query_result['nextCursor'])
        else:
            return ListResult[QueryResult](query_result['results'])

    @classmethod
    def delete(cls, object_type, object_id, relation, subject, policy="", opts: Dict[str, Any] = {}):
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
            payload["subject"] = subject
        if policy != "":
            payload["policy"] = policy
        return cls._delete(uri="/v2/warrants", json=payload, opts=opts)

    @classmethod
    def batch_delete(cls, warrants):
        return cls._delete(uri="/v2/warrants", json=warrants)

    """
    JSON serialization/deserialization
    """
    @staticmethod
    def from_json(obj):
        if "subject" not in obj:
            # Inside 'subject' attr, serialize accordingly:
            return Subject.from_json(obj)
        else:
            return Warrant(obj)
