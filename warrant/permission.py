from warrant import APIResource, Subject, Warrant, constants


class Permission(APIResource):

    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

    @classmethod
    def list(cls, list_params={}):
        return cls._get(uri="/v1/permissions", params=list_params, object_hook=Permission.from_json)

    @classmethod
    def get(cls, id):
        return cls._get(uri="/v1/permissions/"+id, params={}, object_hook=Permission.from_json)

    @classmethod
    def create(cls, id, name="", description=""):
        payload = {
            "permissionId": id
        }
        if name != "":
            payload["name"] = name
        if description != "":
            payload["description"] = description
        return cls._post(uri="/v1/permissions", json=payload, object_hook=Permission.from_json)

    def update(self, name, description):
        payload = {
            "name": name,
            "description": description
        }
        return self._put(uri="/v1/permissions/"+self.id, json=payload, object_hook=Permission.from_json)

    @classmethod
    def delete(cls, id):
        cls._delete(uri="/v1/permissions/"+id, params={})

    """
    Users
    """
    @classmethod
    def list_for_user(cls, user_id, list_params={}):
        return cls._get(uri="/v1/users/"+user_id+"/permissions", params=list_params, object_hook=Permission.from_json)

    @classmethod
    def assign_to_user(cls, user_id, permission_id):
        user_subject = Subject(constants.USER_OBJECT_TYPE, user_id)
        return Warrant.create(constants.PERMISSION_OBJECT_TYPE, permission_id, "member", user_subject)

    @classmethod
    def remove_from_user(cls, user_id, permission_id):
        user_subject = Subject(constants.USER_OBJECT_TYPE, user_id)
        return Warrant.delete(constants.PERMISSION_OBJECT_TYPE, permission_id, "member", user_subject)

    """
    Roles
    """
    @classmethod
    def list_for_role(cls, role_id, list_params={}):
        return cls._get(uri="/v1/roles/"+role_id+"/permissions", params=list_params, object_hook=Permission.from_json)

    @classmethod
    def assign_to_role(cls, role_id, permission_id):
        role_subject = Subject(constants.ROLE_OBJECT_TYPE, role_id)
        return Warrant.create(constants.PERMISSION_OBJECT_TYPE, permission_id, "member", role_subject)

    @classmethod
    def remove_from_role(cls, role_id, permission_id):
        role_subject = Subject(constants.ROLE_OBJECT_TYPE, role_id)
        return Warrant.delete(constants.PERMISSION_OBJECT_TYPE, permission_id, "member", role_subject)

    """
    JSON serialization/deserialization
    """
    @staticmethod
    def from_json(obj):
        return Permission(obj["permissionId"], obj["name"], obj["description"])
