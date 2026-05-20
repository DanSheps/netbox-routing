from django.test import TestCase

from ipam.models import Prefix
from netbox_routing.choices import ActionChoices

from netbox_routing.filtersets.objects import *
from netbox_routing.models.objects import *

__all__ = (
    'ASPathTestCase',
    'ASPathEntryTestCase',
    'PrefixListTestCase',
    'PrefixListEntryTestCase',
    'RouteMapTestCase',
    'RouteMapEntryTestCase',
)


class ASPathTestCase(TestCase):
    queryset = ASPath.objects.all()
    filterset = ASPathFilterSet

    @classmethod
    def setUpTestData(cls):

        cls.aspath = [
            ASPath(
                name='AS Path List 1-1',
            ),
            ASPath(
                name='AS Path List 1-2',
            ),
            ASPath(
                name='AS Path List 2-1',
            ),
            ASPath(
                name='AS Path List 2-2',
            ),
        ]
        ASPath.objects.bulk_create(cls.aspath)

    def test_q(self):
        params = {'q': 'AS Path List 1-'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)


class ASPathEntryTestCase(TestCase):
    queryset = ASPathEntry.objects.all()
    filterset = ASPathEntryFilterSet

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

        cls.aspath_entry = [
            ASPathEntry(
                aspath=cls.aspath[0],
                action=ActionChoices.PERMIT,
                sequence=1,
                pattern='^1234$',
            ),
            ASPathEntry(
                aspath=cls.aspath[0],
                action=ActionChoices.PERMIT,
                sequence=2,
                pattern='^5678$',
            ),
            ASPathEntry(
                aspath=cls.aspath[1],
                action=ActionChoices.PERMIT,
                sequence=1,
                pattern='^1234$',
            ),
            ASPathEntry(
                aspath=cls.aspath[1],
                action=ActionChoices.PERMIT,
                sequence=2,
                pattern='^5678',
            ),
        ]
        ASPathEntry.objects.bulk_create(cls.aspath_entry)

    def test_q(self):
        params = {'q': '1234'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_aspath(self):
        params = {
            'aspath_id': [
                self.aspath[1].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

        params = {
            'aspath': [
                self.aspath[1].name,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)


class PrefixListTestCase(TestCase):
    queryset = PrefixList.objects.all()
    filterset = PrefixListFilterSet

    @classmethod
    def setUpTestData(cls):

        cls.prefix_list = [
            PrefixList(
                name='Prefix List 1-1',
            ),
            PrefixList(
                name='Prefix List 1-2',
            ),
            PrefixList(
                name='Prefix List 2-1',
            ),
            PrefixList(
                name='Prefix List 2-2',
            ),
        ]
        PrefixList.objects.bulk_create(cls.prefix_list)

    def test_q(self):
        params = {'q': 'Prefix List 1-'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)


class PrefixListEntryTestCase(TestCase):
    queryset = PrefixListEntry.objects.all()
    filterset = PrefixListEntryFilterSet

    @classmethod
    def setUpTestData(cls):
        cls.prefix_list = (
            PrefixList(
                name='Prefix List 1',
            ),
            PrefixList(
                name='Prefix List 2',
            ),
        )
        PrefixList.objects.bulk_create(cls.prefix_list)

        cls.prefixes = (Prefix(prefix='10.0.0.0/24'),)
        Prefix.objects.bulk_create(cls.prefixes)

        cls.custom_prefixes = (CustomPrefix(prefix='10.0.1.0/24'),)
        CustomPrefix.objects.bulk_create(cls.custom_prefixes)

        cls.prefix_list_entry = [
            PrefixListEntry(
                prefix_list=cls.prefix_list[0],
                action=ActionChoices.PERMIT,
                sequence=1,
                assigned_prefix=cls.prefixes[0],
            ),
            PrefixListEntry(
                prefix_list=cls.prefix_list[0],
                action=ActionChoices.PERMIT,
                sequence=2,
                assigned_prefix=cls.custom_prefixes[0],
            ),
            PrefixListEntry(
                prefix_list=cls.prefix_list[1],
                action=ActionChoices.PERMIT,
                sequence=1,
                assigned_prefix=cls.prefixes[0],
            ),
            PrefixListEntry(
                prefix_list=cls.prefix_list[1],
                action=ActionChoices.PERMIT,
                sequence=2,
                assigned_prefix=cls.custom_prefixes[0],
            ),
        ]
        PrefixListEntry.objects.bulk_create(cls.prefix_list_entry)

    def test_q(self):
        params = {'q': 'Prefix List 1'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_prefix_list(self):
        params = {
            'prefix_list_id': [
                self.prefix_list[1].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

        params = {
            'prefix_list': [
                self.prefix_list[1].name,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_prefix(self):
        params = {
            'prefix_id': [
                self.prefixes[0].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

        params = {
            'prefix': [
                self.prefixes[0].prefix,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_custom_prefix(self):
        params = {
            'custom_prefix_id': [
                self.custom_prefixes[0].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

        params = {
            'custom_prefix': [
                self.custom_prefixes[0].prefix,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)


class RouteMapTestCase(TestCase):
    queryset = RouteMap.objects.all()
    filterset = RouteMapFilterSet

    @classmethod
    def setUpTestData(cls):

        cls.prefix_list = [
            RouteMap(
                name='Route Map 1-1',
            ),
            RouteMap(
                name='Route Map 1-2',
            ),
            RouteMap(
                name='Route Map 2-1',
            ),
            RouteMap(
                name='Route Map 2-2',
            ),
        ]
        RouteMap.objects.bulk_create(cls.prefix_list)

    def test_q(self):
        params = {'q': 'Route Map 1-'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)


class RouteMapEntryTestCase(TestCase):
    queryset = RouteMapEntry.objects.all()
    filterset = RouteMapEntryFilterSet

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

        cls.route_map_entry = [
            RouteMapEntry(
                route_map=cls.route_map[0],
                action=ActionChoices.PERMIT,
                sequence=1,
                match={'tag': 1234},
            ),
            RouteMapEntry(
                route_map=cls.route_map[0],
                action=ActionChoices.PERMIT,
                sequence=2,
                match={'tag': 5678},
            ),
            RouteMapEntry(
                route_map=cls.route_map[1],
                action=ActionChoices.PERMIT,
                sequence=1,
                match={'tag': 9012},
            ),
            RouteMapEntry(
                route_map=cls.route_map[1],
                action=ActionChoices.PERMIT,
                sequence=2,
                match={'tag': 3456},
            ),
        ]
        RouteMapEntry.objects.bulk_create(cls.route_map_entry)

    def test_q(self):
        params = {'q': 'Route Map 1'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_match(self):
        params = {'q': '34'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_prefix_list(self):
        params = {
            'route_map_id': [
                self.route_map[1].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

        params = {
            'route_map': [
                self.route_map[1].name,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
