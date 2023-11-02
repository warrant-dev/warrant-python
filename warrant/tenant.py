from warrant import APIResource, PricingTier, Feature, User, Authz, Subject, WarrantObject


class Tenant(WarrantObject):
    def __init__(self, id="", meta=None):
        self.id = id
        WarrantObject.__init__(self, "tenant", id, meta)

    @classmethod
    def list(cls, list_params={}, opts={}):
        list_params['objectType'] = 'tenant'
        list_result = WarrantObject.list(list_params, opts=opts)
        tenants = map(lambda warrant_obj: Tenant(warrant_obj.object_id, warrant_obj.meta), list_result['results'])
        list_result['results'] = list(tenants)
        return list_result

    @classmethod
    def get(cls, id, opts={}):
        warrant_obj = WarrantObject.get("tenant", id, opts=opts)
        return Tenant.from_warrant_obj(warrant_obj)

    @classmethod
    def create(cls, id="", meta={}, opts={}):
        warrant_obj = WarrantObject.create("tenant", id, meta, opts=opts)
        return Tenant.from_warrant_obj(warrant_obj)

    @classmethod
    def delete(cls, id, opts={}):
        return WarrantObject.delete("tenant", id, opts=opts)

    @classmethod
    def list_for_user(cls, user_id, list_params={}, opts={}):
        return Warrant.query("select tenant where user:"+user_id+" is *", list_params, opts=opts)

    """
    Users
    """
    def list_users(self, list_params={}, opts={}):
        return User.list_for_tenant(self.id, list_params, opts=opts)

    def assign_user(self, user_id, opts={}):
        User.assign_to_tenant(self.id, user_id, opts=opts)

    def remove_user(self, user_id, opts={}):
        User.remove_from_tenant(self.id, user_id, opts=opts)

    """
    Pricing tiers
    """
    def list_pricing_tiers(self, list_params={}, opts={}):
        return PricingTier.list_for_tenant(self.id, list_params, opts=opts)

    def assign_pricing_tier(self, pricing_tier_id, opts={}):
        PricingTier.assign_to_tenant(self.id, pricing_tier_id, opts=opts)

    def remove_pricing_tier(self, pricing_tier_id, opts={}):
        PricingTier.remove_from_tenant(self.id, pricing_tier_id, opts=opts)

    """
    Features
    """
    def list_features(self, list_params={}, opts={}):
        return Feature.list_for_tenant(self.id, list_params, opts=opts)

    def assign_feature(self, feature_id, opts={}):
        Feature.assign_to_tenant(self.id, feature_id, opts=opts)

    def remove_feature(self, feature_id, opts={}):
        Feature.remove_from_tenant(self.id, feature_id, opts=opts)

    def has_feature(self, feature_id, opts={}):
        return Authz.check("feature", feature_id, "member", Subject("user", self.id), opts=opts)

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
