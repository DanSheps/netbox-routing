from netaddr.ip import IPAddress
from ipam.models import VRF
from utilities.testing import APIViewTestCases, create_test_device

from netbox_routing.models import StaticRoute
from netbox_routing.tests.base import IPAddressFieldMixin

__all__ = (
    'StaticRouteTestCase',
)

class StaticRouteTestCase(IPAddressFieldMixin, APIViewTestCases.APIViewTestCase):
    model = StaticRoute
    view_namespace = "plugins-api:netbox_routing"
    brief_fields = ['description', 'display', 'id', 'name', 'next_hop', 'prefix', 'url', ]


    bulk_update_data = {
        'metric': 5
    }

    @classmethod
    def setUpTestData(cls):

        device = create_test_device(name='Test Device')
        vrf = VRF.objects.create(name='Test VRF')

        nh = IPAddress('10.10.10.1')

        routes = (
            StaticRoute(name='Test Route 1', vrf=vrf, prefix='0.0.0.0/0', next_hop=nh),
            StaticRoute(name='Test Route 2', vrf=None, prefix='1.1.1.1/32', next_hop=nh),
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
                'permanent': True
            },
            {
                'name': 'Google DNS',
                'devices': [device.pk],
                'vrf': None,
                'prefix': '4.4.4.4/32',
                'next_hop': '10.10.10.1',
                'metric': 1,
                'permanent': True
            },
            {
                'name': 'One dot one dot one dot one',
                'devices': [device.pk],
                'vrf': None,
                'prefix': '1.1.1.0/24',
                'next_hop': '10.10.10.1',
                'metric': 1,
                'permanent': True
            },
        ]
