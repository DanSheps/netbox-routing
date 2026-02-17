from django.test import TestCase

from ipam.models import Prefix
from netbox_routing.models.objects import *

from netbox_routing.choices import ActionChoices
from netbox_routing.forms.objects import *

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

    def test_object(self):
        form = ASPathForm(
            data={
                'name': 'AS Path List 1',
                'description': 'Description',
                'comment': 'Comment',
            }
        )
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_minimal_object(self):
        form = ASPathForm(
            data={
                'name': 'AS Path List 1',
            }
        )
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_form_invalid(self):
        form = ASPathForm(
            data={
                'name': 'AS Path List 1 Too Long Name Needs to be over 100 characters long and enough characters to cau'
                'se an error with the form validation',
            }
        )
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValueError):
            form.save()


class ASPathEntryTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.aspath = ASPath.objects.create(
            name='AS Path List 1',
        )

    def test_object(self):
        form = ASPathEntryForm(
            data={
                'aspath': self.aspath,
                'sequence': 1,
                'action': ActionChoices.PERMIT,
                'pattern': '^2242$',
            }
        )
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_form_invalid(self):
        form = ASPathEntryForm(data={'aspath': self.aspath, 'pattern': '^2242$'})
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValueError):
            form.save()


class PrefixListTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def test_object(self):
        form = PrefixListForm(
            data={
                'name': 'Prefix List 1',
                'family': 4,
                'description': 'Description',
                'comment': 'Comment',
            }
        )
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_minimal_object(self):
        form = PrefixListForm(
            data={
                'name': 'Prefix List 1',
                'family': 6,
            }
        )
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_form_invalid(self):
        form = PrefixListForm(
            data={
                'name': 'Prefix List 1',
            }
        )
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValueError):
            form.save()


class PrefixListEntryTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.prefix_list = PrefixList.objects.create(
            name='Prefix List 1',
            family=4,
        )
        cls.prefix = Prefix(prefix='10.0.0.0/8')
        cls.prefix.full_clean()
        cls.prefix.save()

        cls.custom_prefix = CustomPrefix(prefix='192.168.0.0/16')
        cls.custom_prefix.full_clean()
        cls.custom_prefix.save()

    def test_prefix(self):
        form = PrefixListEntryForm(
            data={
                'prefix_list': self.prefix_list,
                'sequence': 1,
                'action': ActionChoices.PERMIT,
                'ipam_prefix': self.prefix.pk,
            }
        )
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_custom_prefix(self):
        form = PrefixListEntryForm(
            data={
                'prefix_list': self.prefix_list,
                'sequence': 1,
                'action': ActionChoices.PERMIT,
                'custom_prefix': self.custom_prefix.pk,
            }
        )
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_form_invalid(self):
        form = PrefixListEntryForm(
            data={
                'prefix_list': self.prefix_list,
                'prefix': self.prefix.pk,
                'custom_prefix': self.custom_prefix.pk,
            }
        )
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValueError):
            form.save()


class RouteMapTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def test_object(self):
        form = RouteMapForm(
            data={
                'name': 'Route Map 1',
                'description': 'Description',
                'comment': 'Comment',
            }
        )
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_minimal_object(self):
        form = RouteMapForm(
            data={
                'name': 'Route Map 1',
            }
        )
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_form_invalid(self):
        form = RouteMapForm(
            data={
                'name': 'Route Map 1 Too Long Name Needs to be over 100 characters long and enough characters to cau'
                'se an error with the form validation',
            }
        )
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValueError):
            form.save()


class RouteMapEntryTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.route_map = RouteMap.objects.create(
            name='Route Map 1',
        )
        cls.community = Community.objects.create(community='64512', status='active')

    def test_object(self):
        form = RouteMapEntryForm(
            data={
                'route_map': self.route_map,
                'sequence': 1,
                'action': ActionChoices.PERMIT,
                'match_community': self.community,
                'match': {},
            }
        )
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())
        self.assertEqual(form.instance.match.get('community'), self.community.pk)

    def test_form_invalid(self):
        form = RouteMapEntryForm(
            data={
                'route_map': self.route_map,
            }
        )
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValueError):
            form.save()
