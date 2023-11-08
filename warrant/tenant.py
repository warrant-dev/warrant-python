from warrant import APIResource, PricingTier, Feature, User, Authz, Subject, Warrant, WarrantObject, ListResult
from typing import Any, Dict, List, Optional


class Tenant(WarrantObject):
    def __init__(self, id: str = "", meta: Dict[str, Any] = {}) -> None:
        self.id = id
        WarrantObject.__init__(self, "tenant", id, meta)

    @classmethod
    def list(cls, list_params: Dict[str, Any] = {}, opts: Dict[str, Any] = {}):
        list_params['objectType'] = 'tenant'
        list_result = WarrantObject.list(list_params, opts=opts)
        tenants = map(lambda warrant_obj: Tenant(warrant_obj.object_id, warrant_obj.meta), list_result.results)
        if list_result.prev_cursor != "" and list_result.next_cursor != "":
            return ListResult[Tenant](list(tenants), list_result.prev_cursor, list_result.next_cursor)
        elif list_result.prev_cursor != "":
            return ListResult[Tenant](list(tenants), list_result.prev_cursor)
        elif list_result.next_cursor != "":
            return ListResult[Tenant](list(tenants), next_cursor=list_result.next_cursor)
        else:
            return ListResult[Tenant](list(tenants))

    @classmethod
    def get(cls, id: str, opts: Dict[str, Any] = {}) -> "Tenant":
        warrant_obj = WarrantObject.get("tenant", id, opts=opts)
        return Tenant.from_warrant_obj(warrant_obj)

    @classmethod
    def create(cls, id: str = "", meta: Dict[str, Any] = {}, opts: Dict[str, Any] = {}) -> "Tenant":
        warrant_obj = WarrantObject.create("tenant", id, meta, opts=opts)
        return Tenant.from_warrant_obj(warrant_obj)

    @classmethod
    def batch_create(cls, tenants: List[Dict[str, Any]], opts: Dict[str, Any] = {}) -> List["Tenant"]:
        objects = map(
            lambda tenant: {"objectType": "tenant", "objectId": tenant['tenantId'], "meta": tenant['meta']} if "meta" in tenant.keys() else {"objectType": "tenant", "objectId": tenant['tenantId']},
            tenants
        )
        created_objects = WarrantObject.batch_create(list(objects), opts)
        created_tenants = map(lambda warrant_obj: Tenant(warrant_obj.object_id, warrant_obj.meta), created_objects)
        return list(created_tenants)

    @classmethod
    def delete(cls, id: str, opts: Dict[str, Any] = {}) -> Optional[str]:
        return WarrantObject.delete("tenant", id, opts=opts)

    @classmethod
    def batch_delete(cls, tenants: List[Dict[str, Any]], opts: Dict[str, Any] = {}) -> Optional[str]:
        objects = map(lambda tenant: {"objectType": "tenant", "objectId": tenant['tenantId']}, tenants)
        return WarrantObject.batch_delete(list(objects), opts)

    @classmethod
    def list_for_user(cls, user_id: str, list_params: Dict[str, Any] = {}, opts: Dict[str, Any] = {}) -> ListResult["Tenant"]:
        query_result = Warrant.query("select tenant where user:"+user_id+" is *", list_params, opts=opts)
        tenants = map(lambda warrant_obj: Tenant(warrant_obj.object_id, warrant_obj.meta), query_result.results)
        if query_result.prev_cursor != "" and query_result.next_cursor != "":
            return ListResult[Tenant](list(tenants), query_result.prev_cursor, query_result.next_cursor)
        elif query_result.prev_cursor != "":
            return ListResult[Tenant](list(tenants), query_result.prev_cursor)
        elif query_result.next_cursor != "":
            return ListResult[Tenant](list(tenants), next_cursor=query_result.next_cursor)
        else:
            return ListResult[Tenant](list(tenants))

    """
    Users
    """
    def list_users(self, list_params: Dict[str, Any] = {}, opts: Dict[str, Any] = {}) -> ListResult["User"]:
        return User.list_for_tenant(self.id, list_params, opts=opts)

    def assign_user(self, user_id: str, relation: str, opts: Dict[str, Any] = {}):
        User.assign_to_tenant(self.id, user_id, relation, opts=opts)

    def remove_user(self, user_id: str, relation: str, opts: Dict[str, Any] = {}):
        User.remove_from_tenant(self.id, user_id, relation, opts=opts)

    """
    Pricing tiers
    """
    def list_pricing_tiers(self, list_params: Dict[str, Any] = {}, opts: Dict[str, Any] = {}):
        return PricingTier.list_for_tenant(self.id, list_params, opts=opts)

    def assign_pricing_tier(self, pricing_tier_id: str, relation: str, opts: Dict[str, Any] = {}):
        PricingTier.assign_to_tenant(self.id, pricing_tier_id, relation, opts=opts)

    def remove_pricing_tier(self, pricing_tier_id: str, relation: str, opts: Dict[str, Any] = {}):
        PricingTier.remove_from_tenant(self.id, pricing_tier_id, relation, opts=opts)

    """
    Features
    """
    def list_features(self, list_params: Dict[str, Any] = {}, opts: Dict[str, Any] = {}):
        return Feature.list_for_tenant(self.id, list_params, opts=opts)

    def assign_feature(self, feature_id: str, relation: str, opts: Dict[str, Any] = {}):
        Feature.assign_to_tenant(self.id, feature_id, relation, opts=opts)

    def remove_feature(self, feature_id: str, relation: str, opts: Dict[str, Any] = {}):
        Feature.remove_from_tenant(self.id, feature_id, relation, opts=opts)

    def has_feature(self, feature_id: str, opts: Dict[str, Any] = {}):
        return Authz.check("feature", feature_id, "member", Subject("tenant", self.id), opts=opts)

    """
    JSON serialization/deserialization
    """
    @staticmethod
    def from_warrant_obj(obj):
        return Tenant(obj.object_id, obj.meta)

    @staticmethod
    def from_json(obj):
        if "objectType" in obj and "objectId" in obj:
            if "meta" in obj:
                return Tenant(obj["objectId"], obj["meta"])
            else:
                return Tenant(obj["objectId"])
        else:
            return obj
