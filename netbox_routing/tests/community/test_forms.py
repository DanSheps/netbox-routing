from django.test import TestCase

from tenancy.models import Tenant

from netbox_routing.choices import ActionChoices
from netbox_routing.forms.community import *

__all__ = ('CommunityTestCase', 'CommunityListTestCase', 'CommunityListEntryTestCase')


class CommunityTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.tenant = Tenant.objects.create(name='Tenant 1')
        cls.role = Role.objects.create(name='Role 1')

    def test_community(self):
        form = CommunityForm(
            data={
                'community': '64512',
                'role': self.role,
                'status': 'active',
                'tenant': self.tenant,
                'description': 'Description',
                'comment': 'Comment',
            }
        )
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_community_minimal(self):
        form = CommunityForm(
            data={
                'community': '64512',
                'status': 'active',
            }
        )
        self.assertTrue(form.is_valid())
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

    def test_community_list(self):
        form = CommunityListForm(
            data={
                'name': 'Community List 1',
                'tenant': self.tenant,
                'description': 'Description',
                'comment': 'Comment',
            }
        )
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_form_invalid(self):
        form = CommunityListForm(
            data={
                'tenant': self.tenant,
            }
        )
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValueError):
            form.save()
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

    def test_community_list_entry(self):
        form = CommunityListEntryForm(
            data={
                'community_list': self.community_list.pk,
                'community': self.community.pk,
                'action': ActionChoices.PERMIT,
                'description': 'Description',
                'comment': 'Comment',
            }
        )
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

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
