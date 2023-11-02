from warrant import APIResource, Subject, Warrant, WarrantObject, constants


class Permission(WarrantObject):
    def __init__(self, id="", meta=None):
        self.id = id
        WarrantObject.__init__(self, "permission", id, meta)

    @classmethod
    def list(cls, list_params={}, opts={}):
        list_params['objectType'] = 'permission'
        list_result = WarrantObject.list(list_params, opts=opts)
        permissions = map(lambda warrant_obj: Permission(warrant_obj.object_id, warrant_obj.meta), list_result['results'])
        list_result['results'] = list(permissions)
        return list_result

    @classmethod
    def get(cls, id, opts={}):
        warrant_obj = WarrantObject.get("permission", id, opts=opts)
        return Permission.from_warrant_obj(warrant_obj)

    @classmethod
    def create(cls, id, meta={}, opts={}):
        warrant_obj = WarrantObject.create("permission", id, meta, opts=opts)
        return Permission.from_warrant_obj(warrant_obj)

    @classmethod
    def delete(cls, id, opts={}):
        return WarrantObject.delete("permission", id, opts=opts)

    """
    Users
    """
    @classmethod
    def list_for_user(cls, user_id, list_params={}, opts={}):
        return Warrant.query("select permission where user:"+user_id+" is *", list_params, opts=opts)

    @classmethod
    def assign_to_user(cls, user_id, permission_id, opts={}):
        user_subject = Subject(constants.USER_OBJECT_TYPE, user_id)
        return Warrant.create(constants.PERMISSION_OBJECT_TYPE, permission_id, "member", user_subject, opts=opts)

    @classmethod
    def remove_from_user(cls, user_id, permission_id, opts={}):
        user_subject = Subject(constants.USER_OBJECT_TYPE, user_id)
        return Warrant.delete(constants.PERMISSION_OBJECT_TYPE, permission_id, "member", user_subject, opts=opts)

    """
    Roles
    """
    @classmethod
    def list_for_role(cls, role_id, list_params={}, opts={}):
        return Warrant.query("select permission where role:"+role_id+" is *", list_params, opts=opts)

    @classmethod
    def assign_to_role(cls, role_id, permission_id, opts={}):
        role_subject = Subject(constants.ROLE_OBJECT_TYPE, role_id)
        return Warrant.create(constants.PERMISSION_OBJECT_TYPE, permission_id, "member", role_subject, opts=opts)

    @classmethod
    def remove_from_role(cls, role_id, permission_id, opts={}):
        role_subject = Subject(constants.ROLE_OBJECT_TYPE, role_id)
        return Warrant.delete(constants.PERMISSION_OBJECT_TYPE, permission_id, "member", role_subject, opts=opts)

    """
    JSON serialization/deserialization
    """
    @staticmethod
    def from_warrant_obj(obj):
        return Permission(obj.object_id, obj.meta)

    @staticmethod
    def from_json(obj):
        if "objectType" in obj and "objectId" in obj:
            if "meta" in obj:
                return Permission(obj["objectId"], obj["meta"])
            else:
                return Permission(obj["objectId"])
        else:
            return obj
