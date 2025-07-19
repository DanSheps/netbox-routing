from django.core.exceptions import ValidationError
from django.test import TestCase
from netaddr import IPAddress, IPNetwork

from utilities.testing import create_test_device

from netbox_routing.models.static import StaticRoute

__all__ = (
    'StaticRouteTestCase',
)


class StaticRouteTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.device = create_test_device(name='Device 1')

    def test_clean_ip_versions(self):
        # pass: both IPv4
        route1 = StaticRoute(prefix=IPNetwork('0.0.0.0/0'), next_hop=IPAddress('1.2.3.4'))
        route1.clean()

        # pass: both IPv6
        route2 = StaticRoute(prefix=IPNetwork('::/0'), next_hop=IPAddress('fe80::1'))
        route2.clean()

        # fail: mixed
        route3 = StaticRoute(prefix=IPNetwork('0.0.0.0/0'), next_hop=IPAddress('fe80::1'))
        self.assertRaises(ValidationError, route3.clean)
