from warrant import APIResource
import json

class WarrantObject(APIResource):
    def __init__(self, object_type, object_id, meta = None):
        self.object_type = object_type
        self.object_id = object_id
        if meta is None:
            self.meta = {}
        else:
            self.meta = meta

    @classmethod
    def list(cls, params={}):
        return cls._get(uri="/v2/objects", params=params, object_hook=WarrantObject.from_json)

    @classmethod
    def create(cls, object_type, object_id="", meta={}):
        payload = {
            "objectType": object_type
        }
        if object_id != "":
            payload["objectId"] = object_id
        if meta != {}:
            payload["meta"] = meta
        return cls._post(uri="/v2/objects", json=payload, object_hook=WarrantObject.from_json)

    @classmethod
    def get(cls, object_type, object_id):
        return cls._get("/v2/objects/"+object_type+"/"+object_id, params={}, object_hook=WarrantObject.from_json)

    def update(self, meta):
        payload = {
            "meta": meta
        }
        updated_obj = self._put(uri="/v2/objects/"+self.object_type+"/"+self.object_id, json=payload, object_hook=WarrantObject.from_json)
        self.meta = updated_obj.meta

    @classmethod
    def delete(cls, object_type, object_id):
        return cls._delete(uri="/v2/objects/"+object_type+"/"+object_id, params={})

    """
    JSON serialization/deserialization
    """
    @staticmethod
    def from_json(obj):
        if "objectType" in obj and "objectId" in obj:
            if "meta" in obj:
                return WarrantObject(obj["objectType"], obj["objectId"], obj["meta"])
            else:
                return WarrantObject(obj["objectType"], obj["objectId"])
        else:
            return obj
