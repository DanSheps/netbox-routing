import netaddr

from ipam.models import VRF
from utilities.testing import ViewTestCases, create_test_device

from netbox_routing.models import StaticRoute

__all__ = (
    'StaticRouteTestCase',
)


class StaticRouteTestCase(
        ViewTestCases.GetObjectViewTestCase,
        ViewTestCases.GetObjectChangelogViewTestCase,
        ViewTestCases.CreateObjectViewTestCase,
        ViewTestCases.EditObjectViewTestCase,
        ViewTestCases.DeleteObjectViewTestCase,
        ViewTestCases.ListObjectsViewTestCase,
        ViewTestCases.BulkEditObjectsViewTestCase,
        ViewTestCases.BulkDeleteObjectsViewTestCase
):
    # ViewTestCases.BulkImportObjectsViewTestCase,
    model = StaticRoute

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
        routes[2].devices.set([devices[0]])

        cls.form_data = {
            'name': 'Route X',
            'devices': [devices[1].pk],
            'vrf': vrf.pk,
            'prefix': netaddr.IPNetwork('1.1.1.1/32'),
            'next_hop': nh,
        }

        cls.bulk_edit_data = {
            'metric': 10,
        }

    def _get_base_url(self):
        return 'plugins:netbox_routing:staticroute_{}'
