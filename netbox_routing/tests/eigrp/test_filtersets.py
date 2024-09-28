import netaddr
from django.test import TestCase

from dcim.models import Device, Interface
from ipam.models import VRF
from utilities.testing import create_test_device

from netbox_routing.filtersets import *
from netbox_routing.models import *

__all__ = (
    'EIGRPRouterTestCase',
    'EIGRPAddressFamilyTestCase',
    'EIGRPNetworkTestCase',
    'EIGRPInterfaceTestCase',
)


class EIGRPRouterTestCase(TestCase):
    pass


class EIGRPAddressFamilyTestCase(TestCase):
    pass


class EIGRPNetworkTestCase(TestCase):
    pass


class EIGRPInterfaceTestCase(TestCase):
    pass
