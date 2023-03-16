from warrant import APIResource, Permission, Subject, Warrant, constants


class Role(APIResource):

    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

    @classmethod
    def list(cls, list_params={}):
        return cls._get("/v1/roles", params=list_params, object_hook=Role.from_json)

    @classmethod
    def get(cls, id):
        return cls._get("/v1/roles/"+id, params={}, object_hook=Role.from_json)

    @classmethod
    def create(cls, id, name="", description=""):
        payload = {
            "roleId": id
        }
        if name != "":
            payload["name"] = name
        if description != "":
            payload["description"] = description
        return cls._post(uri="/v1/roles", json=payload, object_hook=Role.from_json)

    def update(self, name, description):
        payload = {
            "name": name,
            "description": description
        }
        return self._put(uri="/v1/roles/"+self.id, json=payload, object_hook=Role.from_json)

    @classmethod
    def delete(cls, id):
        cls._delete(uri="/v1/roles/"+id, params={})

    """
    Users
    """
    @classmethod
    def list_for_user(cls, user_id, list_params={}):
        return cls._get(uri="/v1/users/"+user_id+"/roles", params=list_params, object_hook=Role.from_json)

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
    def from_json(obj):
        return Role(obj["roleId"], obj["name"], obj["description"])
