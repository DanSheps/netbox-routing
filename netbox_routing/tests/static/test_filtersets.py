import netaddr
from django.test import TestCase

from ipam.models import VRF
from utilities.testing import create_test_device

from netbox_routing.filtersets import *
from netbox_routing.models import *

__all__ = (
    'StaticRouteTestCase',
)


class StaticRouteTestCase(TestCase):
    queryset = StaticRoute.objects.all()
    filterset = StaticRouteFilterSet

    @classmethod
    def setUpTestData(cls):
        devices = [create_test_device(name='Device 1'), create_test_device(name='Device 2')]
        vrf = VRF.objects.create(name='Test VRF')

        nh = netaddr.IPAddress('10.10.10.1')

        routes = (
            StaticRoute(name="Route 1", vrf=vrf, prefix='0.0.0.0/0', next_hop=nh),
            StaticRoute(name="Route 2", vrf=vrf, prefix='1.1.1.0/24', next_hop=netaddr.IPAddress('10.10.10.2')),
            StaticRoute(name="Route 3", prefix='0.0.0.0/0', next_hop=nh, metric=100)
        )

        StaticRoute.objects.bulk_create(routes)

        routes[0].devices.set([devices[0]])
        routes[1].devices.set([devices[0]])
        routes[2].devices.set([devices[1]])

    def test_q(self):
        params = {'q': 'Route 1'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_name(self):
        params = {'name': ['Route 1', 'Route 2']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_device(self):
        params = {'device': ['Device 1']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_vrf(self):
        params = {'vrf': ['Test VRF']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_prefix(self):
        params = {'prefix': '0.0.0.0/0'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_next_hop(self):
        params = {'next_hop': '10.10.10.1'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_metric(self):
        params = {'metric': [1]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
