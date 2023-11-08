from warrant import APIResource, ListResult
from typing import Any, Dict, List, Optional


class WarrantObject(APIResource):
    def __init__(self, object_type: str, object_id: str, meta: Dict[str, Any] = {}) -> None:
        self.object_type = object_type
        self.object_id = object_id
        self.meta = meta

    @classmethod
    def list(cls, params: Dict[str, Any] = {}, opts: Dict[str, Any] = {}) -> ListResult["WarrantObject"]:
        if params is None:
            params = {}
        if opts is None:
            opts = {}
        list_result = cls._get(uri="/v2/objects", params=params, opts=opts, object_hook=WarrantObject.from_json)
        if "prevCursor" in list_result and "nextCursor" in list_result:
            return ListResult[WarrantObject](list_result['results'], list_result['prevCursor'], list_result['nextCursor'])
        elif "prevCursor" in list_result:
            return ListResult[WarrantObject](list_result['results'], list_result['prevCursor'])
        elif "nextCursor" in list_result:
            return ListResult[WarrantObject](list_result['results'], next_cursor=list_result['nextCursor'])
        else:
            return ListResult[WarrantObject](list_result['results'])

    @classmethod
    def create(cls, object_type: str, object_id: str = "", meta: Dict[str, Any] = {}, opts: Dict[str, Any] = {}) -> "WarrantObject":
        payload: Dict[str, Any] = {
            "objectType": object_type
        }
        if object_id is not None and object_id != "":
            payload["objectId"] = object_id
        if meta != {}:
            payload["meta"] = meta
        return cls._post(uri="/v2/objects", json_payload=payload, opts=opts, object_hook=WarrantObject.from_json)

    @classmethod
    def batch_create(cls, objects: List[Dict[str, Any]], opts: Dict[str, Any] = {}) -> List["WarrantObject"]:
        return cls._post(uri="/v2/objects", json_payload=objects, opts=opts, object_hook=WarrantObject.from_json)

    @classmethod
    def get(cls, object_type: str, object_id: str, opts: Dict[str, Any] = {}) -> "WarrantObject":
        return cls._get("/v2/objects/"+object_type+"/"+object_id, params={}, opts=opts, object_hook=WarrantObject.from_json)

    def update(self, meta: Dict[str, Any], opts: Dict[str, Any] = {}) -> None:
        payload = {
            "meta": meta
        }
        updated_obj = self._put(uri="/v2/objects/"+self.object_type+"/"+self.object_id, json_payload=payload, opts=opts, object_hook=WarrantObject.from_json)
        self.meta = updated_obj.meta

    @classmethod
    def delete(cls, object_type: str, object_id: str, opts: Dict[str, Any] = {}) -> Optional[str]:
        return cls._delete(uri="/v2/objects/"+object_type+"/"+object_id, params={}, opts=opts)

    @classmethod
    def batch_delete(cls, objects: List[Dict[str, Any]], opts: Dict[str, Any] = {}) -> Optional[str]:
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
