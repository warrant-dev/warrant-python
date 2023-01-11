from warrant import APIResource, PricingTier, Feature, User, Authz, Subject


class Tenant(APIResource):

    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def list(cls, list_params={}):
        return cls._get(uri="/v1/tenants", params=list_params, object_hook=Tenant.from_json)

    @classmethod
    def list_for_user(cls, user_id, list_params={}):
        return cls._get("/v1/users/"+user_id+"/tenants", params=list_params, object_hook=Tenant.from_json)

    @classmethod
    def get(cls, id):
        return cls._get(uri="/v1/tenants/"+id, params={}, object_hook=Tenant.from_json)

    @classmethod
    def create(cls, id="", name=""):
        payload = {}
        if id != "":
            payload["tenantId"] = id
        if name != "":
            payload["name"] = name
        return cls._post(uri="/v1/tenants", json=payload, object_hook=Tenant.from_json)

    def update(self, name):
        payload = {
            "name": name
        }
        return self._put(uri="/v1/tenants/"+self.id, json=payload, object_hook=Tenant.from_json)

    @classmethod
    def delete(cls, id):
        cls._delete(uri="/v1/tenants/"+id, params={})

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
    def from_json(obj):
        return Tenant(obj["tenantId"], obj["name"])
