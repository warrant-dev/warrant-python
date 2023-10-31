import warrant

"""
Common usage examples for:
- Users
- Tenants
- Roles, Permissions (RBAC)
- Pricing Tiers, Features
"""

# Replace with your own API key to run example
warrant.api_key = ""
warrant.api_endpoint = "https://api.warrant.dev"

"""
Objects
"""
# Create objects
print("---------- Objects ----------")
object1 = warrant.WarrantObject.create(object_type="document")
object2 = warrant.WarrantObject.create(object_type="folder", object_id="planning")
print(f"Created objects: [{object1.object_type}:{object1.object_id} {object2.object_type}:{object2.object_id}]")
object1 = warrant.WarrantObject.get(object1.object_type, object1.object_id)
print(f"Fetched object: {object1.object_type}:{object1.object_id}")
object2.update(meta={"description": "Folder for planning docs"})
print(f"Updated object: {object2.object_type}:{object2.object_id} [{object2.meta}]")

objects_list = warrant.WarrantObject.list({"limit": 2})
print(f"List objects: {objects_list}")

"""
Users & Tenants
"""
# Create some users
print("---------- Users & Tenants ----------")
user1 = warrant.User.create()
user2 = warrant.User.create(id="custom_user_id_1")
print(f"Created users: [{user1.id}, {user2.id}]")
user2.update("newemail@test.com")
print(f"User updated: {user2.id} - {user2.email}")

# Create tenants & assign the users to them (multitenancy)
tenant1 = warrant.Tenant.create(id="dunder_mifflin")
tenant2 = warrant.Tenant.create(id="big_box_paper")
print(f"Created tenants: [{tenant1.id}, {tenant2.id}]")
tenant1.update("Dunder Mifflin")
print(f"Updated tenant: {tenant1.id} - {tenant1.name}")
tenant1.assign_user(user1.id)
print(f"Assigned user [{user1.id}] to tenant [{tenant1.id}]")
user2_subject = warrant.Subject("user", user2.id)
warrant.Warrant.create("tenant", tenant1.id, "admin", user2_subject)
print(f"Assigned user [{user2.id}] as admin to tenant [{tenant2.id}]")
tenant1_users = ""
for u in tenant1.list_users():
    tenant1_users += u.id + " "
print(f"Verify users for [{tenant1.id}]: [{tenant1_users}]")
tenant2_users = ""
for u in tenant2.list_users():
    tenant2_users += u.id + " "
print(f"Verify users for [{tenant2.id}]: [{tenant2_users}]")
print("\n")


"""
Roles & Permissions (Role Based Access Control)
"""
# Create roles
print("---------- Role Based Access Control ----------")
admin_role = warrant.Role.create(id="admin1")
viewer_role = warrant.Role.create(id="viewer")
print(f"Created roles: [{admin_role.id}, {viewer_role.id}]")
admin_role.update("Admin", "Administrator role")
print(f"Updated admin role: {admin_role.id} - {admin_role.name} - {admin_role.description}")

# Create permissions
create_report_perm = warrant.Permission.create(id="create_report")
delete_report_perm = warrant.Permission.create(id="delete_report")
view_report_perm = warrant.Permission.create(id="view_report")
special_perm = warrant.Permission.create(id="special_perm")
print(f"Created permissions: [{create_report_perm.id}, {delete_report_perm.id}, {view_report_perm.id}, {special_perm.id}]")
create_report_perm.update("Create Report", "Permission for creating reports")
print(f"Updated create report permission: {create_report_perm.id} - {create_report_perm.name} - {create_report_perm.description}")

# Assign permissions to roles:
# 'create_report', 'delete_report', 'view_report' -> 'admin' role
# 'view_report' -> 'viewer' role
admin_role.assign_permission(create_report_perm.id)
admin_role.assign_permission(delete_report_perm.id)
admin_role.assign_permission(view_report_perm.id)
admin_role_perms = ""
for p in admin_role.list_permissions():
    admin_role_perms += p.id + " "
print(f"Assigned permissions to [{admin_role.id}] role: [{admin_role_perms}]")
viewer_role.assign_permission(view_report_perm.id)
viewer_role_perms = ""
for p in viewer_role.list_permissions():
    viewer_role_perms += p.id + " "
print(f"Assigned permissions to [{viewer_role.id}] role: [{viewer_role_perms}]")

# Assign roles & permissions to users:
# 'admin' role and 'special_perm' permission -> 'user1'
# 'viewer' role -> 'user2'
user1.assign_role(admin_role.id)
print(f"Assigned role [{admin_role.id}] to user [{user1.id}]")
user1.assign_permission(special_perm.id)
print(f"Assigned permission [{special_perm.id}] to user [{user1.id}]")
user2.assign_role(viewer_role.id)
print(f"Assigned role [{viewer_role.id}] to user [{user2.id}]")

# RBAC checks
print(f"Does user [{user1.id}] have the [{create_report_perm.id}] permission? (should be true) -> {user1.has_permission(create_report_perm.id)}")
print(f"Does user [{user1.id}] have the [{delete_report_perm.id}] permission? (should be true) -> {user1.has_permission(delete_report_perm.id)}")
print(f"Does user [{user1.id}] have the [{view_report_perm.id}] permission? (should be true) -> {user1.has_permission(view_report_perm.id)}")
print(f"Does user [{user1.id}] have the [{special_perm.id}] permission? (should be true) -> {user1.has_permission(special_perm.id)}")

print(f"Does user [{user2.id}] have the [{create_report_perm.id}] permission? (should be false) -> {user2.has_permission(create_report_perm.id)}")
print(f"Does user [{user2.id}] have the [{delete_report_perm.id}] permission? (should be false) -> {user2.has_permission(delete_report_perm.id)}")
print(f"Does user [{user2.id}] have the [{view_report_perm.id}] permission? (should be true) -> {user2.has_permission(view_report_perm.id)}")
print(f"Does user [{user2.id}] have the [{special_perm.id}] permission? (should be false) -> {user2.has_permission(special_perm.id)}")
print("\n")


"""
Pricing Tiers & Features
"""
# Create pricing tiers
print("---------- Pricing Tiers & Features ----------")
enterprise_tier = warrant.PricingTier.create("enterprise")
free_tier = warrant.PricingTier.create("free")
print(f"Created pricing tiers: [{enterprise_tier.id}, {free_tier.id}]")

# Create features
analytics_feature = warrant.Feature.create("analytics")
dashboard_feature = warrant.Feature.create("dashboard")
print(f"Created features: [{analytics_feature.id}, {dashboard_feature.id}]")

# Assign features to pricing tiers:
# 'analytics' feature -> 'enterprise' tier
# 'dashboard' feature -> 'free' tier
enterprise_tier.assign_feature(analytics_feature.id)
enterprise_tier_features = ""
for f in enterprise_tier.list_features():
    enterprise_tier_features += f.id + " "
print(f"Assigned features to [{enterprise_tier.id}] tier: [{enterprise_tier_features}]")
free_tier.assign_feature(dashboard_feature.id)
free_tier_features = ""
for f in free_tier.list_features():
    free_tier_features += f.id + " "
print(f"Assigned features to [{free_tier.id}] tier: [{free_tier_features}]")

# Assign tiers to users:
# 'enterprise' tier -> 'user1'
# 'free' tier -> 'user2'
user1.assign_pricing_tier(enterprise_tier.id)
print(f"Assigned tier [{enterprise_tier.id}] to user [{user1.id}]")
user2.assign_pricing_tier(free_tier.id)
print(f"Assigned tier [{free_tier.id}] to user [{user2.id}]")

# Pricing tiers checks
print(f"Does [{user1.id}] have access to the [{analytics_feature.id}] feature? (should be true) -> {user1.has_feature(analytics_feature.id)}")
print(f"Does [{user1.id}] have access to the [{dashboard_feature.id}] feature? (should be false) -> {user1.has_feature(dashboard_feature.id)}")
print(f"Does [{user2.id}] have access to the [{analytics_feature.id}] feature? (should be false) -> {user2.has_feature(analytics_feature.id)}")
print(f"Does [{user2.id}] have access to the [{dashboard_feature.id}] feature? (should be true) -> {user2.has_feature(dashboard_feature.id)}")
print("\n")


"""
Create authz sessions (for FE use)
"""
# Generate a self-service dashboard url for user2
print("---------- FE & Self-service Authz Tokens ----------")
print("Created self service dashboard url for user [" + user2.id + "]: " +
      warrant.Authz.create_self_service_url(tenant_id=tenant1.id, user_id=user2.id, self_service_strategy="rbac", redirect_url="http://example.com"))

# Authz sessions
print("Created authorization session token for user [" + user1.id + "]: " + warrant.Authz.create_authorization_session(user_id=user1.id))
print("Created authorization session token for user [" + user2.id + "]: " + warrant.Authz.create_authorization_session(user_id=user2.id))
print("\n")


"""
Create and query your own warrants
"""
print("---------- Create & Query Warrants ----------")
permission1 = warrant.Permission.create(id="permission1")
user1_subject = warrant.Subject("user", user1.id)
result = warrant.Authz.check("permission", "permission1", "member", user1_subject)
print(f"Does [{user1.id}] have the [permission1] permission? (should be false) -> {result}")
warrant.Warrant.create("permission", "permission1", "member", user1_subject)
print("Manually assigned [permission1] permission to [" + user1.id + "]")
result = warrant.Authz.check("permission", "permission1", "member", user1_subject)
print(f"Does [{user1.id}] have the [permission1] permission? (should be true) -> {result}")

# Create, check, and delete warrant with a policy
test_user_subject = warrant.Subject("user", "test-user")
warrant.Warrant.create("permission", "test-permission", "member", test_user_subject, "geo == 'us'")
print("Manually assigned [test-permission] permission to test-user with the context [geo == 'us']")
result = warrant.Authz.check("permission", "test-permission", "member", test_user_subject, {"geo": "us"})
print(f"Does test-user have the [test-permission] permission with the following context [geo == 'us']? (should be true) -> {result}")
result = warrant.Authz.check("permission", "test-permission", "member", test_user_subject, {"geo": "eu"})
print(f"Does test-user have the [test-permission] permission with the following context [geo == 'eu']? (should be false) -> {result}")
warrant.Warrant.delete("permission", "test-permission", "member", test_user_subject, "geo == 'us'")
print("Manually removed [test-permission] permission from test-user with the context [geo == 'us']")
warrant.WarrantObject.delete("user", "test-user")
print("Removed automatically created object user:test-user")
warrant.WarrantObject.delete("permission", "test-permission")
print("Removed automatically created object permission:test-permission")

# Query warrants
# warrants = warrant.Warrant.query(select="explicit warrants", for_clause="subject=user:"+user1.id, where="relation=member")
# print("Query warrants results:")
# for w in warrants:
#     print(f"[{w.object_type}:{w.object_id} {w.relation} {w.subject.object_type}:{w.subject.object_id}]")

warrant.Warrant.delete("permission", "permission1", "member", user1_subject)
print("Manually removed [permission1] permission from [" + user1.id + "]")
result = warrant.Authz.check("permission", "permission1", "member", user1_subject)
print(f"Does [{user1.id}] have the [permission1] permission? (should be false) -> {result}")
print("\n")


"""
Cleanup
"""
# Remove associations (not explicitly required if deleting objects, shown for completeness)
print("Cleaning up...")
user1.remove_permission(special_perm.id)
user1.remove_role(admin_role.id)
user2.remove_role(viewer_role.id)
admin_role.remove_permission(create_report_perm.id)
admin_role.remove_permission(delete_report_perm.id)
admin_role.remove_permission(view_report_perm.id)
viewer_role.remove_permission(view_report_perm.id)
tenant1.remove_user(user1.id)
warrant.Warrant.delete("tenant", tenant1.id, "admin", user2_subject)
enterprise_tier.remove_feature(analytics_feature.id)
free_tier.remove_feature(dashboard_feature.id)

warrant.WarrantObject.delete(object1.object_type, object1.object_id)
warrant.WarrantObject.delete(object2.object_type, object2.object_id)
warrant.User.delete(user1.id)
warrant.User.delete(user2.id)
warrant.Tenant.delete(tenant1.id)
warrant.Tenant.delete(tenant2.id)
warrant.Role.delete(admin_role.id)
warrant.Role.delete(viewer_role.id)
warrant.Permission.delete(create_report_perm.id)
warrant.Permission.delete(delete_report_perm.id)
warrant.Permission.delete(view_report_perm.id)
warrant.Permission.delete(special_perm.id)
warrant.Permission.delete(permission1.id)
warrant.Feature.delete(analytics_feature.id)
warrant.Feature.delete(dashboard_feature.id)
warrant.PricingTier.delete(enterprise_tier.id)
warrant.PricingTier.delete(free_tier.id)
print("Done")
