# from django.core.exceptions import ValidationError
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

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

    @classmethod
    def setUpTestData(cls):
        pass

    def test_community(self):
        name = 'AS Path 1'
        asp = ASPath(
            name=name,
        )
        asp.full_clean()
        asp.save()
        self.assertIsInstance(asp, ASPath)
        self.assertEqual(asp.__str__(), name)

    def test_unique_together(self):

        name = 'AS Path 1'
        asp = ASPath(
            name=name,
        )
        asp.full_clean()
        asp.save()

        asp = ASPath(
            name=name,
        )

        with self.assertRaises(ValidationError):
            asp.full_clean()
        with self.assertRaises(IntegrityError):
            asp.save()


class ASPathEntryTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.aspath = ASPath(
            name='AS Path',
        )
        cls.aspath.full_clean()
        cls.aspath.save()

    def test_aspath_entry(self):
        for seq, pattern in (
            (1, '^1$'),
            (2, '^2$'),
            (3, '^3$'),
            (4, '^4$'),
        ):
            aspe = ASPathEntry(
                aspath=self.aspath,
                action='permit',
                sequence=seq,
                pattern=pattern,
            )
            aspe.full_clean()
            aspe.save()
            self.assertIsInstance(aspe, ASPathEntry)
            self.assertEqual(aspe.__str__(), f'{self.aspath} permit {seq}')


class PrefixListTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def test_community(self):
        name = 'Prefix List 1'
        pl = PrefixList(
            name=name,
        )
        pl.full_clean()
        pl.save()
        self.assertIsInstance(pl, PrefixList)
        self.assertEqual(pl.__str__(), name)

    def test_unique_together(self):

        name = 'Prefix List 1'
        pl = PrefixList(
            name=name,
        )
        pl.full_clean()
        pl.save()

        pl = PrefixList(
            name=name,
        )

        with self.assertRaises(ValidationError):
            pl.full_clean()
        with self.assertRaises(IntegrityError):
            pl.save()


class PrefixListEntryTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.prefix_list = PrefixList(
            name='Prefix List',
        )
        cls.prefix_list.full_clean()
        cls.prefix_list.save()

    def test_prefix_list_entry(self):
        for seq, pattern in (
            (1, '10.0.1.0/24'),
            (2, '10.0.2.0/24'),
            (3, '10.0.3.0/24'),
            (4, '10.0.4.0/24'),
        ):
            ple = PrefixListEntry(
                prefix_list=self.prefix_list,
                action='permit',
                sequence=seq,
                prefix=pattern,
            )
            ple.full_clean()
            ple.save()
            self.assertIsInstance(ple, PrefixListEntry)
            self.assertEqual(ple.__str__(), f'{self.prefix_list} permit {seq}')


class RouteMapTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def test_community(self):
        name = 'Route Map 1'
        rm = RouteMap(
            name=name,
        )
        rm.full_clean()
        rm.save()
        self.assertIsInstance(rm, RouteMap)
        self.assertEqual(rm.__str__(), name)

    def test_unique_together(self):

        name = 'Route Map 1'
        rm = RouteMap(
            name=name,
        )
        rm.full_clean()
        rm.save()

        rm = RouteMap(
            name=name,
        )

        with self.assertRaises(ValidationError):
            rm.full_clean()
        with self.assertRaises(IntegrityError):
            rm.save()


class RouteMapEntryTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.route_map = RouteMap(
            name='Route Map',
        )
        cls.route_map.full_clean()
        cls.route_map.save()

    def test_route_map_entry(self):
        for seq, pattern in (
            (1, '10.0.1.0/24'),
            (2, '10.0.2.0/24'),
            (3, '10.0.3.0/24'),
            (4, '10.0.4.0/24'),
        ):
            rme = RouteMapEntry(
                route_map=self.route_map,
                action='permit',
                sequence=seq,
                match={'tags': f'{seq}{seq}{seq}{seq}'},
            )
            rme.full_clean()
            rme.save()
            self.assertIsInstance(rme, RouteMapEntry)
            self.assertEqual(rme.__str__(), f'{self.route_map} permit {seq}')
