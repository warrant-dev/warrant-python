from warrant import APIResource

class WarrantObject(APIResource):
    def __init__(self, object_type, object_id, meta = None):
        self.object_type = object_type
        self.object_id = object_id
        if meta is None:
            self.meta = {}
        else:
            self.meta = meta

    @classmethod
    def list(cls, params={}, opts={}):
        return cls._get(uri="/v2/objects", params=params, opts=opts, object_hook=WarrantObject.from_json)

    @classmethod
    def create(cls, object_type, object_id="", meta={}, opts={}):
        payload = {
            "objectType": object_type
        }
        if object_id != "":
            payload["objectId"] = object_id
        if meta != {}:
            payload["meta"] = meta
        return cls._post(uri="/v2/objects", json=payload, opts=opts, object_hook=WarrantObject.from_json)

    @classmethod
    def batch_create(cls, objects, opts={}):
        return cls._post(uri="/v2/objects", json=objects, opts=opts, object_hook=WarrantObject.from_json)

    @classmethod
    def get(cls, object_type, object_id, opts={}):
        return cls._get("/v2/objects/"+object_type+"/"+object_id, params={}, opts=opts, object_hook=WarrantObject.from_json)

    def update(self, meta, opts={}):
        payload = {
            "meta": meta
        }
        updated_obj = self._put(uri="/v2/objects/"+self.object_type+"/"+self.object_id, json=payload, opts=opts, object_hook=WarrantObject.from_json)
        self.meta = updated_obj.meta

    @classmethod
    def delete(cls, object_type, object_id, opts={}):
        return cls._delete(uri="/v2/objects/"+object_type+"/"+object_id, params={}, opts=opts)

    @classmethod
    def batch_delete(cls, objects, opts={}):
        return cls._delete(uri="/v2/objects", json=objects, opts=opts)

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
