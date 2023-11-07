from warrant import APIResource, Permission, Subject, Warrant, WarrantObject, constants, ListResult
from typing import Any, Dict, List, Optional


class Role(WarrantObject):
    def __init__(self, id: str = "", meta: Dict[str, Any] = {}) -> None:
        self.id = id
        WarrantObject.__init__(self, "role", id, meta)

    @classmethod
    def list(cls, list_params: Dict[str, Any] = {}, opts: Dict[str, Any] = {}):
        list_params['objectType'] = 'role'
        list_result = WarrantObject.list(list_params, opts=opts)
        roles = map(lambda warrant_obj: Role(warrant_obj.object_id, warrant_obj.meta), list_result.results)
        if list_result.prev_cursor != "" and list_result.next_cursor != "":
            return ListResult[Role](list(roles), list_result.prev_cursor, list_result.next_cursor)
        elif list_result.prev_cursor != "":
            return ListResult[Role](list(roles), list_result.prev_cursor)
        elif list_result.next_cursor != "":
            return ListResult[Role](list(roles), next_cursor=list_result.next_cursor)
        else:
            return ListResult[Role](list(roles))

    @classmethod
    def get(cls, id: str, opts: Dict[str, Any] = {}) -> "Role":
        warrant_obj = WarrantObject.get("role", id, opts=opts)
        return Role.from_warrant_obj(warrant_obj)

    @classmethod
    def create(cls, id: str = "", meta: Dict[str, Any] = {}, opts: Dict[str, Any] = {}) -> "Role":
        warrant_obj = WarrantObject.create("role", id, meta, opts=opts)
        return Role.from_warrant_obj(warrant_obj)

    @classmethod
    def delete(cls, id: str, opts: Dict[str, Any] = {}) -> Optional[str]:
        return WarrantObject.delete("role", id, opts=opts)

    """
    Users
    """
    @classmethod
    def list_for_user(cls, user_id: str, list_params: Dict[str, Any] = {}, opts: Dict[str, Any] = {}) -> ListResult["Role"]:
        query_result = Warrant.query("select role where user:"+user_id+" is *", list_params, opts=opts)
        roles = map(lambda warrant_obj: Role(warrant_obj.object_id, warrant_obj.meta), query_result.results)
        if query_result.prev_cursor != "" and query_result.next_cursor != "":
            return ListResult[Role](list(roles), query_result.prev_cursor, query_result.next_cursor)
        elif query_result.prev_cursor != "":
            return ListResult[Role](list(roles), query_result.prev_cursor)
        elif query_result.next_cursor != "":
            return ListResult[Role](list(roles), next_cursor=query_result.next_cursor)
        else:
            return ListResult[Role](list(roles))

    @classmethod
    def assign_to_user(cls, user_id: str, role_id: str, relation: str, opts: Dict[str, Any] = {}):
        user_subject = Subject(constants.USER_OBJECT_TYPE, user_id)
        return Warrant.create(constants.ROLE_OBJECT_TYPE, role_id, relation, user_subject, opts=opts)

    @classmethod
    def remove_from_user(cls, user_id: str, role_id: str, relation: str, opts: Dict[str, Any] = {}):
        user_subject = Subject(constants.USER_OBJECT_TYPE, user_id)
        return Warrant.delete(constants.ROLE_OBJECT_TYPE, role_id, relation, user_subject, opts=opts)

    """
    Permissions
    """
    def list_permissions(self, list_params: Dict[str, Any] = {}, opts: Dict[str, Any] = {}) -> ListResult["Permission"]:
        return Permission.list_for_role(self.id, list_params, opts=opts)

    def assign_permission(self, permission_id: str, relation: str, opts: Dict[str, Any] = {}):
        Permission.assign_to_role(self.id, permission_id, relation, opts=opts)

    def remove_permission(self, permission_id: str, relation: str, opts: Dict[str, Any] = {}):
        Permission.remove_from_role(self.id, permission_id, relation, opts=opts)

    """
    JSON serialization/deserialization
    """
    @staticmethod
    def from_warrant_obj(obj):
        return Role(obj.object_id, obj.meta)

    @staticmethod
    def from_json(obj):
        if "objectType" in obj and "objectId" in obj:
            if "meta" in obj:
                return Role(obj["objectId"], obj["meta"])
            else:
                return Role(obj["objectId"])
        else:
            return obj
