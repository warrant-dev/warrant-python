from warrant import APIResource, Subject, Warrant, WarrantObject, constants


class Feature(WarrantObject):
    def __init__(self, id="", meta=None):
        self.id = id
        WarrantObject.__init__(self, "feature", id, meta)

    @classmethod
    def list(cls, list_params={}):
        list_params['objectType'] = 'feature'
        list_result = WarrantObject.list(list_params)
        features = map(lambda warrant_obj: Feature(warrant_obj.object_id, warrant_obj.meta), list_result['results'])
        list_result['results'] = list(features)
        return list_result

    @classmethod
    def get(cls, id):
        warrant_obj = WarrantObject.get("feature", id)
        return Feature.from_warrant_obj(warrant_obj)

    @classmethod
    def create(cls, id, meta={}):
        warrant_obj = WarrantObject.create("feature", id, meta)
        return Feature.from_warrant_obj(warrant_obj)

    @classmethod
    def delete(cls, id):
        return WarrantObject.delete("feature", id)

    """
    Pricing tiers
    """
    @classmethod
    def list_for_pricing_tier(cls, pricing_tier_id, list_params={}):
        return Warrant.query("select feature where pricing-tier:"+pricing_tier_id+" is *", list_params)

    @classmethod
    def assign_to_pricing_tier(cls, pricing_tier_id, feature_id):
        pricing_tier_subject = Subject(constants.PRICING_TIER_OBJECT_TYPE, pricing_tier_id)
        return Warrant.create(constants.FEATURE_OBJECT_TYPE, feature_id, "member", pricing_tier_subject)

    @classmethod
    def remove_from_pricing_tier(cls, pricing_tier_id, feature_id):
        pricing_tier_subject = Subject(constants.PRICING_TIER_OBJECT_TYPE, pricing_tier_id)
        return Warrant.delete(constants.FEATURE_OBJECT_TYPE, feature_id, "member", pricing_tier_subject)

    """
    Tenants
    """
    @classmethod
    def list_for_tenant(cls, tenant_id, list_params={}):
        return Warrant.query("select feature where tenant:"+tenant_id+" is *", list_params)

    @classmethod
    def assign_to_tenant(cls, tenant_id, feature_id):
        tenant_subject = Subject(constants.TENANT_OBJECT_TYPE, tenant_id)
        return Warrant.create(constants.FEATURE_OBJECT_TYPE, feature_id, "member", tenant_subject)

    @classmethod
    def remove_from_tenant(cls, tenant_id, feature_id):
        tenant_subject = Subject(constants.TENANT_OBJECT_TYPE, tenant_id)
        return Warrant.delete(constants.FEATURE_OBJECT_TYPE, feature_id, "member", tenant_subject)

    """
    Users
    """
    @classmethod
    def list_for_user(cls, user_id, list_params={}):
        return Warrant.query("select feature where user:"+user_id+" is *", list_params)

    @classmethod
    def assign_to_user(cls, user_id, feature_id):
        user_subject = Subject(constants.USER_OBJECT_TYPE, user_id)
        return Warrant.create(constants.FEATURE_OBJECT_TYPE, feature_id, "member", user_subject)

    @classmethod
    def remove_from_user(cls, user_id, feature_id):
        user_subject = Subject(constants.USER_OBJECT_TYPE, user_id)
        return Warrant.delete(constants.FEATURE_OBJECT_TYPE, feature_id, "member", user_subject)

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
