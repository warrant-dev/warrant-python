from warrant import Subject, Warrant, Object, constants, ListResult
from typing import Any, Dict, Optional


class Feature(Object):
    def __init__(self, id: str = "", meta: Dict[str, Any] = {}) -> None:
        self.id = id
        Object.__init__(self, "feature", id, meta)

    @classmethod
    def list(cls, list_params: Dict[str, Any] = {}, opts: Dict[str, Any] = {}):
        list_params['objectType'] = 'feature'
        list_result = Object.list(list_params, opts=opts)
        features = map(lambda warrant_obj: Feature(warrant_obj.object_id, warrant_obj.meta), list_result.results)
        if list_result.prev_cursor != "" and list_result.next_cursor != "":
            return ListResult[Feature](list(features), list_result.prev_cursor, list_result.next_cursor)
        elif list_result.prev_cursor != "":
            return ListResult[Feature](list(features), list_result.prev_cursor)
        elif list_result.next_cursor != "":
            return ListResult[Feature](list(features), next_cursor=list_result.next_cursor)
        else:
            return ListResult[Feature](list(features))

    @classmethod
    def get(cls, id: str, opts: Dict[str, Any] = {}) -> "Feature":
        warrant_obj = Object.get("feature", id, opts=opts)
        return Feature.from_warrant_obj(warrant_obj)

    @classmethod
    def create(cls, id: str, meta: Dict[str, Any] = {}, opts: Dict[str, Any] = {}) -> "Feature":
        warrant_obj = Object.create("feature", id, meta, opts=opts)
        return Feature.from_warrant_obj(warrant_obj)

    @classmethod
    def delete(cls, id: str, opts: Dict[str, Any] = {}) -> Optional[str]:
        return Object.delete("feature", id, opts=opts)

    """
    Pricing tiers
    """
    @classmethod
    def list_for_pricing_tier(cls, pricing_tier_id: str, list_params: Dict[str, Any] = {}, opts: Dict[str, Any] = {}) -> ListResult["Feature"]:
        query_result = Warrant.query("select feature where pricing-tier:"+pricing_tier_id+" is *", list_params, opts=opts)
        features = map(lambda warrant_obj: Feature(warrant_obj.object_id, warrant_obj.meta), query_result.results)
        if query_result.prev_cursor != "" and query_result.next_cursor != "":
            return ListResult[Feature](list(features), query_result.prev_cursor, query_result.next_cursor)
        elif query_result.prev_cursor != "":
            return ListResult[Feature](list(features), query_result.prev_cursor)
        elif query_result.next_cursor != "":
            return ListResult[Feature](list(features), next_cursor=query_result.next_cursor)
        else:
            return ListResult[Feature](list(features))

    @classmethod
    def assign_to_pricing_tier(cls, pricing_tier_id: str, feature_id: str, relation: str = "member", opts: Dict[str, Any] = {}):
        pricing_tier_subject = Subject(constants.PRICING_TIER_OBJECT_TYPE, pricing_tier_id)
        return Warrant.create(constants.FEATURE_OBJECT_TYPE, feature_id, relation, pricing_tier_subject, opts=opts)

    @classmethod
    def remove_from_pricing_tier(cls, pricing_tier_id: str, feature_id: str, relation: str = "member", opts: Dict[str, Any] = {}):
        pricing_tier_subject = Subject(constants.PRICING_TIER_OBJECT_TYPE, pricing_tier_id)
        return Warrant.delete(constants.FEATURE_OBJECT_TYPE, feature_id, relation, pricing_tier_subject, opts=opts)

    """
    Tenants
    """
    @classmethod
    def list_for_tenant(cls, tenant_id: str, list_params: Dict[str, Any] = {}, opts: Dict[str, Any] = {}) -> ListResult["Feature"]:
        query_result = Warrant.query("select feature where tenant:"+tenant_id+" is *", list_params, opts=opts)
        features = map(lambda warrant_obj: Feature(warrant_obj.object_id, warrant_obj.meta), query_result.results)
        if query_result.prev_cursor != "" and query_result.next_cursor != "":
            return ListResult[Feature](list(features), query_result.prev_cursor, query_result.next_cursor)
        elif query_result.prev_cursor != "":
            return ListResult[Feature](list(features), query_result.prev_cursor)
        elif query_result.next_cursor != "":
            return ListResult[Feature](list(features), next_cursor=query_result.next_cursor)
        else:
            return ListResult[Feature](list(features))

    @classmethod
    def assign_to_tenant(cls, tenant_id: str, feature_id: str, relation: str = "member", opts: Dict[str, Any] = {}):
        tenant_subject = Subject(constants.TENANT_OBJECT_TYPE, tenant_id)
        return Warrant.create(constants.FEATURE_OBJECT_TYPE, feature_id, relation, tenant_subject, opts=opts)

    @classmethod
    def remove_from_tenant(cls, tenant_id: str, feature_id: str, relation: str = "member", opts: Dict[str, Any] = {}):
        tenant_subject = Subject(constants.TENANT_OBJECT_TYPE, tenant_id)
        return Warrant.delete(constants.FEATURE_OBJECT_TYPE, feature_id, relation, tenant_subject, opts=opts)

    """
    Users
    """
    @classmethod
    def list_for_user(cls, user_id: str, list_params: Dict[str, Any] = {}, opts: Dict[str, Any] = {}) -> ListResult["Feature"]:
        query_result = Warrant.query("select feature where user:"+user_id+" is *", list_params, opts=opts)
        features = map(lambda warrant_obj: Feature(warrant_obj.object_id, warrant_obj.meta), query_result.results)
        if query_result.prev_cursor != "" and query_result.next_cursor != "":
            return ListResult[Feature](list(features), query_result.prev_cursor, query_result.next_cursor)
        elif query_result.prev_cursor != "":
            return ListResult[Feature](list(features), query_result.prev_cursor)
        elif query_result.next_cursor != "":
            return ListResult[Feature](list(features), next_cursor=query_result.next_cursor)
        else:
            return ListResult[Feature](list(features))

    @classmethod
    def assign_to_user(cls, user_id: str, feature_id: str, relation: str = "member", opts: Dict[str, Any] = {}):
        user_subject = Subject(constants.USER_OBJECT_TYPE, user_id)
        return Warrant.create(constants.FEATURE_OBJECT_TYPE, feature_id, relation, user_subject, opts=opts)

    @classmethod
    def remove_from_user(cls, user_id: str, feature_id: str, relation: str = "member", opts: Dict[str, Any] = {}):
        user_subject = Subject(constants.USER_OBJECT_TYPE, user_id)
        return Warrant.delete(constants.FEATURE_OBJECT_TYPE, feature_id, relation, user_subject, opts=opts)

    """
    JSON serialization/deserialization
    """
    @staticmethod
    def from_warrant_obj(obj):
        return Feature(obj.object_id, obj.meta)

    @staticmethod
    def from_json(obj):
        if "objectType" in obj and "objectId" in obj:
            if "meta" in obj:
                return Feature(obj["objectId"], obj["meta"])
            else:
                return Feature(obj["objectId"])
        else:
            return obj
