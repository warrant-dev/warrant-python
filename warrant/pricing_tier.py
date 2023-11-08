from warrant import APIResource, Feature, Subject, Warrant, Object, constants, ListResult
from typing import Any, Dict, List, Optional


class PricingTier(Object):
    def __init__(self, id: str = "", meta: Dict[str, Any] = {}) -> None:
        self.id = id
        Object.__init__(self, "pricing-tier", id, meta)

    @classmethod
    def list(cls, list_params: Dict[str, Any] = {}, opts: Dict[str, Any] = {}):
        list_params['objectType'] = 'pricing-tier'
        list_result = Object.list(list_params, opts=opts)
        pricing_tiers = map(lambda warrant_obj: PricingTier(warrant_obj.object_id, warrant_obj.meta), list_result.results)
        if list_result.prev_cursor != "" and list_result.next_cursor != "":
            return ListResult[PricingTier](list(pricing_tiers), list_result.prev_cursor, list_result.next_cursor)
        elif list_result.prev_cursor != "":
            return ListResult[PricingTier](list(pricing_tiers), list_result.prev_cursor)
        elif list_result.next_cursor != "":
            return ListResult[PricingTier](list(pricing_tiers), next_cursor=list_result.next_cursor)
        else:
            return ListResult[PricingTier](list(pricing_tiers))

    @classmethod
    def get(cls, id: str, opts: Dict[str, Any] = {}) -> "PricingTier":
        warrant_obj = Object.get("pricing-tier", id, opts=opts)
        return PricingTier.from_warrant_obj(warrant_obj)

    @classmethod
    def create(cls, id: str, meta: Dict[str, Any] = {}, opts: Dict[str, Any] = {}) -> "PricingTier":
        warrant_obj = Object.create("pricing-tier", id, meta, opts=opts)
        return PricingTier.from_warrant_obj(warrant_obj)

    @classmethod
    def delete(cls, id: str, opts: Dict[str, Any] = {}):
        return Object.delete("pricing-tier", id, opts=opts)

    """
    Features
    """
    def list_features(self, list_params: Dict[str, Any] = {}, opts: Dict[str, Any] = {}) -> ListResult[Feature]:
        return Feature.list_for_pricing_tier(pricing_tier_id=self.id, list_params=list_params, opts=opts)

    def assign_feature(self, feature_id: str, relation: str, opts: Dict[str, Any] = {}):
        Feature.assign_to_pricing_tier(pricing_tier_id=self.id, feature_id=feature_id, relation=relation, opts=opts)

    def remove_feature(self, feature_id: str, relation: str, opts: Dict[str, Any] = {}):
        Feature.remove_from_pricing_tier(pricing_tier_id=self.id, feature_id=feature_id, relation=relation, opts=opts)

    """
    Tenants
    """
    @classmethod
    def list_for_tenant(cls, tenant_id: str, list_params: Dict[str, Any] = {}, opts: Dict[str, Any] = {}) -> ListResult["PricingTier"]:
        query_result = Warrant.query("select pricing-tier where tenant:"+tenant_id+" is *", list_params, opts=opts)
        pricing_tiers = map(lambda warrant_obj: PricingTier(warrant_obj.object_id, warrant_obj.meta), query_result.results)
        if query_result.prev_cursor != "" and query_result.next_cursor != "":
            return ListResult[PricingTier](list(pricing_tiers), query_result.prev_cursor, query_result.next_cursor)
        elif query_result.prev_cursor != "":
            return ListResult[PricingTier](list(pricing_tiers), query_result.prev_cursor)
        elif query_result.next_cursor != "":
            return ListResult[PricingTier](list(pricing_tiers), next_cursor=query_result.next_cursor)
        else:
            return ListResult[PricingTier](list(pricing_tiers))

    @classmethod
    def assign_to_tenant(cls, tenant_id: str, pricing_tier_id: str, relation: str, opts: Dict[str, Any] = {}):
        tenant_subject = Subject(constants.TENANT_OBJECT_TYPE, tenant_id)
        return Warrant.create(constants.PRICING_TIER_OBJECT_TYPE, pricing_tier_id, relation, tenant_subject, opts=opts)

    @classmethod
    def remove_from_tenant(cls, tenant_id: str, pricing_tier_id: str, relation: str, opts: Dict[str, Any] = {}):
        tenant_subject = Subject(constants.TENANT_OBJECT_TYPE, tenant_id)
        return Warrant.delete(constants.PRICING_TIER_OBJECT_TYPE, pricing_tier_id, relation, tenant_subject, opts=opts)

    """
    Users
    """
    @classmethod
    def list_for_user(cls, user_id: str, list_params: Dict[str, Any] = {}, opts: Dict[str, Any] = {}) -> ListResult["PricingTier"]:
        query_result = Warrant.query("select pricing-tier where user:"+user_id+" is *", list_params, opts=opts)
        pricing_tiers = map(lambda warrant_obj: PricingTier(warrant_obj.object_id, warrant_obj.meta), query_result.results)
        if query_result.prev_cursor != "" and query_result.next_cursor != "":
            return ListResult[PricingTier](list(pricing_tiers), query_result.prev_cursor, query_result.next_cursor)
        elif query_result.prev_cursor != "":
            return ListResult[PricingTier](list(pricing_tiers), query_result.prev_cursor)
        elif query_result.next_cursor != "":
            return ListResult[PricingTier](list(pricing_tiers), next_cursor=query_result.next_cursor)
        else:
            return ListResult[PricingTier](list(pricing_tiers))

    @classmethod
    def assign_to_user(cls, user_id: str, pricing_tier_id: str, relation: str, opts: Dict[str, Any] = {}):
        user_subject = Subject(constants.USER_OBJECT_TYPE, user_id)
        return Warrant.create(constants.PRICING_TIER_OBJECT_TYPE, pricing_tier_id, relation, user_subject, opts=opts)

    @classmethod
    def remove_from_user(cls, user_id: str, pricing_tier_id: str, relation: str, opts: Dict[str, Any] = {}):
        user_subject = Subject(constants.USER_OBJECT_TYPE, user_id)
        return Warrant.delete(constants.PRICING_TIER_OBJECT_TYPE, pricing_tier_id, relation, user_subject, opts=opts)

    """
    JSON serialization/deserialization
    """
    @staticmethod
    def from_warrant_obj(obj):
        return PricingTier(obj.object_id, obj.meta)

    @staticmethod
    def from_json(obj):
        if "objectType" in obj and "objectId" in obj:
            if "meta" in obj:
                return PricingTier(obj["objectId"], obj["meta"])
            else:
                return PricingTier(obj["objectId"])
        else:
            return obj
