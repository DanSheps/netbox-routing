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
    ViewTestCases.BulkImportObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
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
            'description': 'Test community description',
            'comments': 'Test community comments',
        }

        cls.csv_data = (
            'community,status',
            '65000:100,active',
            '65000:200,active',
            '65000:300,reserved',
        )

        cls.csv_update_data = (
            'id,description',
            f'{cls.communities[0].pk},Updated description 1',
            f'{cls.communities[1].pk},Updated description 2',
            f'{cls.communities[2].pk},Updated description 3',
        )

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
    ViewTestCases.BulkImportObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
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
            'description': 'Test community list description',
            'comments': 'Test community list comments',
        }

        cls.csv_data = (
            'name',
            'Import List 1',
            'Import List 2',
            'Import List 3',
        )

        cls.csv_update_data = (
            'id,description',
            f'{cls.community_list[0].pk},Updated description 1',
            f'{cls.community_list[1].pk},Updated description 2',
            f'{cls.community_list[2].pk},Updated description 3',
        )

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
    ViewTestCases.BulkImportObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
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
            'description': 'Test entry description',
            'comments': 'Test entry comments',
        }

        cls.csv_data = (
            'community_list,community,action',
            'Community List 3,64512,permit',
            'Community List 3,64513,deny',
            'Community List 3,64514,permit',
        )

        cls.csv_update_data = (
            'id,description',
            f'{cls.community_list_entries[0].pk},Updated description 1',
            f'{cls.community_list_entries[1].pk},Updated description 2',
            f'{cls.community_list_entries[2].pk},Updated description 3',
        )

        cls.bulk_edit_data = {
            'description': 'Test Description',
        }

    def _get_base_url(self):
        return 'plugins:netbox_routing:communitylistentry_{}'
