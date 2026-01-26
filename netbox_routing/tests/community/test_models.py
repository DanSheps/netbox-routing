# from django.core.exceptions import ValidationError
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from ipam.models import Role

# from utilities.testing import create_test_device

from netbox_routing.models.community import *

__all__ = (
    'CommunityTestCase',
    'CommunityListTestCase',
    'CommunityListEntryTestCase',
)


class CommunityTestCase(TestCase):
    def setUp(self):
        Role.objects.create(name='Test Role')

    def test_community(self):
        role = Role.objects.get(name='Test Role')
        community_value = '64512'
        community = Community(
            community=community_value,
            status='active',
            role=role,
        )
        community.full_clean()
        community.save()
        self.assertIsInstance(community, Community)
        self.assertEqual(community.__str__(), community_value)

        community_value = '64512:64512'
        community = Community(
            community=community_value,
            status='active',
            role=role,
        )
        community.full_clean()
        community.save()
        self.assertIsInstance(community, Community)
        self.assertEqual(community.__str__(), community_value)

        community_value = '64512:64512:64512'
        community = Community(
            community=community_value,
            status='active',
            role=role,
        )
        community.full_clean()
        community.save()
        self.assertIsInstance(community, Community)
        self.assertEqual(community.__str__(), community_value)

        community_value = '64512:64512:64512:64512'
        community = Community(
            community=community_value,
            status='active',
            role=role,
        )

        with self.assertRaises(ValidationError):
            community.full_clean()
            community.save()

    def test_unique_together(self):

        role = Role.objects.get(name='Test Role')
        community_value = '64512:64512:64512'
        community = Community(
            community=community_value,
            status='active',
            role=role,
        )
        community.full_clean()
        community.save()

        community = Community(
            community=community_value,
            status='active',
            role=role,
        )

        with self.assertRaises(ValidationError):
            community.full_clean()
        with self.assertRaises(IntegrityError):
            community.save()


class CommunityListTestCase(TestCase):
    def setUp(self):
        pass

    def test_community_list(self):
        cl = CommunityList(
            name='Test Community List',
        )
        cl.full_clean()
        cl.save()

    def test_community_list_unique(self):
        cl = CommunityList(
            name='Test Community List',
        )
        cl.full_clean()
        cl.save()

        cl = CommunityList(
            name='Test Community List',
        )
        with self.assertRaises(ValidationError):
            cl.full_clean()
        with self.assertRaises(IntegrityError):
            cl.save()


class CommunityListEntryTestCase(TestCase):
    def setUp(self):
        role = Role.objects.create(name='Test Role')
        self.communities = (
            Community(
                community='64512',
                status='active',
                role=role,
            ),
            Community(
                community='64513',
                status='active',
                role=role,
            ),
            Community(
                community='64514',
                status='active',
                role=role,
            ),
            Community(
                community='64515',
                status='active',
                role=role,
            ),
            Community(
                community='64516',
                status='active',
                role=role,
            ),
        )
        Community.objects.bulk_create(self.communities)

        self.cl = CommunityList(
            name='Test Community List',
        )
        self.cl.full_clean()
        self.cl.save()

    def test_community_list_entry(self):
        for community in self.communities:
            cle = CommunityListEntry(community_list=self.cl, community=community)
            cle.full_clean()
            cle.save()
