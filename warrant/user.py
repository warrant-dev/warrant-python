from warrant import APIResource, PricingTier, Feature, Role, Permission, Authz, Subject, Warrant, WarrantObject, constants


class User(WarrantObject):
    def __init__(self, id="", meta=None):
        self.id = id
        WarrantObject.__init__(self, "user", id, meta)

    @classmethod
    def list(cls, list_params={}):
        list_params['objectType'] = 'user'
        list_result = WarrantObject.list(list_params)
        users = map(lambda warrant_obj: User(warrant_obj.object_id, warrant_obj.meta), list_result['results'])
        list_result['results'] = list(users)
        return list_result

    @classmethod
    def list_for_tenant(cls, tenant_id, list_params={}):
        return Warrant.query("select * of type user for tenant:"+tenant_id, list_params)

    @classmethod
    def get(cls, id):
        warrant_obj = WarrantObject.get("user", id)
        return User.from_warrant_obj(warrant_obj)

    @classmethod
    def create(cls, id="", meta={}):
        warrant_obj = WarrantObject.create("user", id, meta)
        return User.from_warrant_obj(warrant_obj)

    @classmethod
    def delete(cls, id):
        return WarrantObject.delete("user", id)

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
    def from_warrant_obj(obj):
        return User(obj.object_id, obj.meta)

    @staticmethod
    def from_json(obj):
        if "objectType" in obj and "objectId" in obj:
            if "meta" in obj:
                return User(obj["objectId"], obj["meta"])
            else:
                return User(obj["objectId"])
        else:
            return obj
