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
    def create(cls, object_type, object_id, relation, subject, policy=""):
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
        if policy != "":
            payload["policy"] = policy
        cls._post(uri="/v1/warrants", json=payload)

    @classmethod
    def query(cls, select, for_clause, where):
        params = {
            "select": select,
            "for": for_clause,
            "where": where,
        }
        return cls._get(uri="/v1/query", params=params, object_hook=Warrant.from_json)

    @classmethod
    def delete(cls, object_type, object_id, relation, subject, policy=""):
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
        if policy != "":
            payload["policy"] = policy
        cls._delete(uri="/v1/warrants", json=payload)

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
