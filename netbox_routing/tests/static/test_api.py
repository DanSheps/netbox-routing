from netaddr.ip import IPAddress
from django.urls import reverse
from rest_framework import status

from ipam.models import VRF
from utilities.testing import APIViewTestCases, create_test_device

from netbox_routing.models import StaticRoute
from netbox_routing.tests.base import IPAddressFieldMixin

__all__ = ('StaticRouteTestCase',)


class StaticRouteTestCase(IPAddressFieldMixin, APIViewTestCases.APIViewTestCase):
    model = StaticRoute
    view_namespace = "plugins-api:netbox_routing"
    brief_fields = [
        'description',
        'display',
        'id',
        'name',
        'next_hop',
        'prefix',
        'url',
    ]

    bulk_update_data = {'metric': 5}

    def test_paginated_list_returns_each_tied_route_once(self):
        """Reproduce the paged list dropping and repeating rows (issue #206).

        StaticRoute orders by (vrf, prefix, metric). These rows share all three and
        differ only by next_hop, so the ordering is not total unless it ends in a
        unique field.

        The REST API pages with LIMIT and OFFSET, and PostgreSQL picks a different
        plan as the offset grows: an incremental sort for the first page, then a full
        sort over a sequential scan for later ones. The two plans order tied rows
        differently, so a row that appeared on an early page appears again later while
        another is never returned.

        Do not filter the list here. A filter changes the row estimates, the planner
        then uses one plan for every offset, and the defect no longer shows.
        """
        self.add_permissions('netbox_routing.view_staticroute')
        vrf = VRF.objects.create(name='Pagination Test VRF')
        StaticRoute.objects.bulk_create(
            [
                StaticRoute(
                    vrf=vrf,
                    prefix='198.18.0.0/24',
                    next_hop=IPAddress(f'198.18.{index // 250}.{index % 250}'),
                    metric=10,
                )
                for index in range(1, 1501)
            ]
        )
        # page the plain list endpoint, as the report does, so every route in the
        # table takes part, not just this VRF's
        expected_ids = set(StaticRoute.objects.values_list('pk', flat=True))
        collected_ids = []
        visited_urls = set()
        url = reverse('plugins-api:netbox_routing-api:staticroute-list')
        url = f'{url}?limit=50'

        while url:
            self.assertNotIn(url, visited_urls)
            visited_urls.add(url)
            response = self.client.get(url, **self.header)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            collected_ids.extend(result['id'] for result in response.data['results'])
            url = response.data['next']

        duplicates = len(collected_ids) - len(set(collected_ids))
        missing = expected_ids - set(collected_ids)
        self.assertEqual(
            (duplicates, missing),
            (0, set()),
            f'paged collection returned {duplicates} duplicate row(s) and missed '
            f'{len(missing)} row(s) out of {len(expected_ids)}',
        )

    @classmethod
    def setUpTestData(cls):
        device = create_test_device(name='Test Device')
        vrf = VRF.objects.create(name='Test VRF')

        nh = IPAddress('10.10.10.1')

        routes = (
            StaticRoute(name='Test Route 1', vrf=vrf, prefix='0.0.0.0/0', next_hop=nh),
            StaticRoute(
                name='Test Route 2', vrf=None, prefix='1.1.1.1/32', next_hop=nh
            ),
            StaticRoute(name='Test Route 3', vrf=vrf, prefix='2.2.2.2/32', next_hop=nh),
        )
        StaticRoute.objects.bulk_create(routes)

        routes[0].devices.set([device])
        routes[1].devices.set([device])
        routes[2].devices.set([device])

        cls.create_data = [
            {
                'name': 'Default Route',
                'devices': [device.pk],
                'vrf': vrf.pk,
                'prefix': '0.0.0.0/0',
                'next_hop': '10.10.10.2',
                'metric': 1,
                'permanent': True,
            },
            {
                'name': 'Google DNS',
                'devices': [device.pk],
                'vrf': None,
                'prefix': '4.4.4.4/32',
                'next_hop': '10.10.10.1',
                'metric': 1,
                'permanent': True,
            },
            {
                'name': 'One dot one dot one dot one',
                'devices': [device.pk],
                'vrf': None,
                'prefix': '1.1.1.0/24',
                'next_hop': '10.10.10.1',
                'metric': 1,
                'permanent': True,
            },
        ]
