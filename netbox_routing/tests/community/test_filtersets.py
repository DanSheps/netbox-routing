from django.test import TestCase

from ipam.models import Role
from netbox_routing.filtersets.community import *
from netbox_routing.models.community import *

__all__ = (
    'CommunityTestCase',
    'CommunityListTestCase',
    'CommunityListEntryTestCase',
)

from tenancy.models import Tenant


class CommunityTestCase(TestCase):
    queryset = Community.objects.all()
    filterset = CommunityFilterSet

    @classmethod
    def setUpTestData(cls):
        cls.tenants = (
            Tenant(name='Test Tenant 1', slug='test-tenant-1'),
            Tenant(name='Test Tenant 2', slug='test-tenant-2'),
        )
        Tenant.objects.bulk_create(cls.tenants)

        cls.roles = (
            Role(name='Test Role 1', slug='test-role-1'),
            Role(name='Test Role 2', slug='test-role-2'),
        )
        Role.objects.bulk_create(cls.roles)

        cls.communities = [
            Community(
                community='64512',
                status='active',
                role=cls.roles[0],
                tenant=cls.tenants[0],
            ),
            Community(
                community='64513',
                status='reserved',
                role=cls.roles[0],
                tenant=cls.tenants[1],
            ),
            Community(
                community='64514',
                status='active',
                role=cls.roles[1],
                tenant=cls.tenants[1],
            ),
            Community(
                community='64515',
                status='reserved',
                role=cls.roles[1],
                tenant=cls.tenants[0],
            ),
        ]
        Community.objects.bulk_create(cls.communities)

    def test_q(self):
        params = {'q': '64512'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_status(self):
        params = {'status': 'active'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {'status': 'reserved'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {'status': 'deprecated'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 0)

    def test_role(self):
        params = {
            'role_id': [
                self.roles[1].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

        params = {
            'role': [
                self.roles[1].name,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_tenant(self):
        params = {
            'tenant_id': [
                self.tenants[1].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

        params = {
            'tenant': [
                self.tenants[1].slug,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)


class CommunityListTestCase(TestCase):
    queryset = CommunityList.objects.all()
    filterset = CommunityListFilterSet

    @classmethod
    def setUpTestData(cls):
        cls.tenants = (
            Tenant(name='Test Tenant 1', slug='test-tenant-1'),
            Tenant(name='Test Tenant 2', slug='test-tenant-2'),
        )
        Tenant.objects.bulk_create(cls.tenants)

        cls.community_lists = [
            CommunityList(
                name='Test Community List 1-1',
                tenant=cls.tenants[0],
            ),
            CommunityList(
                name='Test Community List 1-2',
                tenant=cls.tenants[1],
            ),
            CommunityList(name='Test Community List 2-1', tenant=cls.tenants[1]),
            CommunityList(name='Test Community List 2-2', tenant=cls.tenants[0]),
        ]
        CommunityList.objects.bulk_create(cls.community_lists)

    def test_q(self):
        params = {'q': 'Test Community List 1-'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_tenant(self):
        params = {
            'tenant_id': [
                self.tenants[1].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

        params = {
            'tenant': [
                self.tenants[1].slug,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)


class CommunityListEntryTestCase(TestCase):
    queryset = CommunityListEntry.objects.all()
    filterset = CommunityListEntryFilterSet

    @classmethod
    def setUpTestData(cls):
        cls.tenants = (Tenant(name='Test Tenant 1', slug='test-tenant-1'),)
        Tenant.objects.bulk_create(cls.tenants)

        cls.roles = (Role(name='Test Role 1', slug='test-role-1'),)
        Role.objects.bulk_create(cls.roles)

        cls.communities = [
            Community(
                community='64512',
                status='active',
                role=cls.roles[0],
                tenant=cls.tenants[0],
            ),
            Community(
                community='64513',
                status='reserved',
                role=cls.roles[0],
                tenant=cls.tenants[0],
            ),
        ]
        Community.objects.bulk_create(cls.communities)

        cls.community_lists = [
            CommunityList(
                name='Test Community List 1',
                tenant=cls.tenants[0],
            ),
            CommunityList(
                name='Test Community List 2',
                tenant=cls.tenants[0],
            ),
        ]
        CommunityList.objects.bulk_create(cls.community_lists)

        cls.community_list_entries = [
            CommunityListEntry(
                community_list=cls.community_lists[0],
                community=cls.communities[0],
                action='permit',
            ),
            CommunityListEntry(
                community_list=cls.community_lists[0],
                community=cls.communities[1],
                action='permit',
            ),
            CommunityListEntry(
                community_list=cls.community_lists[1],
                community=cls.communities[0],
                action='permit',
            ),
            CommunityListEntry(
                community_list=cls.community_lists[1],
                community=cls.communities[1],
                action='permit',
            ),
        ]
        CommunityListEntry.objects.bulk_create(cls.community_list_entries)

    def test_q(self):
        params = {'q': 'Test Community List 1'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_community(self):
        params = {
            'community_id': [
                self.communities[1].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

        params = {
            'community': [
                self.communities[1].community,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_community_list(self):
        params = {
            'community_list_id': [
                self.community_lists[1].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

        params = {
            'community_list': [
                self.community_lists[1].name,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
