from ipam.models import Role
from netbox_routing.choices import ActionChoices
from utilities.testing import ViewTestCases
from tenancy.models import Tenant

from netbox_routing.models.community import *

__all__ = (
    'CommunityTestCase',
    'CommunityListTestCase',
    'CommunityListEntryTestCase',
)


class CommunityTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    # ViewTestCases.BulkImportObjectsViewTestCase,
    model = Community

    @classmethod
    def setUpTestData(cls):
        cls.tenant = Tenant.objects.create(name='Tenant 1')
        cls.role = Role.objects.create(name='Role 1')

        cls.communities = (
            Community(
                community='64512',
                status='active',
            ),
            Community(
                community='64513',
                status='active',
                role=cls.role,
            ),
            Community(
                community='64514',
                status='active',
                role=cls.role,
                tenant=cls.tenant,
            ),
        )

        Community.objects.bulk_create(cls.communities)

        cls.form_data = {
            'community': '64515',
            'status': 'active',
        }

        cls.bulk_edit_data = {
            'description': 'Test Description',
        }

    def _get_base_url(self):
        return 'plugins:netbox_routing:community_{}'


class CommunityListTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    # ViewTestCases.BulkImportObjectsViewTestCase,
    model = CommunityList

    @classmethod
    def setUpTestData(cls):
        cls.tenant = Tenant.objects.create(name='Tenant 1')

        cls.community_list = (
            CommunityList(
                name='Community List 1',
            ),
            CommunityList(
                name='Community List 2',
            ),
            CommunityList(
                name='Community List 3',
                tenant=cls.tenant,
            ),
        )

        CommunityList.objects.bulk_create(cls.community_list)

        cls.form_data = {
            'name': 'Community List X',
        }

        cls.bulk_edit_data = {
            'description': 'Test Description',
        }

    def _get_base_url(self):
        return 'plugins:netbox_routing:communitylist_{}'


class CommunityListEntryTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    # ViewTestCases.BulkImportObjectsViewTestCase,
    model = CommunityListEntry

    @classmethod
    def setUpTestData(cls):
        cls.tenant = Tenant.objects.create(name='Tenant 1')
        cls.role = Role.objects.create(name='Role 1')

        cls.communities = (
            Community(
                community='64512',
                status='active',
            ),
            Community(
                community='64513',
                status='active',
                role=cls.role,
            ),
            Community(
                community='64514',
                status='active',
                role=cls.role,
                tenant=cls.tenant,
            ),
        )

        Community.objects.bulk_create(cls.communities)

        cls.community_lists = (
            CommunityList(
                name='Community List 1',
            ),
            CommunityList(
                name='Community List 2',
            ),
            CommunityList(
                name='Community List 3',
                tenant=cls.tenant,
            ),
        )

        CommunityList.objects.bulk_create(cls.community_lists)

        cls.community_list_entries = (
            CommunityListEntry(
                community_list=cls.community_lists[0],
                community=cls.communities[0],
                action=ActionChoices.PERMIT,
            ),
            CommunityListEntry(
                community_list=cls.community_lists[0],
                community=cls.communities[0],
                action=ActionChoices.PERMIT,
            ),
            CommunityListEntry(
                community_list=cls.community_lists[1],
                community=cls.communities[0],
                action=ActionChoices.PERMIT,
            ),
            CommunityListEntry(
                community_list=cls.community_lists[1],
                community=cls.communities[1],
                action=ActionChoices.PERMIT,
            ),
        )

        CommunityListEntry.objects.bulk_create(cls.community_list_entries)

        cls.form_data = {
            'community_list': cls.community_lists[2].pk,
            'community': cls.communities[2].pk,
            'action': ActionChoices.PERMIT,
        }

        cls.bulk_edit_data = {
            'description': 'Test Description',
        }

    def _get_base_url(self):
        return 'plugins:netbox_routing:communitylistentry_{}'
