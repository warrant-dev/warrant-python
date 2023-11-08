from warrant import APIResource, Subject, Warrant, WarrantObject, constants, ListResult
from typing import Any, Dict, List, Optional


class Permission(WarrantObject):
    def __init__(self, id: str = "", meta: Dict[str, Any] = {}) -> None:
        self.id = id
        WarrantObject.__init__(self, "permission", id, meta)

    @classmethod
    def list(cls, list_params: Dict[str, Any] = {}, opts: Dict[str, Any] = {}):
        list_params['objectType'] = 'permission'
        list_result = WarrantObject.list(list_params, opts=opts)
        permissions = map(lambda warrant_obj: Permission(warrant_obj.object_id, warrant_obj.meta), list_result.results)
        if list_result.prev_cursor != "" and list_result.next_cursor != "":
            return ListResult[Permission](list(permissions), list_result.prev_cursor, list_result.next_cursor)
        elif list_result.prev_cursor != "":
            return ListResult[Permission](list(permissions), list_result.prev_cursor)
        elif list_result.next_cursor != "":
            return ListResult[Permission](list(permissions), next_cursor=list_result.next_cursor)
        else:
            return ListResult[Permission](list(permissions))

    @classmethod
    def get(cls, id: str, opts: Dict[str, Any] = {}) -> "Permission":
        warrant_obj = WarrantObject.get("permission", id, opts=opts)
        return Permission.from_warrant_obj(warrant_obj)

    @classmethod
    def create(cls, id: str, meta={}, opts: Dict[str, Any] = {}) -> "Permission":
        warrant_obj = WarrantObject.create("permission", id, meta, opts=opts)
        return Permission.from_warrant_obj(warrant_obj)

    @classmethod
    def delete(cls, id: str, opts: Dict[str, Any] = {}) -> Optional[str]:
        return WarrantObject.delete("permission", id, opts=opts)

    """
    Users
    """
    @classmethod
    def list_for_user(cls, user_id: str, list_params: Dict[str, Any] = {}, opts: Dict[str, Any] = {}) -> ListResult["Permission"]:
        query_result = Warrant.query("select permission where user:"+user_id+" is *", list_params, opts=opts)
        permissions = map(lambda warrant_obj: Permission(warrant_obj.object_id, warrant_obj.meta), query_result.results)
        if query_result.prev_cursor != "" and query_result.next_cursor != "":
            return ListResult[Permission](list(permissions), query_result.prev_cursor, query_result.next_cursor)
        elif query_result.prev_cursor != "":
            return ListResult[Permission](list(permissions), query_result.prev_cursor)
        elif query_result.next_cursor != "":
            return ListResult[Permission](list(permissions), next_cursor=query_result.next_cursor)
        else:
            return ListResult[Permission](list(permissions))

    @classmethod
    def assign_to_user(cls, user_id: str, permission_id: str, relation: str, opts: Dict[str, Any] = {}):
        user_subject = Subject(constants.USER_OBJECT_TYPE, user_id)
        return Warrant.create(constants.PERMISSION_OBJECT_TYPE, permission_id, relation, user_subject, opts=opts)

    @classmethod
    def remove_from_user(cls, user_id: str, permission_id: str, relation: str, opts: Dict[str, Any] = {}):
        user_subject = Subject(constants.USER_OBJECT_TYPE, user_id)
        return Warrant.delete(constants.PERMISSION_OBJECT_TYPE, permission_id, relation, user_subject, opts=opts)

    """
    Roles
    """
    @classmethod
    def list_for_role(cls, role_id: str, list_params: Dict[str, Any] = {}, opts: Dict[str, Any] = {}) -> ListResult["Permission"]:
        query_result = Warrant.query("select permission where role:"+role_id+" is *", list_params, opts=opts)
        permissions = map(lambda warrant_obj: Permission(warrant_obj.object_id, warrant_obj.meta), query_result.results)
        if query_result.prev_cursor != "" and query_result.next_cursor != "":
            return ListResult[Permission](list(permissions), query_result.prev_cursor, query_result.next_cursor)
        elif query_result.prev_cursor != "":
            return ListResult[Permission](list(permissions), query_result.prev_cursor)
        elif query_result.next_cursor != "":
            return ListResult[Permission](list(permissions), next_cursor=query_result.next_cursor)
        else:
            return ListResult[Permission](list(permissions))

    @classmethod
    def assign_to_role(cls, role_id: str, permission_id: str, relation: str, opts: Dict[str, Any] = {}):
        role_subject = Subject(constants.ROLE_OBJECT_TYPE, role_id)
        return Warrant.create(constants.PERMISSION_OBJECT_TYPE, permission_id, relation, role_subject, opts=opts)

    @classmethod
    def remove_from_role(cls, role_id: str, permission_id: str, relation: str, opts: Dict[str, Any] = {}):
        role_subject = Subject(constants.ROLE_OBJECT_TYPE, role_id)
        return Warrant.delete(constants.PERMISSION_OBJECT_TYPE, permission_id, relation, role_subject, opts=opts)

    """
    JSON serialization/deserialization
    """
    @staticmethod
    def from_warrant_obj(obj):
        return Permission(obj.object_id, obj.meta)

    @staticmethod
    def from_json(obj):
        if "objectType" in obj and "objectId" in obj:
            if "meta" in obj:
                return Permission(obj["objectId"], obj["meta"])
            else:
                return Permission(obj["objectId"])
        else:
            return obj
