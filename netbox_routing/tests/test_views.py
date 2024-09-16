import netaddr

from dcim.models import Device
from extras.models import Tag
from ipam.models import VRF
from utilities.testing import ViewTestCases, create_tags, create_test_device

from netbox_routing.models import StaticRoute


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

        """
        cls.csv_data = (
            "name,slug,description",
            "Region 4,region-4,Fourth region",
            "Region 5,region-5,Fifth region",
            "Region 6,region-6,Sixth region",
        )

        cls.csv_update_data = (
            "id,name,description",
            f"{regions[0].pk},Region 7,Fourth region7",
            f"{regions[1].pk},Region 8,Fifth region8",
            f"{regions[2].pk},Region 0,Sixth region9",
        )
        """

    def _get_base_url(self):
        return 'plugins:netbox_routing:staticroute_{}'
