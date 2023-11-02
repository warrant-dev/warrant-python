from warrant import APIResource, PricingTier, Feature, Role, Permission, Authz, Subject, Warrant, WarrantObject, constants


class User(WarrantObject):
    def __init__(self, id="", meta=None):
        self.id = id
        WarrantObject.__init__(self, "user", id, meta)

    @classmethod
    def list(cls, list_params={}, opts={}):
        list_params['objectType'] = 'user'
        list_result = WarrantObject.list(list_params, opts=opts)
        users = map(lambda warrant_obj: User(warrant_obj.object_id, warrant_obj.meta), list_result['results'])
        list_result['results'] = list(users)
        return list_result

    @classmethod
    def list_for_tenant(cls, tenant_id, list_params={}, opts={}):
        return Warrant.query("select * of type user for tenant:"+tenant_id, list_params, opts=opts)

    @classmethod
    def get(cls, id, opts={}):
        warrant_obj = WarrantObject.get("user", id, opts=opts)
        return User.from_warrant_obj(warrant_obj)

    @classmethod
    def create(cls, id="", meta={}, opts={}):
        warrant_obj = WarrantObject.create("user", id, meta, opts=opts)
        return User.from_warrant_obj(warrant_obj)

    @classmethod
    def delete(cls, id, opts={}):
        return WarrantObject.delete("user", id, opts=opts)

    """
    Tenants
    """
    @classmethod
    def assign_to_tenant(cls, tenant_id, user_id, opts={}):
        user_subject = Subject(constants.USER_OBJECT_TYPE, user_id)
        return Warrant.create(constants.TENANT_OBJECT_TYPE, tenant_id, "member", user_subject, opts=opts)

    @classmethod
    def remove_from_tenant(cls, tenant_id, user_id, opts={}):
        user_subject = Subject(constants.USER_OBJECT_TYPE, user_id)
        return Warrant.delete(constants.TENANT_OBJECT_TYPE, tenant_id, "member", user_subject, opts=opts)

    """
    Roles
    """
    def list_roles(self, list_params={}, opts={}):
        return Role.list_for_user(self.id, list_params, opts=opts)

    def assign_role(self, role_id, opts={}):
        Role.assign_to_user(self.id, role_id, opts=opts)

    def remove_role(self, role_id, opts={}):
        Role.remove_from_user(self.id, role_id, opts=opts)

    """
    Permissions
    """
    def list_permissions(self, list_params={}, opts={}):
        return Permission.list_for_user(self.id, list_params, opts=opts)

    def assign_permission(self, permission_id, opts={}):
        Permission.assign_to_user(self.id, permission_id, opts=opts)

    def remove_permission(self, permission_id, opts={}):
        Permission.remove_from_user(self.id, permission_id, opts=opts)

    def has_permission(self, permission_id, opts={}):
        return Authz.check("permission", permission_id, "member", Subject("user", self.id), opts=opts)

    """
    Pricing tiers
    """
    def list_pricing_tiers(self, list_params={}, opts={}):
        return PricingTier.list_for_user(self.id, list_params, opts=opts)

    def assign_pricing_tier(self, pricing_tier_id, opts={}):
        PricingTier.assign_to_user(self.id, pricing_tier_id, opts=opts)

    def remove_pricing_tier(self, pricing_tier_id, opts={}):
        PricingTier.remove_from_user(self.id, pricing_tier_id, opts=opts)

    """
    Features
    """
    def list_features(self, list_params={}, opts={}):
        return Feature.list_for_user(self.id, list_params, opts=opts)

    def assign_feature(self, feature_id, opts={}):
        Feature.assign_to_user(self.id, feature_id, opts=opts)

    def remove_feature(self, feature_id, opts={}):
        Feature.remove_from_user(self.id, feature_id, opts=opts)

    def has_feature(self, feature_id, opts={}):
        return Authz.check("feature", feature_id, "member", Subject("user", self.id), opts=opts)

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
