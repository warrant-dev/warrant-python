from warrant import APIResource, Feature


class PricingTier(APIResource):

    def __init__(self, id):
        self.id = id

    @classmethod
    def list(cls, list_params={}):
        return cls._get(uri="/v1/pricing-tiers", params=list_params, object_hook=PricingTier._from_json)

    @classmethod
    def get(cls, id):
        return cls._get(uri="/v1/pricing-tiers/"+id, params={}, object_hook=PricingTier._from_json)

    @classmethod
    def create(cls, id):
        payload = {
            "pricingTierId": id
        }
        return cls._post(uri="/v1/pricing-tiers", json=payload, object_hook=PricingTier._from_json)

    @classmethod
    def delete(cls, id):
        cls._delete(uri="/v1/pricing-tiers/"+id, params={})

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
        return cls._get(uri="/v1/tenants/"+tenant_id+"/pricing-tiers", params=list_params, object_hook=PricingTier._from_json)

    @classmethod
    def assign_to_tenant(cls, tenant_id, pricing_tier_id):
        cls._post(uri="/v1/tenants/"+tenant_id+"/pricing-tiers/"+pricing_tier_id)

    @classmethod
    def remove_from_tenant(cls, tenant_id, pricing_tier_id):
        cls._delete(uri="/v1/tenants/"+tenant_id+"/pricing-tiers/"+pricing_tier_id, params={})

    """
    Users
    """
    @classmethod
    def list_for_user(cls, user_id, list_params={}):
        return cls._get(uri="/v1/users/"+user_id+"/pricing-tiers", params=list_params, object_hook=PricingTier._from_json)

    @classmethod
    def assign_to_user(cls, user_id, pricing_tier_id):
        cls._post(uri="/v1/users/"+user_id+"/pricing-tiers/"+pricing_tier_id)

    @classmethod
    def remove_from_user(cls, user_id, pricing_tier_id):
        cls._delete(uri="/v1/users/"+user_id+"/pricing-tiers/"+pricing_tier_id, params={})

    """
    JSON serialization/deserialization
    """
    @staticmethod
    def _from_json(obj):
        return PricingTier(obj["pricingTierId"])
