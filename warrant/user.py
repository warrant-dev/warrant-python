from warrant import APIResource, PricingTier, Feature, Role, Permission, Authz, Subject, Warrant, constants


class User(APIResource):

    def __init__(self, id, email):
        self.id = id
        self.email = email

    @classmethod
    def list(cls, list_params={}):
        return cls._get(uri="/v1/users", params=list_params, object_hook=User.from_json)

    @classmethod
    def list_for_tenant(cls, tenant_id, list_params={}):
        return cls._get(uri="/v1/tenants/"+tenant_id+"/users", params=list_params, object_hook=User.from_json)

    @classmethod
    def get(cls, id):
        return cls._get(uri="/v1/users/"+id, params={}, object_hook=User.from_json)

    @classmethod
    def create(cls, id="", email=""):
        payload = {}
        if id != "":
            payload["userId"] = id
        if email != "":
            payload["email"] = email
        return cls._post(uri="/v1/users", json=payload, object_hook=User.from_json)

    def update(self, email):
        payload = {
            "email": email
        }
        return self._put(uri="/v1/users/"+self.id, json=payload, object_hook=User.from_json)

    @classmethod
    def delete(cls, id):
        return cls._delete(uri="/v1/users/"+id, params={})

    """
    Tenants
    """
    @classmethod
    def assign_to_tenant(cls, tenant_id, user_id):
        user_subject = Subject(constants.USER_OBJECT_TYPE, user_id)
        return Warrant.create(constants.TENANT_OBJECT_TYPE, tenant_id, "member", user_subject)

    @classmethod
    def remove_from_tenant(cls, tenant_id, user_id):
        user_subject = Subject(constants.USER_OBJECT_TYPE, user_id)
        return Warrant.delete(constants.TENANT_OBJECT_TYPE, tenant_id, "member", user_subject)

    """
    Roles
    """
    def list_roles(self, list_params={}):
        return Role.list_for_user(self.id, list_params)

    def assign_role(self, role_id):
        Role.assign_to_user(self.id, role_id)

    def remove_role(self, role_id):
        Role.remove_from_user(self.id, role_id)

    """
    Permissions
    """
    def list_permissions(self, list_params={}):
        return Permission.list_for_user(self.id, list_params)

    def assign_permission(self, permission_id):
        Permission.assign_to_user(self.id, permission_id)

    def remove_permission(self, permission_id):
        Permission.remove_from_user(self.id, permission_id)

    def has_permission(self, permission_id):
        return Authz.check("permission", permission_id, "member", Subject("user", self.id))

    """
    Pricing tiers
    """
    def list_pricing_tiers(self, list_params={}):
        return PricingTier.list_for_user(self.id, list_params)

    def assign_pricing_tier(self, pricing_tier_id):
        PricingTier.assign_to_user(self.id, pricing_tier_id)

    def remove_pricing_tier(self, pricing_tier_id):
        PricingTier.remove_from_user(self.id, pricing_tier_id)

    """
    Features
    """
    def list_features(self, list_params={}):
        return Feature.list_for_user(self.id, list_params)

    def assign_feature(self, feature_id):
        Feature.assign_to_user(self.id, feature_id)

    def remove_feature(self, feature_id):
        Feature.remove_from_user(self.id, feature_id)

    def has_feature(self, feature_id):
        return Authz.check("feature", feature_id, "member", Subject("user", self.id))

    """
    JSON serialization/deserialization
    """
    @staticmethod
    def from_json(obj):
        return User(obj["userId"], obj["email"])
