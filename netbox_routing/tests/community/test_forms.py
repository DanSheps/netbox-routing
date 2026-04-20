from django.test import TestCase

from ipam.models import Role
from tenancy.models import Tenant

from netbox_routing.choices import ActionChoices
from netbox_routing.forms.community import *

__all__ = ('CommunityTestCase', 'CommunityListTestCase', 'CommunityListEntryTestCase')


class CommunityTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.tenant = Tenant.objects.create(name='Tenant 1')
        cls.role = Role.objects.create(name='Role 1')

    def test_community_with_description_and_comments(self):
        form = CommunityForm(
            data={
                'community': '64512',
                'role': self.role.pk,
                'status': 'active',
                'tenant': self.tenant.pk,
                'description': 'Blackhole community',
                'comments': 'Used for DDoS mitigation',
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        instance = form.save()
        instance.refresh_from_db()
        self.assertEqual(instance.description, 'Blackhole community')
        self.assertEqual(instance.comments, 'Used for DDoS mitigation')

    def test_community_minimal(self):
        form = CommunityForm(
            data={
                'community': '64512',
                'status': 'active',
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        self.assertTrue(form.save())

    def test_form_invalid_community(self):
        form = CommunityForm(
            data={
                'community': 'g443gf',
                'status': 'active',
            }
        )
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValueError):
            form.save()

    def test_form_invalid_status(self):
        form = CommunityForm(
            data={
                'community': '64512:21333',
                'status': 'private',
            }
        )
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValueError):
            form.save()


class CommunityListTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.tenant = Tenant.objects.create(name='Tenant 1')

    def test_community_list_with_description_and_comments(self):
        form = CommunityListForm(
            data={
                'name': 'Community List 1',
                'tenant': self.tenant.pk,
                'description': 'Customer communities',
                'comments': 'Managed by NOC team',
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        instance = form.save()
        instance.refresh_from_db()
        self.assertEqual(instance.description, 'Customer communities')
        self.assertEqual(instance.comments, 'Managed by NOC team')

    def test_form_invalid(self):
        form = CommunityListForm(
            data={
                'tenant': self.tenant.pk,
            }
        )
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValueError):
            form.save()


class CommunityListEntryTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.tenant = Tenant.objects.create(name='Tenant 1')
        cls.role = Role.objects.create(name='Role 1')
        cls.community = Community.objects.create(
            community='64512',
            status='active',
            role=cls.role,
            tenant=cls.tenant,
        )
        cls.community_list = CommunityList.objects.create(
            name='Community List 1',
            tenant=cls.tenant,
        )

    def test_community_list_entry_with_description_and_comments(self):
        form = CommunityListEntryForm(
            data={
                'community_list': self.community_list.pk,
                'community': self.community.pk,
                'action': ActionChoices.PERMIT,
                'description': 'Allow blackhole',
                'comments': 'Required for DDoS policy',
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        instance = form.save()
        instance.refresh_from_db()
        self.assertEqual(instance.description, 'Allow blackhole')
        self.assertEqual(instance.comments, 'Required for DDoS policy')

    def test_form_invalid(self):
        form = CommunityListEntryForm(
            data={
                'community': self.community.pk,
            }
        )
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValueError):
            form.save()

        form = CommunityListEntryForm(
            data={
                'community_list': self.community_list.pk,
            }
        )
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValueError):
            form.save()
