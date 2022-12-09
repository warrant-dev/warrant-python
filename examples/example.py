from warrant import *

def make_warrant_requests(api_key):
    client = WarrantClient(api_key)

    # Create users, tenants, roles, permissions
    user1 = client.create_user()
    print("Created user with generated id: " + user1)
    provided_user_id = "custom_user_100"
    user2 = client.create_user(provided_user_id)
    print("Created user with provided id: " + user2)
    tenant1 = client.create_tenant("custom_tenant_210")
    print("Created tenant with provided id: " + tenant1)
    admin_role = client.create_role("admin1")
    print("Created role: " + admin_role)
    permission1 = client.create_permission("create_report")
    print("Created permission: " + permission1)
    permission2 = client.create_permission("delete_report")
    print("Created permission: " + permission2)
    print("Assigned role " + client.assign_role_to_user(user1, admin_role) + " to user " + user1)
    print("Assigned permission " + client.assign_permission_to_user(user1, permission1) + " to user " + user1)
    print("Assigned permission " + client.assign_permission_to_role(admin_role, permission2) + " to role " + admin_role)
    print("Created authorization session token for user " + user1 + ": " + client.create_authorization_session(AuthorizationSession(user_id=user1)))
    print("Created authorization session token for user " + user2 + ": " + client.create_authorization_session(AuthorizationSession(user_id=user2)))
    print("Assigned permission " + client.assign_permission_to_user(user2, "view-self-service-dashboard") + " to user " + user2)
    print("Created self service session for user " + user2 + ": " + client.create_self_service_session(SelfServiceSession(user_id=user2, tenant_id=tenant1), "http://example.com"))

    # Create and test warrants
    user1_subject = Subject("user", user1)
    print("--- Testing Warrants ---")
    print(client.create_warrant(object_type="tenant", object_id=tenant1, relation="member", subject=user1_subject))
    subject_to_check = Subject("user", user1)
    warrants_to_check = [Warrant("tenant", tenant1, "member", subject_to_check)]
    is_authorized = client.is_authorized(WarrantCheck(warrants_to_check, "allOf"))
    print(f"Tenant check authorization result: {is_authorized}")
    role_warrants_to_check = [Warrant("role", admin_role, "member", subject_to_check)]
    role_check = client.is_authorized(WarrantCheck(role_warrants_to_check, "allOf"))
    print(f"Admin role check authorization result: {role_check}")
    permission_warrants_to_check = [Warrant("permission", permission1, "member", subject_to_check)]
    permission_check = client.is_authorized(WarrantCheck(permission_warrants_to_check, "allOf"))
    print(f"create_report permission check authorization result: {permission_check}")
    role_subject = Subject("role", admin_role)
    role_permission_warrants_to_check = [Warrant("permission", permission2, "parent", role_subject)]
    role_permission_check = client.is_authorized(WarrantCheck(role_permission_warrants_to_check, "allOf"))
    print(f"create_report role/permission check authorization result: {role_permission_check}")
    print(f"List all warrants: {client.list_warrants()}")

    # Query all warrants for user1
    query_subject = "user:" + user1
    print(f"List all wararnts for user1: {client.query_warrants(query_subject)}")

    # Delete users, tenants, roles, permissions
    client.remove_permission_from_role(admin_role, permission2)
    client.remove_permission_from_user(user1, permission1)
    client.remove_role_from_user(user1, admin_role)
    client.delete_user(user1)
    print("Deleted user " + user1)
    client.delete_user(user2)
    print("Deleted user " + user2)
    client.delete_tenant(tenant1)
    print("Deleted tenant " + tenant1)
    client.delete_role(admin_role)
    print("Deleted role " + admin_role)
    client.delete_permission(permission1)
    print("Deleted permission " + permission1)
    client.delete_permission(permission2)
    print("Deleted permission " + permission2)

if __name__ == '__main__':
    # Replace with your Warrant api key
    api_key = "API_KEY"
    make_warrant_requests(api_key)
