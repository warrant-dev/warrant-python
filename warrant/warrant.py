from warrant import APIResource, WarrantException


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


class Warrant(APIResource):

    def __init__(self, obj):
        self.object_type = obj["objectType"]
        self.object_id = obj["objectId"]
        self.relation = obj["relation"]
        self.subject = obj["subject"]

    @classmethod
    def create(cls, object_type, object_id, relation, subject, policy="", opts={}):
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
        return cls._post(uri="/v2/warrants", json=payload, opts=opts, object_hook=Warrant.from_json)

    @classmethod
    def batch_create(cls, warrants, opts={}):
        return cls._post(uri="/v2/warrants", json=warrants, opts=opts, object_hook=Warrant.from_json)

    @classmethod
    def query(cls, query, list_params={}, opts={}):
        params = {
            "q": query,
        } | list_params
        return cls._get(uri="/v2/query", params=params, opts=opts)

    @classmethod
    def delete(cls, object_type, object_id, relation, subject, policy="", opts={}):
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
        cls._delete(uri="/v2/warrants", json=payload, opts=opts)

    @classmethod
    def batch_delete(cls, warrants):
        cls._delete(uri="/v2/warrants", json=warrants)

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
