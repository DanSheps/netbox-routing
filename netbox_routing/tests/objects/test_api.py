from ipam.models import Prefix
from utilities.testing import APIViewTestCases

from netbox_routing.models.objects import *

__all__ = (
    'ASPathTestCase',
    'ASPathEntryTestCase',
    'PrefixListTestCase',
    'PrefixListEntryTestCase',
    'RouteMapTestCase',
    'RouteMapEntryTestCase',
)


class ASPathTestCase(APIViewTestCases.APIViewTestCase):
    model = ASPath
    view_namespace = "plugins-api:netbox_routing"
    graphql_base_name = 'aspath'
    brief_fields = [
        'display',
        'id',
        'name',
        'url',
    ]

    bulk_update_data = {'description': 'Description'}

    @classmethod
    def setUpTestData(cls):
        cls.aspath = (
            cls.model(
                name='AS Path List 1',
            ),
            cls.model(
                name='AS Path List 2',
            ),
            cls.model(
                name='AS Path List 3',
            ),
        )
        cls.model.objects.bulk_create(cls.aspath)

        cls.create_data = [
            {
                'name': 'AS Path List 4',
            },
            {
                'name': 'AS Path List 5',
            },
        ]


class ASPathEntryTestCase(APIViewTestCases.APIViewTestCase):
    model = ASPathEntry
    view_namespace = "plugins-api:netbox_routing"
    graphql_base_name = 'aspath_entry'
    brief_fields = [
        'action',
        'aspath',
        'display',
        'id',
        'pattern',
        'sequence',
        'url',
    ]

    bulk_update_data = {'description': 'Description'}

    @classmethod
    def setUpTestData(cls):
        cls.aspath = (
            ASPath(
                name='AS Path List 1',
            ),
            ASPath(
                name='AS Path List 2',
            ),
        )
        ASPath.objects.bulk_create(cls.aspath)

        cls.aspath_entry = (
            cls.model(
                aspath=cls.aspath[0], action='permit', sequence=1, pattern='^2448$'
            ),
            cls.model(
                aspath=cls.aspath[0], action='permit', sequence=2, pattern='^2448 2447$'
            ),
            cls.model(
                aspath=cls.aspath[1], action='permit', sequence=1, pattern='^.*$'
            ),
        )
        cls.model.objects.bulk_create(cls.aspath_entry)

        cls.create_data = [
            {
                'aspath': cls.aspath[0].pk,
                'action': 'permit',
                'sequence': 3,
                'pattern': '^2448 2448 2448$',
            },
            {
                'aspath': cls.aspath[0].pk,
                'action': 'permit',
                'sequence': 4,
                'pattern': '^2448 2448 2448 2448$',
            },
        ]


class PrefixListTestCase(APIViewTestCases.APIViewTestCase):
    model = PrefixList
    view_namespace = "plugins-api:netbox_routing"
    graphql_base_name = 'prefixlist'
    brief_fields = [
        'display',
        'id',
        'name',
        'url',
    ]

    bulk_update_data = {'description': 'Description'}

    @classmethod
    def setUpTestData(cls):
        cls.prefix_list = (
            cls.model(
                name='Prefix List 1',
            ),
            cls.model(
                name='Prefix List 2',
            ),
            cls.model(
                name='Prefix List 3',
            ),
        )
        cls.model.objects.bulk_create(cls.prefix_list)

        cls.create_data = [
            {
                'name': 'Prefix List 4',
            },
            {
                'name': 'Prefix List 5',
            },
        ]


class PrefixListEntryTestCase(APIViewTestCases.APIViewTestCase):
    model = PrefixListEntry
    view_namespace = "plugins-api:netbox_routing"
    graphql_base_name = 'prefixlist_entry'
    brief_fields = [
        'action',
        'assigned_prefix_id',
        'assigned_prefix_type',
        'display',
        'ge',
        'id',
        'le',
        'prefix_list',
        'sequence',
        'url',
    ]

    bulk_update_data = {'description': 'Description'}

    @classmethod
    def setUpTestData(cls):
        prefixes = (
            Prefix(prefix='10.0.0.0/24'),
            Prefix(prefix='10.0.1.0/24'),
            Prefix(prefix='10.0.2.0/24'),
            Prefix(prefix='10.0.3.0/24'),
        )
        Prefix.objects.bulk_create(prefixes)

        custom_prefixes = (
            CustomPrefix(prefix='10.0.0.0/24'),
            CustomPrefix(prefix='10.0.4.0/24'),
        )
        CustomPrefix.objects.bulk_create(custom_prefixes)

        cls.prefix_list = (
            PrefixList(
                name='Prefix List 1',
            ),
            PrefixList(
                name='Prefix List 2',
            ),
        )
        PrefixList.objects.bulk_create(cls.prefix_list)

        cls.prefix_list_entry = (
            cls.model(
                prefix_list=cls.prefix_list[0],
                action='permit',
                sequence=1,
                assigned_prefix=prefixes[0],
            ),
            cls.model(
                prefix_list=cls.prefix_list[0],
                action='permit',
                sequence=2,
                assigned_prefix=prefixes[1],
            ),
            cls.model(
                prefix_list=cls.prefix_list[1],
                action='permit',
                sequence=1,
                assigned_prefix=custom_prefixes[0],
            ),
        )
        cls.model.objects.bulk_create(cls.prefix_list_entry)

        cls.create_data = [
            {
                'prefix_list': cls.prefix_list[0].pk,
                'action': 'permit',
                'sequence': 3,
                'assigned_prefix_type': 'ipam.prefix',
                'assigned_prefix_id': prefixes[0].pk,
            },
            {
                'prefix_list': cls.prefix_list[0].pk,
                'action': 'permit',
                'sequence': 4,
                'assigned_prefix_type': 'netbox_routing.customprefix',
                'assigned_prefix_id': custom_prefixes[1].pk,
            },
        ]


class RouteMapTestCase(APIViewTestCases.APIViewTestCase):
    model = RouteMap
    view_namespace = "plugins-api:netbox_routing"
    brief_fields = [
        'display',
        'id',
        'name',
        'url',
    ]

    bulk_update_data = {'description': 'Description'}

    @classmethod
    def setUpTestData(cls):
        cls.route_map = (
            cls.model(
                name='Route Map 1',
            ),
            cls.model(
                name='Route Map 2',
            ),
            cls.model(
                name='Route Map 3',
            ),
        )
        cls.model.objects.bulk_create(cls.route_map)

        cls.create_data = [
            {
                'name': 'Route Map 4',
            },
            {
                'name': 'Route Map 5',
            },
        ]


class RouteMapEntryTestCase(APIViewTestCases.APIViewTestCase):
    model = RouteMapEntry
    view_namespace = "plugins-api:netbox_routing"
    brief_fields = [
        'action',
        'display',
        'id',
        'route_map',
        'sequence',
        'url',
    ]

    bulk_update_data = {'description': 'Description'}

    @classmethod
    def setUpTestData(cls):
        cls.route_map = (
            RouteMap(
                name='Route Map 1',
            ),
            RouteMap(
                name='Route Map 2',
            ),
        )
        RouteMap.objects.bulk_create(cls.route_map)

        cls.route_map_entry = (
            cls.model(
                route_map=cls.route_map[0],
                action='permit',
                sequence=1,
                match={'tags': 1},
                set={},
            ),
            cls.model(
                route_map=cls.route_map[0],
                action='permit',
                sequence=2,
                match={'tags': 2},
                set={},
            ),
            cls.model(
                route_map=cls.route_map[1],
                action='permit',
                sequence=1,
                match={'tags': 3},
                set={},
            ),
        )
        cls.model.objects.bulk_create(cls.route_map_entry)

        cls.create_data = [
            {
                'route_map': cls.route_map[0].pk,
                'action': 'permit',
                'sequence': 3,
                'match': {'tags': 4},
            },
            {
                'route_map': cls.route_map[0].pk,
                'action': 'permit',
                'sequence': 4,
                'match': {'tags': 5},
            },
        ]
