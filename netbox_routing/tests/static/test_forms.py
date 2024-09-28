from django.test import TestCase

from dcim.models import Device
from utilities.testing import create_test_device

from netbox_routing.forms import *

__all__ = (
    'StaticRouteTestCase',
)


class StaticRouteTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        device = create_test_device(name='Device 1')

    def test_staticroute(self):
        form = StaticRouteForm(data={
            'name': 'Route 1',
            'devices': [Device.objects.first().pk],
            'vrf': None,
            'prefix': '0.0.0.0/0',
            'next_hop': '10.10.10.1',
            'metric': 1,
        })
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())
