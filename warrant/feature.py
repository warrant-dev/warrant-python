from warrant import APIResource, Subject, Warrant, constants


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
        return cls._get(uri="/v1/tenants/"+tenant_id+"/features", params=list_params, object_hook=Feature.from_json)

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
        return cls._get(uri="/v1/users/"+user_id+"/features", params=list_params, object_hook=Feature.from_json)

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
    def from_json(obj):
        return Feature(obj["featureId"])
