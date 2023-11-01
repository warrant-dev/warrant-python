from warrant import APIResource, Permission, Subject, Warrant, WarrantObject, constants

class Role(WarrantObject):
    def __init__(self, id="", meta=None):
        self.id = id
        WarrantObject.__init__(self, "role", id, meta)

    @classmethod
    def list(cls, list_params={}):
        list_params['objectType'] = 'role'
        list_result = WarrantObject.list(list_params)
        roles = map(lambda warrant_obj: Role(warrant_obj.object_id, warrant_obj.meta), list_result['results'])
        list_result['results'] = list(roles)
        return list_result

    @classmethod
    def get(cls, id):
        warrant_obj = WarrantObject.get("role", id)
        return Role.from_warrant_obj(warrant_obj)

    @classmethod
    def create(cls, id="", meta={}):
        warrant_obj = WarrantObject.create("role", id, meta)
        return Role.from_warrant_obj(warrant_obj)

    @classmethod
    def delete(cls, id):
        return WarrantObject.delete("role", id)

    """
    Users
    """
    @classmethod
    def list_for_user(cls, user_id, list_params={}):
        return Warrant.query("select role where user:"+user_id+" is *", list_params)

    @classmethod
    def assign_to_user(cls, user_id, role_id):
        user_subject = Subject(constants.USER_OBJECT_TYPE, user_id)
        return Warrant.create(constants.ROLE_OBJECT_TYPE, role_id, "member", user_subject)

    @classmethod
    def remove_from_user(cls, user_id, role_id):
        user_subject = Subject(constants.USER_OBJECT_TYPE, user_id)
        return Warrant.delete(constants.ROLE_OBJECT_TYPE, role_id, "member", user_subject)

    """
    Permissions
    """
    def list_permissions(self, list_params={}):
        return Permission.list_for_role(self.id, list_params)

    def assign_permission(self, permission_id):
        Permission.assign_to_role(self.id, permission_id)

    def remove_permission(self, permission_id):
        Permission.remove_from_role(self.id, permission_id)

    """
    JSON serialization/deserialization
    """
    @staticmethod
    def from_warrant_obj(obj):
        return Role(obj.object_id, obj.meta)

    @staticmethod
    def from_json(obj):
        if "objectType" in obj and "objectId" in obj:
            if "meta" in obj:
                return Role(obj["objectId"], obj["meta"])
            else:
                return Role(obj["objectId"])
        else:
            return obj
