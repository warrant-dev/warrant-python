from warrant import APIResource

class Feature(APIResource):

    def __init__(self, id):
        self.id = id

    @classmethod
    def list(cls, list_params={}):
        return cls._get(uri="/v1/features", params=list_params, object_hook=Feature.from_json)

    @classmethod
    def get(cls, id):
        return cls._get(uri="/v1/features/"+id, params={}, object_hook=Feature.from_json)

    @classmethod
    def create(cls, id):
        payload = {
            "featureId": id
        }
        return cls._post(uri="/v1/features", json=payload, object_hook=Feature.from_json)

    @classmethod
    def delete(cls, id):
        cls._delete(uri="/v1/features/"+id, params={})

    """
    Pricing tiers
    """
    @classmethod
    def list_for_pricing_tier(cls, pricing_tier_id, list_params={}):
        return cls._get(uri="/v1/pricing-tiers/"+pricing_tier_id+"/features", params=list_params, object_hook=Feature.from_json)

    @classmethod
    def assign_to_pricing_tier(cls, pricing_tier_id, feature_id):
        cls._post(uri="/v1/pricing-tiers/"+pricing_tier_id+"/features/"+feature_id, json={})

    @classmethod
    def remove_from_pricing_tier(cls, pricing_tier_id, feature_id):
        cls._delete(uri="/v1/pricing-tiers/"+pricing_tier_id+"/features/"+feature_id, params={})

    """
    Tenants
    """
    @classmethod
    def list_for_tenant(cls, tenant_id, list_params={}):
        return cls._get(uri="/v1/tenants/"+tenant_id+"/features", params=list_params, object_hook=Feature.from_json)

    @classmethod
    def assign_to_tenant(cls, tenant_id, feature_id):
        cls._post(uri="/v1/tenants/"+tenant_id+"/features/"+feature_id, json={})

    @classmethod
    def remove_from_tenant(cls, tenant_id, feature_id):
        cls._delete(uri="/v1/tenants/"+tenant_id+"/features/"+feature_id, params={})

    """
    Users
    """
    @classmethod
    def list_for_user(cls, user_id, list_params={}):
        return cls._get(uri="/v1/users/"+user_id+"/features", params=list_params, object_hook=Feature.from_json)

    @classmethod
    def assign_to_user(cls, user_id, feature_id):
        cls._post(uri="/v1/users/"+user_id+"/features/"+feature_id, json={})

    @classmethod
    def remove_from_user(cls, user_id, feature_id):
        cls._delete(uri="/v1/users/"+user_id+"/features/"+feature_id, params={})

    """
    JSON serialization/deserialization
    """
    @staticmethod
    def from_json(obj):
      return Feature(obj["featureId"])
