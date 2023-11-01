from warrant import APIResource, Feature, Subject, Warrant, WarrantObject, constants


class PricingTier(WarrantObject):
    def __init__(self, id="", meta=None):
        self.id = id
        WarrantObject.__init__(self, "pricing-tier", id, meta)

    @classmethod
    def list(cls, list_params={}):
        list_params['objectType'] = 'pricing-tier'
        list_result = WarrantObject.list(list_params)
        pricing_tiers = map(lambda warrant_obj: PricingTier(warrant_obj.object_id, warrant_obj.meta), list_result['results'])
        list_result['results'] = list(pricing_tiers)
        return list_result

    @classmethod
    def get(cls, id):
        warrant_obj = WarrantObject.get("pricing-tier", id)
        return PricingTier.from_warrant_obj(warrant_obj)

    @classmethod
    def create(cls, id, meta={}):
        warrant_obj = WarrantObject.create("pricing-tier", id, meta)
        return PricingTier.from_warrant_obj(warrant_obj)

    @classmethod
    def delete(cls, id):
        return WarrantObject.delete("pricing-tier", id)


    """
    Features
    """
    def list_features(self, list_params={}):
        return Feature.list_for_pricing_tier(pricing_tier_id=self.id, list_params=list_params)

    def assign_feature(self, feature_id):
        Feature.assign_to_pricing_tier(pricing_tier_id=self.id, feature_id=feature_id)

    def remove_feature(self, feature_id):
        Feature.remove_from_pricing_tier(pricing_tier_id=self.id, feature_id=feature_id)

    """
    Tenants
    """
    @classmethod
    def list_for_tenant(cls, tenant_id, list_params={}):
        return Warrant.query("select pricing-tier where tenant:"+tenant_id+" is *", list_params)

    @classmethod
    def assign_to_tenant(cls, tenant_id, pricing_tier_id):
        tenant_subject = Subject(constants.TENANT_OBJECT_TYPE, tenant_id)
        return Warrant.create(constants.PRICING_TIER_OBJECT_TYPE, pricing_tier_id, "member", tenant_subject)

    @classmethod
    def remove_from_tenant(cls, tenant_id, pricing_tier_id):
        tenant_subject = Subject(constants.TENANT_OBJECT_TYPE, tenant_id)
        return Warrant.delete(constants.PRICING_TIER_OBJECT_TYPE, pricing_tier_id, "member", tenant_subject)

    """
    Users
    """
    @classmethod
    def list_for_user(cls, user_id, list_params={}):
        return Warrant.query("select pricing-tier where user:"+user_id+" is *", list_params)

    @classmethod
    def assign_to_user(cls, user_id, pricing_tier_id):
        user_subject = Subject(constants.USER_OBJECT_TYPE, user_id)
        return Warrant.create(constants.PRICING_TIER_OBJECT_TYPE, pricing_tier_id, "member", user_subject)

    @classmethod
    def remove_from_user(cls, user_id, pricing_tier_id):
        user_subject = Subject(constants.USER_OBJECT_TYPE, user_id)
        return Warrant.delete(constants.PRICING_TIER_OBJECT_TYPE, pricing_tier_id, "member", user_subject)

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
