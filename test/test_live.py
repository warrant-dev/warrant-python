import warrant
import unittest


class LiveTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        warrant.api_key = "YOUR_API_KEY_HERE"
        warrant.api_endpoint = "https://api.warrant.dev"

    def test_crud_users(self):
        user1 = warrant.User.create()
        self.assertIsNotNone(user1.id)
        self.assertEqual(user1.meta, {})

        user2 = warrant.User.create("zz_some_id", {"email": "test@email.com"})
        refetched_user = warrant.User.get(user2.id)
        self.assertEqual(user2.id, refetched_user.id)
        self.assertEqual(user2.meta, {"email": "test@email.com"})

        user2.update({"email": "updated@email.com"})
        refetched_user = warrant.User.get(user2.id, opts={"Warrant-Token": "latest"})
        self.assertEqual(user2.id, "zz_some_id")
        self.assertEqual(user2.meta, {"email": "updated@email.com"})

        users_list = warrant.User.list({"limit": 10}, {"Warrant-Token": "latest"})
        self.assertEqual(len(users_list.results), 2)
        self.assertEqual(users_list.results[0].id, user1.id)
        self.assertEqual(users_list.results[1].id, refetched_user.id)

        warrant_token = warrant.User.delete(user1.id)
        self.assertIsNotNone(warrant_token)
        warrant_token = warrant.User.delete(user2.id)
        self.assertIsNotNone(warrant_token)
        users_list = warrant.User.list({"limit": 10}, {"Warrant-Token": "latest"})
        self.assertEqual(len(users_list.results), 0)

    def test_batch_create_and_delete_users(self):
        users = warrant.User.batch_create([
            {"userId": "user-a", "meta": {"name": "User A"}},
            {"userId": "user-b"},
            {"userId": "user-c", "meta": {"email": "user-c@email.com"}}
        ])
        self.assertEqual(len(users), 3)

        fetched_users = warrant.User.list({"limit": 10}, {"Warrant-Token": "latest"})
        self.assertEqual(len(fetched_users.results), 3)
        self.assertEqual(fetched_users.results[0].id, "user-a")
        self.assertEqual(fetched_users.results[0].meta, {"name": "User A"})
        self.assertEqual(fetched_users.results[1].id, "user-b")
        self.assertEqual(fetched_users.results[2].id, "user-c")
        self.assertEqual(fetched_users.results[2].meta, {"email": "user-c@email.com"})

        warrant.User.batch_delete([
            {"userId": "user-a", "meta": {"name": "User A"}},
            {"userId": "user-b"},
            {"userId": "user-c", "meta": {"email": "user-c@email.com"}}
        ])

        fetched_users = warrant.User.list({"limit": 10}, {"Warrant-Token": "latest"})
        self.assertEqual(len(fetched_users.results), 0)

    def test_crud_tenants(self):
        tenant1 = warrant.Tenant.create()
        self.assertIsNotNone(tenant1.id)
        self.assertEqual(tenant1.meta, {})

        tenant2 = warrant.Tenant.create("zz_some_tenant_id", {"name": "new_name"})
        refetched_tenant = warrant.Tenant.get(tenant2.id)
        self.assertEqual(tenant2.id, refetched_tenant.id)
        self.assertEqual(tenant2.meta, {"name": "new_name"})

        tenant2.update({"name": "updated_name"})
        refetched_tenant = warrant.Tenant.get(tenant2.id)
        self.assertEqual(refetched_tenant.id, "zz_some_tenant_id")
        self.assertEqual(refetched_tenant.meta, {"name": "updated_name"})

        tenants_list = warrant.Tenant.list({"limit": 10}, {"Warrant-Token": "latest"})
        self.assertEqual(len(tenants_list.results), 2)
        self.assertEqual(tenants_list.results[0].id, tenant1.id)
        self.assertEqual(tenants_list.results[1].id, refetched_tenant.id)

        warrant_token = warrant.Tenant.delete(tenant1.id)
        self.assertIsNotNone(warrant_token)
        warrant_token = warrant.Tenant.delete(tenant2.id)
        self.assertIsNotNone(warrant_token)
        tenants_list = warrant.Tenant.list({"limit": 10}, {"Warrant-Token": "latest"})
        self.assertEqual(len(tenants_list.results), 0)

    def test_batch_create_and_delete_tenants(self):
        tenants = warrant.Tenant.batch_create([
            {"tenantId": "tenant-a", "meta": {"name": "Tenant A"}},
            {"tenantId": "tenant-b"},
            {"tenantId": "tenant-c", "meta": {"description": "Company C"}}
        ])
        self.assertEqual(len(tenants), 3)

        fetched_tenants = warrant.Tenant.list({"limit": 10}, {"Warrant-Token": "latest"})
        self.assertEqual(len(fetched_tenants.results), 3)
        self.assertEqual(fetched_tenants.results[0].id, "tenant-a")
        self.assertEqual(fetched_tenants.results[0].meta, {"name": "Tenant A"})
        self.assertEqual(fetched_tenants.results[1].id, "tenant-b")
        self.assertEqual(fetched_tenants.results[2].id, "tenant-c")
        self.assertEqual(fetched_tenants.results[2].meta, {"description": "Company C"})

        warrant.Tenant.batch_delete([
            {"tenantId": "tenant-a", "meta": {"name": "Tenant A"}},
            {"tenantId": "tenant-b"},
            {"tenantId": "tenant-c", "meta": {"description": "Company C"}}
        ])

        fetched_tenants = warrant.Tenant.list({"limit": 10}, {"Warrant-Token": "latest"})
        self.assertEqual(len(fetched_tenants.results), 0)

    def test_crud_roles(self):
        admin_role = warrant.Role.create("admin", {"name": "Admin", "description": "The admin role"})
        self.assertEqual(admin_role.id, "admin")
        self.assertEqual(admin_role.meta, {"name": "Admin", "description": "The admin role"})

        viewer_role = warrant.Role.create("viewer", {"name": "Viewer", "description": "The viewer role"})
        refetched_role = warrant.Role.get(viewer_role.id, {"Warrant-Token": "latest"})
        self.assertEqual(viewer_role.id, refetched_role.id)
        self.assertEqual(viewer_role.meta, refetched_role.meta)

        viewer_role.update({"name": "Viewer Updated", "description": "Updated desc"})
        refetched_role = warrant.Role.get(viewer_role.id, {"Warrant-Token": "latest"})
        self.assertEqual(refetched_role.id, "viewer")
        self.assertEqual(refetched_role.meta, {"name": "Viewer Updated", "description": "Updated desc"})

        roles_list = warrant.Role.list({"limit": 10}, {"Warrant-Token": "latest"})
        self.assertEqual(len(roles_list.results), 2)
        self.assertEqual(roles_list.results[0].id, admin_role.id)
        self.assertEqual(roles_list.results[1].id, viewer_role.id)

        warrant_token = warrant.Role.delete(admin_role.id)
        self.assertIsNotNone(warrant_token)
        warrant_token = warrant.Role.delete(viewer_role.id)
        self.assertIsNotNone(warrant_token)
        roles_list = warrant.Role.list({"limit": 10}, {"Warrant-Token": "latest"})
        self.assertEqual(len(roles_list.results), 0)

    def test_crud_permissions(self):
        permission1 = warrant.Permission.create("perm1", {"name": "Permission 1", "description": "Permission with id 1"})
        self.assertEqual(permission1.id, "perm1")
        self.assertEqual(permission1.meta, {"name": "Permission 1", "description": "Permission with id 1"})

        permission2 = warrant.Permission.create("perm2", {"name": "Permission 2", "description": "Permission with id 2"})
        refetched_permission = warrant.Permission.get(permission2.id, {"Warrant-Token": "latest"})
        self.assertEqual(permission2.id, refetched_permission.id)
        self.assertEqual(permission2.meta, refetched_permission.meta)

        permission2.update({"name": "Permission 2 Updated", "description": "Updated desc"})
        refetched_permission = warrant.Permission.get("perm2", {"Warrant-Token": "latest"})
        self.assertEqual(refetched_permission.id, "perm2")
        self.assertEqual(refetched_permission.meta, {"name": "Permission 2 Updated", "description": "Updated desc"})

        permissions_list = warrant.Permission.list({"limit": 10}, {"Warrant-Token": "latest"})
        self.assertEqual(len(permissions_list.results), 2)
        self.assertEqual(permissions_list.results[0].id, permission1.id)
        self.assertEqual(permissions_list.results[1].id, permission2.id)

        warrant_token = warrant.Permission.delete(permission1.id)
        self.assertIsNotNone(warrant_token)
        warrant_token = warrant.Permission.delete(permission2.id)
        self.assertIsNotNone(warrant_token)
        permissions_list = warrant.Permission.list({"limit": 10}, {"Warrant-Token": "latest"})
        self.assertEqual(len(permissions_list.results), 0)

    def test_crud_pricing_tiers(self):
        tier1 = warrant.PricingTier.create("new-tier-1", {"name": "New Pricing Tier"})
        self.assertEqual(tier1.id, "new-tier-1")
        self.assertEqual(tier1.meta, {"name": "New Pricing Tier"})

        tier2 = warrant.PricingTier.create("tier-2")
        refetched_tier = warrant.PricingTier.get(tier2.id, {"Warrant-Token": "latest"})
        self.assertEqual(tier2.id, refetched_tier.id)
        self.assertEqual(tier2.meta, refetched_tier.meta)

        tier2.update({"name": "Tier 2", "description": "New pricing tier"})
        refetched_tier = warrant.PricingTier.get(tier2.id, {"Warrant-Token": "latest"})
        self.assertEqual(refetched_tier.id, "tier-2")
        self.assertEqual(refetched_tier.meta, {"name": "Tier 2", "description": "New pricing tier"})

        tiers_list = warrant.PricingTier.list({"limit": 10}, {"Warrant-Token": "latest"})
        self.assertEqual(len(tiers_list.results), 2)
        self.assertEqual(tiers_list.results[0].id, tier1.id)
        self.assertEqual(tiers_list.results[1].id, tier2.id)

        warrant_token = warrant.PricingTier.delete(tier1.id)
        self.assertIsNotNone(warrant_token)
        warrant_token = warrant.PricingTier.delete(tier2.id)
        self.assertIsNotNone(warrant_token)
        tiers_list = warrant.PricingTier.list({"limit": 10}, {"Warrant-Token": "latest"})
        self.assertEqual(len(tiers_list.results), 0)

    def test_crud_features(self):
        feature1 = warrant.Feature.create("new-feature", {"name": "New Feature"})
        self.assertEqual(feature1.id, "new-feature")
        self.assertEqual(feature1.meta, {"name": "New Feature"})

        feature2 = warrant.Feature.create("feature-2")
        refetched_feature = warrant.Feature.get(feature2.id, {"Warrant-Token": "latest"})
        self.assertEqual(feature2.id, refetched_feature.id)
        self.assertEqual(feature2.meta, refetched_feature.meta)

        feature2.update({"name": "Feature 2", "description": "Second feature"})
        refetched_feature = warrant.Feature.get(feature2.id, {"Warrant-Token": "latest"})
        self.assertEqual(refetched_feature.id, "feature-2")
        self.assertEqual(refetched_feature.meta, {"name": "Feature 2", "description": "Second feature"})

        features_list = warrant.Feature.list({"limit": 10}, {"Warrant-Token": "latest"})
        self.assertEqual(len(features_list.results), 2)
        self.assertEqual(features_list.results[0].id, feature2.id)
        self.assertEqual(features_list.results[1].id, feature1.id)

        warrant_token = warrant.Feature.delete(feature1.id)
        self.assertIsNotNone(warrant_token)
        warrant_token = warrant.Feature.delete(feature2.id)
        self.assertIsNotNone(warrant_token)
        features_list = warrant.Feature.list({"limit": 10}, {"Warrant-Token": "latest"})
        self.assertEqual(len(features_list.results), 0)

    def test_crud_objects(self):
        object1 = warrant.Object.create("document")
        self.assertEqual(object1.object_type, "document")
        self.assertIsNotNone(object1.object_id)
        self.assertEqual(object1.meta, {})

        object2 = warrant.Object.create("folder", "planning")
        refetched_object = warrant.Object.get(object2.object_type, object2.object_id, {"Warrant-Token": "latest"})
        self.assertEqual(object2.object_type, refetched_object.object_type)
        self.assertEqual(object2.object_id, refetched_object.object_id)
        self.assertEqual(object2.meta, refetched_object.meta)

        object2.update({"description": "Second document"})
        refetched_object = warrant.Object.get(object2.object_type, object2.object_id, {"Warrant-Token": "latest"})
        self.assertEqual(refetched_object.object_type, "folder")
        self.assertEqual(refetched_object.object_id, "planning")
        self.assertEqual(refetched_object.meta, {"description": "Second document"})

        objects_list = warrant.Object.list({"sortBy": "createdAt", "limit": 10}, {"Warrant-Token": "latest"})
        self.assertEqual(len(objects_list.results), 2)
        self.assertEqual(objects_list.results[0].object_type, object1.object_type)
        self.assertEqual(objects_list.results[0].object_id, object1.object_id)
        self.assertEqual(objects_list.results[1].object_type, object2.object_type)
        self.assertEqual(objects_list.results[1].object_id, object2.object_id)

        warrant_token = warrant.Object.delete(object1.object_type, object1.object_id)
        self.assertIsNotNone(warrant_token)
        warrant_token = warrant.Object.delete(object2.object_type, object2.object_id)
        self.assertIsNotNone(warrant_token)
        objects_list = warrant.Object.list({"sortBy": "createdAt", "limit": 10}, {"Warrant-Token": "latest"})
        self.assertEqual(len(objects_list.results), 0)

    def test_batch_create_delete_objects(self):
        objects = warrant.Object.batch_create([
            {"objectType": "document", "objectId": "document-a"},
            {"objectType": "document", "objectId": "document-b"},
            {"objectType": "folder", "objectId": "resources", "meta": {"description": "Helpful documents"}}
        ])
        self.assertEqual(len(objects), 3)

        objects_list = warrant.Object.list({"limit": 10}, {"Warrant-Token": "latest"})
        self.assertEqual(len(objects_list.results), 3)
        self.assertEqual(objects_list.results[0].object_type, "document")
        self.assertEqual(objects_list.results[0].object_id, "document-a")
        self.assertEqual(objects_list.results[1].object_type, "document")
        self.assertEqual(objects_list.results[1].object_id, "document-b")
        self.assertEqual(objects_list.results[2].object_type, "folder")
        self.assertEqual(objects_list.results[2].object_id, "resources")
        self.assertEqual(objects_list.results[2].meta, {"description": "Helpful documents"})

        warrant.Object.batch_delete([
            {"objectType": "document", "objectId": "document-a"},
            {"objectType": "document", "objectId": "document-b"},
            {"objectType": "folder", "objectId": "resources", "meta": {"description": "Helpful documents"}}
        ])
        objects_list = warrant.Object.list({"limit": 10}, {"Warrant-Token": "latest"})
        self.assertEqual(len(objects_list.results), 0)

    def test_multitenancy_example(self):
        # Create users
        user1 = warrant.User.create()
        user2 = warrant.User.create()

        # Create tenants
        tenant1 = warrant.Tenant.create("tenant-1", {"name": "Tenant 1"})
        tenant2 = warrant.Tenant.create("tenant-2", {"name": "Tenant 2"})

        user1_tenants_list = warrant.Tenant.list_for_user(user1.id, {"limit": 100}, {"Warrant-Token": "latest"})
        tenant1_users_list = warrant.User.list_for_tenant(tenant1.id, {"limit": 100}, {"Warrant-Token": "latest"})
        self.assertEqual(len(user1_tenants_list.results), 0)
        self.assertEqual(len(tenant1_users_list.results), 0)

        # Assign user1 -> tenant1
        tenant1.assign_user(user1.id, "member")

        user1_tenants_list = warrant.Tenant.list_for_user(user1.id, {"limit": 100}, {"Warrant-Token": "latest"})
        self.assertEqual(len(user1_tenants_list.results), 1)
        self.assertEqual(user1_tenants_list.results[0].object_id, "tenant-1")
        self.assertEqual(user1_tenants_list.results[0].meta, {"name": "Tenant 1"})

        tenant1_users_list = warrant.User.list_for_tenant(tenant1.id, {"limit": 100}, {"Warrant-Token": "latest"})
        self.assertEqual(len(tenant1_users_list.results), 1)
        self.assertEqual(tenant1_users_list.results[0].object_id, user1.id)
        self.assertEqual(tenant1_users_list.results[0].meta, {})

        # Remove user1 -> tenant1
        tenant1.remove_user(user1.id, "member")

        user1_tenants_list = warrant.Tenant.list_for_user(user1.id, {"limit": 100}, {"Warrant-Token": "latest"})
        self.assertEqual(len(user1_tenants_list.results), 0)

        tenant1_users_list = warrant.User.list_for_tenant(tenant1.id, {"limit": 100}, {"Warrant-Token": "latest"})
        self.assertEqual(len(tenant1_users_list.results), 0)

        warrant_token = warrant.User.delete(user1.id)
        self.assertIsNotNone(warrant_token)
        warrant_token = warrant.User.delete(user2.id)
        self.assertIsNotNone(warrant_token)
        warrant_token = warrant.Tenant.delete(tenant1.id)
        self.assertIsNotNone(warrant_token)
        warrant_token = warrant.Tenant.delete(tenant2.id)
        self.assertIsNotNone(warrant_token)

    def test_rbac_example(self):
        # Create users
        admin_user = warrant.User.create()
        viewer_user = warrant.User.create()

        # Create roles
        admin_role = warrant.Role.create("admin", {"name": "Admin", "description": "The admin role"})
        viewer_role = warrant.Role.create("viewer", {"name": "Viewer", "description": "The viewer role"})

        # Create permissions
        create_permission = warrant.Permission.create("create-report", {"name": "Create Report", "description": "Permission to create reports"})
        view_permission = warrant.Permission.create("view-report", {"name": "View Report", "description": "Permission to view reports"})

        admin_user_roles_list = warrant.Role.list_for_user(admin_user.id, {"limit": 100}, {"Warrant-Token": "latest"})
        self.assertEqual(len(admin_user_roles_list.results), 0)

        admin_role_permissions_list = warrant.Permission.list_for_role(admin_role.id, {"limit": 100}, {"Warrant-Token": "latest"})
        self.assertEqual(len(admin_role_permissions_list.results), 0)

        admin_user_has_permission = admin_user.has_permission(create_permission.id, {"Warrant-Token": "latest"})
        self.assertEqual(admin_user_has_permission, False)

        # Assign 'create-report' -> admin role -> admin user
        admin_role.assign_permission(create_permission.id, "member")
        admin_user.assign_role(admin_role.id, "member")

        admin_user_has_permission = admin_user.has_permission(create_permission.id, {"Warrant-Token": "latest"})
        self.assertEqual(admin_user_has_permission, True)

        admin_user_roles_list = warrant.Role.list_for_user(admin_user.id, {"limit": 100}, {"Warrant-Token": "latest"})
        self.assertEqual(len(admin_user_roles_list.results), 1)
        self.assertEqual(admin_user_roles_list.results[0].object_id, admin_role.id)
        self.assertEqual(admin_user_roles_list.results[0].meta, {"name": "Admin", "description": "The admin role"})

        admin_role_permissions_list = warrant.Permission.list_for_role(admin_role.id, {"limit": 100}, {"Warrant-Token": "latest"})
        self.assertEqual(len(admin_role_permissions_list.results), 1)
        self.assertEqual(admin_role_permissions_list.results[0].object_id, create_permission.id)
        self.assertEqual(admin_role_permissions_list.results[0].meta, {"name": "Create Report", "description": "Permission to create reports"})

        # Remove 'create-report' -> admin role -> admin user
        admin_role.remove_permission(create_permission.id, "member")
        admin_user.remove_role(admin_role.id, "member")

        admin_user_has_permission = admin_user.has_permission(create_permission.id, {"Warrant-Token": "latest"})
        self.assertEqual(admin_user_has_permission, False)

        admin_user_roles_list = warrant.Role.list_for_user(admin_user.id, {"limit": 100}, {"Warrant-Token": "latest"})
        self.assertEqual(len(admin_user_roles_list.results), 0)

        admin_role_permissions_list = warrant.Permission.list_for_role(admin_role.id, {"limit": 100}, {"Warrant-Token": "latest"})
        self.assertEqual(len(admin_role_permissions_list.results), 0)

        # Assign 'view-report' -> viewer user
        viewer_user_has_permission = viewer_user.has_permission(view_permission.id, {"Warrant-Token": "latest"})
        self.assertEqual(viewer_user_has_permission, False)

        viewer_user_permissions_list = warrant.Permission.list_for_user(viewer_user.id, {"limit": 100}, {"Warrant-Token": "latest"})
        self.assertEqual(len(viewer_user_permissions_list.results), 0)

        viewer_user.assign_permission(view_permission.id, "member")

        viewer_user_has_permission = viewer_user.has_permission(view_permission.id, {"Warrant-Token": "latest"})
        self.assertEqual(viewer_user_has_permission, True)

        viewer_user_permissions_list = warrant.Permission.list_for_user(viewer_user.id, {"limit": 100}, {"Warrant-Token": "latest"})
        self.assertEqual(len(viewer_user_permissions_list.results), 1)
        self.assertEqual(viewer_user_permissions_list.results[0].object_id, view_permission.id)
        self.assertEqual(viewer_user_permissions_list.results[0].meta, {"name": "View Report", "description": "Permission to view reports"})

        viewer_user.remove_permission(view_permission.id, "member")

        viewer_user_has_permission = viewer_user.has_permission(view_permission.id, {"Warrant-Token": "latest"})
        self.assertEqual(viewer_user_has_permission, False)

        viewer_user_permissions_list = warrant.Permission.list_for_user(viewer_user.id, {"limit": 100}, {"Warrant-Token": "latest"})
        self.assertEqual(len(viewer_user_permissions_list.results), 0)

        # Clean up
        warrant_token = warrant.User.delete(admin_user.id)
        self.assertIsNotNone(warrant_token)
        warrant_token = warrant.User.delete(viewer_user.id)
        self.assertIsNotNone(warrant_token)
        warrant_token = warrant.Role.delete(admin_role.id)
        self.assertIsNotNone(warrant_token)
        warrant_token = warrant.Role.delete(viewer_role.id)
        self.assertIsNotNone(warrant_token)
        warrant_token = warrant.Permission.delete(create_permission.id)
        self.assertIsNotNone(warrant_token)
        warrant_token = warrant.Permission.delete(view_permission.id)
        self.assertIsNotNone(warrant_token)

    def test_pricing_tiers_features_and_users_example(self):
        # Create users
        free_user = warrant.User.create()
        paid_user = warrant.User.create()

        # Create pricing tiers
        free_tier = warrant.PricingTier.create("free", {"name": "Free Tier"})
        paid_tier = warrant.PricingTier.create("paid")

        # Create features
        custom_feature = warrant.Feature.create("custom-feature", {"name": "Custom Feature"})
        feature1 = warrant.Feature.create("feature-1")
        feature2 = warrant.Feature.create("feature-2")

        # Assign 'custom-feature' -> paid user
        paid_user_has_feature = paid_user.has_feature(custom_feature.id, {"Warrant-Token": "latest"})
        self.assertEqual(paid_user_has_feature, False)

        paid_user_features_list = warrant.Feature.list_for_user(paid_user.id, {"limit": 100}, {"Warrant-Token": "latest"})
        self.assertEqual(len(paid_user_features_list.results), 0)

        paid_user.assign_feature(custom_feature.id, "member")

        paid_user_has_feature = paid_user.has_feature(custom_feature.id, {"Warrant-Token": "latest"})
        self.assertEqual(paid_user_has_feature, True)

        paid_user_features_list = warrant.Feature.list_for_user(paid_user.id, {"limit": 100}, {"Warrant-Token": "latest"})
        self.assertEqual(len(paid_user_features_list.results), 1)
        self.assertEqual(paid_user_features_list.results[0].object_id, "custom-feature")
        self.assertEqual(paid_user_features_list.results[0].meta, {"name": "Custom Feature"})

        paid_user.remove_feature(custom_feature.id, "member")

        paid_user_has_feature = paid_user.has_feature(custom_feature.id, {"Warrant-Token": "latest"})
        self.assertEqual(paid_user_has_feature, False)

        paid_user_features_list = warrant.Feature.list_for_user(paid_user.id, {"limit": 100}, {"Warrant-Token": "latest"})
        self.assertEqual(len(paid_user_features_list.results), 0)

        # Assign 'feature-1' -> 'free' tier -> free user
        free_user_has_feature = free_user.has_feature(feature1.id, {"Warrant-Token": "latest"})
        self.assertEqual(free_user_has_feature, False)

        free_tier_features_list = warrant.Feature.list_for_pricing_tier(free_tier.id, {"limit": 100}, {"Warrant-Token": "latest"})
        self.assertEqual(len(free_tier_features_list.results), 0)

        free_user_tiers_list = warrant.PricingTier.list_for_user(free_user.id, {"limit": 100}, {"Warrant-Token": "latest"})
        self.assertEqual(len(free_user_tiers_list.results), 0)

        free_tier.assign_feature(feature1.id, "member")
        free_user.assign_pricing_tier(free_tier.id, "member")

        free_user_has_feature = free_user.has_feature(feature1.id, {"Warrant-Token": "latest"})
        self.assertEqual(free_user_has_feature, True)

        free_tier_features_list = warrant.Feature.list_for_pricing_tier(free_tier.id, {"limit": 100}, {"Warrant-Token": "latest"})
        self.assertEqual(len(free_tier_features_list.results), 1)
        self.assertEqual(free_tier_features_list.results[0].object_id, "feature-1")
        self.assertEqual(free_tier_features_list.results[0].meta, {})

        free_user_tiers_list = warrant.PricingTier.list_for_user(free_user.id, {"limit": 100}, {"Warrant-Token": "latest"})
        self.assertEqual(len(free_user_tiers_list.results), 1)
        self.assertEqual(free_user_tiers_list.results[0].object_id, "free")
        self.assertEqual(free_user_tiers_list.results[0].meta, {"name": "Free Tier"})

        free_tier.remove_feature(feature1.id, "member")
        free_user.remove_pricing_tier(free_tier.id, "member")

        free_user_has_feature = free_user.has_feature(feature1.id, {"Warrant-Token": "latest"})
        self.assertEqual(free_user_has_feature, False)

        free_tier_features_list = warrant.Feature.list_for_pricing_tier(free_tier.id, {"limit": 100}, {"Warrant-Token": "latest"})
        self.assertEqual(len(free_tier_features_list.results), 0)

        free_user_tiers_list = warrant.PricingTier.list_for_user(free_user.id, {"limit": 100}, {"Warrant-Token": "latest"})
        self.assertEqual(len(free_user_tiers_list.results), 0)

        # Clean up
        warrant_token = warrant.User.delete(free_user.id)
        self.assertIsNotNone(warrant_token)
        warrant_token = warrant.User.delete(paid_user.id)
        self.assertIsNotNone(warrant_token)
        warrant_token = warrant.PricingTier.delete(free_tier.id)
        self.assertIsNotNone(warrant_token)
        warrant_token = warrant.PricingTier.delete(paid_tier.id)
        self.assertIsNotNone(warrant_token)
        warrant_token = warrant.Feature.delete(custom_feature.id)
        self.assertIsNotNone(warrant_token)
        warrant_token = warrant.Feature.delete(feature1.id)
        self.assertIsNotNone(warrant_token)
        warrant_token = warrant.Feature.delete(feature2.id)
        self.assertIsNotNone(warrant_token)

    def test_pricing_tiers_features_and_tenants_example(self):
        # Create tenants
        free_tenant = warrant.Tenant.create()
        paid_tenant = warrant.Tenant.create()

        # Create pricing tiers
        free_tier = warrant.PricingTier.create("free", {"name": "Free Tier"})
        paid_tier = warrant.PricingTier.create("paid")

        # Create features
        custom_feature = warrant.Feature.create("custom-feature", {"name": "Custom Feature"})
        feature1 = warrant.Feature.create("feature-1", {"description": "First feature"})
        feature2 = warrant.Feature.create("feature-2")

        # Assign 'custom-feature' -> paid tenant
        paid_tenant_has_feature = paid_tenant.has_feature(custom_feature.id, {"Warrant-Token": "latest"})
        self.assertEqual(paid_tenant_has_feature, False)

        paid_tenant_features_list = paid_tenant.list_features({"limit": 100}, {"Warrant-Token": "latest"})
        self.assertEqual(len(paid_tenant_features_list.results), 0)

        paid_tenant.assign_feature(custom_feature.id, "member")

        paid_tenant_has_feature = paid_tenant.has_feature(custom_feature.id, {"Warrant-Token": "latest"})
        self.assertEqual(paid_tenant_has_feature, True)

        paid_tenant_features_list = paid_tenant.list_features({"limit": 100}, {"Warrant-Token": "latest"})
        self.assertEqual(len(paid_tenant_features_list.results), 1)
        self.assertEqual(paid_tenant_features_list.results[0].object_id, "custom-feature")
        self.assertEqual(paid_tenant_features_list.results[0].meta, {"name": "Custom Feature"})

        paid_tenant.remove_feature(custom_feature.id, "member")

        paid_tenant_has_feature = paid_tenant.has_feature(custom_feature.id, {"Warrant-Token": "latest"})
        self.assertEqual(paid_tenant_has_feature, False)

        paid_tenant_features_list = paid_tenant.list_features({"limit": 100}, {"Warrant-Token": "latest"})
        self.assertEqual(len(paid_tenant_features_list.results), 0)

        # Assign 'feature-1' -> free tier -> free tenant
        free_tenant_has_feature = free_tenant.has_feature(feature1.id, {"Warrant-Token": "latest"})
        self.assertEqual(free_tenant_has_feature, False)

        free_tier_features_list = free_tier.list_features({"limit": 100}, {"Warrant-Token": "latest"})
        self.assertEqual(len(free_tier_features_list.results), 0)

        free_tenant_tiers_list = free_tenant.list_pricing_tiers({"limit": 100}, {"Warrant-Token": "latest"})
        self.assertEqual(len(free_tenant_tiers_list.results), 0)

        free_tier.assign_feature(feature1.id, "member")
        free_tenant.assign_pricing_tier(free_tier.id, "member")

        free_tenant_has_feature = free_tenant.has_feature(feature1.id, {"Warrant-Token": "latest"})
        self.assertEqual(free_tenant_has_feature, True)

        free_tier_features_list = free_tier.list_features({"limit": 100}, {"Warrant-Token": "latest"})
        self.assertEqual(len(free_tier_features_list.results), 1)
        self.assertEqual(free_tier_features_list.results[0].object_id, "feature-1")
        self.assertEqual(free_tier_features_list.results[0].meta, {"description": "First feature"})

        free_tenant_tiers_list = free_tenant.list_pricing_tiers({"limit": 100}, {"Warrant-Token": "latest"})
        self.assertEqual(len(free_tenant_tiers_list.results), 1)
        self.assertEqual(free_tenant_tiers_list.results[0].object_id, "free")
        self.assertEqual(free_tenant_tiers_list.results[0].meta, {"name": "Free Tier"})

        free_tier.remove_feature(feature1.id, "member")
        free_tenant.remove_pricing_tier(free_tier.id, "member")

        free_tenant_has_feature = free_tenant.has_feature(feature1.id, {"Warrant-Token": "latest"})
        self.assertEqual(free_tenant_has_feature, False)

        free_tier_features_list = free_tier.list_features({"limit": 100}, {"Warrant-Token": "latest"})
        self.assertEqual(len(free_tier_features_list.results), 0)

        free_tenant_tiers_list = free_tenant.list_pricing_tiers({"limit": 100}, {"Warrant-Token": "latest"})
        self.assertEqual(len(free_tenant_tiers_list.results), 0)

        # Clean up
        warrant_token = warrant.Tenant.delete(free_tenant.id)
        self.assertIsNotNone(warrant_token)
        warrant_token = warrant.Tenant.delete(paid_tenant.id)
        self.assertIsNotNone(warrant_token)
        warrant_token = warrant.PricingTier.delete(free_tier.id)
        self.assertIsNotNone(warrant_token)
        warrant_token = warrant.PricingTier.delete(paid_tier.id)
        self.assertIsNotNone(warrant_token)
        warrant_token = warrant.Feature.delete(custom_feature.id)
        self.assertIsNotNone(warrant_token)
        warrant_token = warrant.Feature.delete(feature1.id)
        self.assertIsNotNone(warrant_token)
        warrant_token = warrant.Feature.delete(feature2.id)
        self.assertIsNotNone(warrant_token)

    def test_sessions(self):
        user = warrant.User.create()
        tenant = warrant.Tenant.create()

        tenant.assign_user(user.id, "admin")

        user_authz_session = warrant.Authz.create_authorization_session(user.id)
        self.assertIsNotNone(user_authz_session)

        user_ss_dash_url = warrant.Authz.create_self_service_url(tenant.id, user.id, "fgac", "http://localhost:8080")
        self.assertIsNotNone(user_ss_dash_url)

        warrant.User.delete(user.id)
        warrant.Tenant.delete(tenant.id)

    def test_warrants(self):
        new_user = warrant.User.create()
        new_permission = warrant.Permission.create("perm1", {"name": "Permission 1", "description": "Permission 1"})

        user_has_permission = warrant.Authz.check(
            new_permission.object_type,
            new_permission.id,
            "member",
            {"objectType": new_user.object_type, "objectId": new_user.id},
            opts={"Warrant-Token": "latest"}
        )
        self.assertEqual(user_has_permission, False)

        warrant.Warrant.create(new_permission.object_type, new_permission.id, "member", {"objectType": new_user.object_type, "objectId": new_user.id})

        user_has_permission = warrant.Authz.check(
            new_permission.object_type,
            new_permission.id,
            "member",
            {"objectType": new_user.object_type, "objectId": new_user.id},
            opts={"Warrant-Token": "latest"}
        )
        self.assertEqual(user_has_permission, True)

        query = f"select permission where user:{new_user.id} is member"
        response = warrant.Warrant.query(query)

        self.assertEqual(len(response.results), 1)
        self.assertEqual(response.results[0].object_type, "permission")
        self.assertEqual(response.results[0].object_id, "perm1")
        self.assertEqual(response.results[0].warrant.relation, "member")

        warrant.Warrant.delete(new_permission.object_type, new_permission.id, "member", {"objectType": new_user.object_type, "objectId": new_user.id})

        user_has_permission = warrant.Authz.check(
            new_permission.object_type,
            new_permission.id,
            "member",
            {"objectType": new_user.object_type, "objectId": new_user.id},
            opts={"Warrant-Token": "latest"}
        )
        self.assertEqual(user_has_permission, False)

        warrant.User.delete(new_user.id)
        warrant.Permission.delete(new_permission.id)

    def test_batch_create_delete_warrants(self):
        new_user = warrant.User.create()
        permission1 = warrant.Permission.create("perm1", {"name": "Permission 1", "description": "Permission 1"})
        permission2 = warrant.Permission.create("perm2", {"name": "Permission 2", "description": "Permission 2"})

        user_has_permission1 = warrant.Authz.check(
            permission1.object_type,
            permission1.id,
            "member",
            {"objectType": new_user.object_type, "objectId": new_user.id},
            opts={"Warrant-Token": "latest"}
        )
        self.assertEqual(user_has_permission1, False)

        user_has_permission2 = warrant.Authz.check(
            permission2.object_type,
            permission2.id,
            "member",
            {"objectType": new_user.object_type, "objectId": new_user.id},
            opts={"Warrant-Token": "latest"}
        )
        self.assertEqual(user_has_permission2, False)

        perm1_warrant = warrant.Warrant({"objectType": "permission", "objectId": permission1.id, "relation": "member", "subject": warrant.Subject("user", new_user.id)})
        user_has_permissions = warrant.Authz.check_many(
            warrant.CheckOp.ALL_OF,
            [
                perm1_warrant,
                {"objectType": permission2.object_type, "objectId": permission2.id, "relation": "member", "subject": {"objectType": new_user.object_type, "objectId": new_user.id}}
            ],
            opts={"Warrant-Token": "latest"}
        )
        self.assertEqual(user_has_permissions, False)

        warrants = warrant.Warrant.batch_create([
            {"objectType": permission1.object_type, "objectId": permission1.id, "relation": "member", "subject": {"objectType": new_user.object_type, "objectId": new_user.id}},
            {"objectType": permission2.object_type, "objectId": permission2.id, "relation": "member", "subject": {"objectType": new_user.object_type, "objectId": new_user.id}}
        ])
        self.assertEqual(len(warrants), 2)

        user_has_permission1 = warrant.Authz.check(
            permission1.object_type,
            permission1.id,
            "member",
            {"objectType": new_user.object_type, "objectId": new_user.id},
            opts={"Warrant-Token": "latest"}
        )
        self.assertEqual(user_has_permission1, True)

        user_has_permission2 = warrant.Authz.check(
            permission2.object_type,
            permission2.id,
            "member",
            {"objectType": new_user.object_type, "objectId": new_user.id},
            opts={"Warrant-Token": "latest"}
        )
        self.assertEqual(user_has_permission2, True)

        user_has_permissions = warrant.Authz.check_many(
            warrant.CheckOp.ALL_OF,
            [
                perm1_warrant,
                {"objectType": permission2.object_type, "objectId": permission2.id, "relation": "member", "subject": {"objectType": new_user.object_type, "objectId": new_user.id}}
            ],
            opts={"Warrant-Token": "latest"}
        )
        self.assertEqual(user_has_permissions, True)

        warrant.Warrant.batch_delete([
            {"objectType": permission1.object_type, "objectId": permission1.id, "relation": "member", "subject": {"objectType": new_user.object_type, "objectId": new_user.id}},
            {"objectType": permission2.object_type, "objectId": permission2.id, "relation": "member", "subject": {"objectType": new_user.object_type, "objectId": new_user.id}}
        ])
        warrant.Object.batch_delete([
            {"objectType": permission1.object_type, "objectId": permission1.id},
            {"objectType": permission2.object_type, "objectId": permission2.id},
            {"objectType": new_user.object_type, "objectId": new_user.id},
        ])

    def test_warrant_with_policy(self):
        warrant.Warrant.create("permission", "test-permission", "member", {"objectType": "user", "objectId": "user-1"}, "geo == 'us'")

        check_result = warrant.Authz.check(
            "permission",
            "test-permission",
            "member",
            {"objectType": "user", "objectId": "user-1"},
            {"geo": "us"},
            {"Warrant-Token": "latest"}
        )
        self.assertEqual(check_result, True)

        check_result = warrant.Authz.check(
            "permission",
            "test-permission",
            "member",
            {"objectType": "user", "objectId": "user-1"},
            {"geo": "eu"},
            {"Warrant-Token": "latest"}
        )
        self.assertEqual(check_result, False)

        # Clean up
        warrant.Warrant.delete("permission", "test-permission", "member", {"objectType": "user", "objectId": "user-1"}, "geo == 'us'")
        warrant.Permission.delete("test-permission")
        warrant.User.delete("user-1")
