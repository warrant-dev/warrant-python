from warrant import APIResource, PricingTier, Feature, Role, Permission, Authz, Subject, Warrant, Object, constants, ListResult
from typing import Any, Dict, List, Optional, Sequence


class User(Object):
    def __init__(self, id: str = "", meta: Dict[str, Any] = {}) -> None:
        self.id = id
        Object.__init__(self, "user", id, meta)

    @classmethod
    def list(cls, list_params: Dict[str, Any] = {}, opts: Dict[str, Any] = {}):
        list_params['objectType'] = 'user'
        list_result = Object.list(list_params, opts=opts)
        users = map(lambda warrant_obj: User(warrant_obj.object_id, warrant_obj.meta), list_result.results)
        if list_result.prev_cursor != "" and list_result.next_cursor != "":
            return ListResult[User](list(users), list_result.prev_cursor, list_result.next_cursor)
        elif list_result.prev_cursor != "":
            return ListResult[User](list(users), list_result.prev_cursor)
        elif list_result.next_cursor != "":
            return ListResult[User](list(users), next_cursor=list_result.next_cursor)
        else:
            return ListResult[User](list(users))

    @classmethod
    def list_for_tenant(cls, tenant_id: str, list_params: Dict[str, Any] = {}, opts: Dict[str, Any] = {}) -> ListResult["User"]:
        query_result = Warrant.query("select * of type user for tenant:"+tenant_id, list_params, opts=opts)
        users = map(lambda warrant_obj: User(warrant_obj.object_id, warrant_obj.meta), query_result.results)
        if query_result.prev_cursor != "" and query_result.next_cursor != "":
            return ListResult[User](list(users), query_result.prev_cursor, query_result.next_cursor)
        elif query_result.prev_cursor != "":
            return ListResult[User](list(users), query_result.prev_cursor)
        elif query_result.next_cursor != "":
            return ListResult[User](list(users), next_cursor=query_result.next_cursor)
        else:
            return ListResult[User](list(users))

    @classmethod
    def get(cls, id: str, opts: Dict[str, Any] = {}) -> "User":
        warrant_obj = Object.get("user", id, opts=opts)
        return User.from_warrant_obj(warrant_obj)

    @classmethod
    def create(cls, id: str = "", meta: Dict[str, Any] = {}, opts: Dict[str, Any] = {}) -> "User":
        warrant_obj = Object.create("user", id, meta, opts=opts)
        return User.from_warrant_obj(warrant_obj)

    @classmethod
    def batch_create(cls, users: List[Dict[str, Any]], opts: Dict[str, Any] = {}) -> List["User"]:
        objects = map(lambda user: {"objectType": "user", "objectId": user['userId'], "meta": user['meta']} if "meta" in user.keys() else {"objectType": "user", "objectId": user['userId']}, users)
        created_objects = Object.batch_create(list(objects), opts)
        created_users = list(map(lambda warrant_obj: User(warrant_obj.object_id, warrant_obj.meta), created_objects))
        return created_users

    @classmethod
    def delete(cls, id: str, opts: Dict[str, Any] = {}) -> Optional[str]:
        return Object.delete("user", id, opts=opts)

    @classmethod
    def batch_delete(cls, users: List[Dict[str, Any]], opts: Dict[str, Any] = {}) -> Optional[str]:
        objects = map(lambda user: {"objectType": "user", "objectId": user['userId']}, users)
        return Object.batch_delete(list(objects), opts)

    """
    Tenants
    """
    @classmethod
    def assign_to_tenant(cls, tenant_id: str, user_id: str, relation: str, opts: Dict[str, Any] = {}):
        user_subject = Subject(constants.USER_OBJECT_TYPE, user_id)
        return Warrant.create(constants.TENANT_OBJECT_TYPE, tenant_id, relation, user_subject, opts=opts)

    @classmethod
    def remove_from_tenant(cls, tenant_id: str, user_id: str, relation: str, opts: Dict[str, Any] = {}):
        user_subject = Subject(constants.USER_OBJECT_TYPE, user_id)
        return Warrant.delete(constants.TENANT_OBJECT_TYPE, tenant_id, relation, user_subject, opts=opts)

    """
    Roles
    """
    def list_roles(self, list_params: Dict[str, Any] = {}, opts: Dict[str, Any] = {}):
        return Role.list_for_user(self.id, list_params, opts=opts)

    def assign_role(self, role_id: str, relation: str, opts: Dict[str, Any] = {}):
        Role.assign_to_user(self.id, role_id, relation, opts=opts)

    def remove_role(self, role_id: str, relation: str, opts: Dict[str, Any] = {}):
        Role.remove_from_user(self.id, role_id, relation, opts=opts)

    """
    Permissions
    """
    def list_permissions(self, list_params: Dict[str, Any] = {}, opts: Dict[str, Any] = {}):
        return Permission.list_for_user(self.id, list_params, opts=opts)

    def assign_permission(self, permission_id: str, relation: str, opts: Dict[str, Any] = {}):
        Permission.assign_to_user(self.id, permission_id, relation, opts=opts)

    def remove_permission(self, permission_id: str, relation: str, opts: Dict[str, Any] = {}):
        Permission.remove_from_user(self.id, permission_id, relation, opts=opts)

    def has_permission(self, permission_id: str, opts: Dict[str, Any] = {}):
        return Authz.check("permission", permission_id, "member", Subject("user", self.id), opts=opts)

    """
    Pricing tiers
    """
    def list_pricing_tiers(self, list_params: Dict[str, Any] = {}, opts: Dict[str, Any] = {}):
        return PricingTier.list_for_user(self.id, list_params, opts=opts)

    def assign_pricing_tier(self, pricing_tier_id: str, relation: str, opts: Dict[str, Any] = {}):
        PricingTier.assign_to_user(self.id, pricing_tier_id, relation, opts=opts)

    def remove_pricing_tier(self, pricing_tier_id: str, relation: str, opts: Dict[str, Any] = {}):
        PricingTier.remove_from_user(self.id, pricing_tier_id, relation, opts=opts)

    """
    Features
    """
    def list_features(self, list_params={}, opts: Dict[str, Any] = {}):
        return Feature.list_for_user(self.id, list_params, opts=opts)

    def assign_feature(self, feature_id: str, relation: str, opts: Dict[str, Any] = {}):
        Feature.assign_to_user(self.id, feature_id, relation, opts=opts)

    def remove_feature(self, feature_id: str, relation: str, opts: Dict[str, Any] = {}):
        Feature.remove_from_user(self.id, feature_id, relation, opts=opts)

    def has_feature(self, feature_id: str, opts: Dict[str, Any] = {}):
        return Authz.check("feature", feature_id, "member", Subject("user", self.id), opts=opts)

    """
    JSON serialization/deserialization
    """
    @staticmethod
    def from_warrant_obj(obj):
        return User(obj.object_id, obj.meta)

    @staticmethod
    def from_json(obj):
        if "objectType" in obj and "objectId" in obj:
            if "meta" in obj:
                return User(obj["objectId"], obj["meta"])
            else:
                return User(obj["objectId"])
        else:
            return obj
