from warrant import APIResource, PricingTier, Feature, User, Authz, Subject, WarrantObject


class Tenant(WarrantObject):
    def __init__(self, id="", meta=None):
        self.id = id
        WarrantObject.__init__(self, "tenant", id, meta)

    @classmethod
    def list(cls, list_params={}):
        list_params['objectType'] = 'tenant'
        list_result = WarrantObject.list(list_params)
        tenants = map(lambda warrant_obj: Tenant(warrant_obj.object_id, warrant_obj.meta), list_result['results'])
        list_result['results'] = list(tenants)
        return list_result

    @classmethod
    def get(cls, id):
        warrant_obj = WarrantObject.get("tenant", id)
        return Tenant.from_warrant_obj(warrant_obj)

    @classmethod
    def create(cls, id="", meta={}):
        warrant_obj = WarrantObject.create("tenant", id, meta)
        return Tenant.from_warrant_obj(warrant_obj)

    @classmethod
    def delete(cls, id):
        return WarrantObject.delete("tenant", id)

    @classmethod
    def list_for_user(cls, user_id, list_params={}):
        return Warrant.query("select tenant where user:"+user_id+" is *", list_params)

    """
    Users
    """
    def list_users(self, list_params={}):
        return User.list_for_tenant(self.id, list_params)

    def assign_user(self, user_id):
        User.assign_to_tenant(self.id, user_id)

    def remove_user(self, user_id):
        User.remove_from_tenant(self.id, user_id)

    """
    Pricing tiers
    """
    def list_pricing_tiers(self, list_params={}):
        return PricingTier.list_for_tenant(self.id, list_params)

    def assign_pricing_tier(self, pricing_tier_id):
        PricingTier.assign_to_tenant(self.id, pricing_tier_id)

    def remove_pricing_tier(self, pricing_tier_id):
        PricingTier.remove_from_tenant(self.id, pricing_tier_id)

    """
    Features
    """
    def list_features(self, list_params={}):
        return Feature.list_for_tenant(self.id, list_params)

    def assign_feature(self, feature_id):
        Feature.assign_to_tenant(self.id, feature_id)

    def remove_feature(self, feature_id):
        Feature.remove_from_tenant(self.id, feature_id)

    def has_feature(self, feature_id):
        return Authz.check("feature", feature_id, "member", Subject("user", self.id))

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
