from django.core.exceptions import ValidationError
from django.test import TestCase

from utilities.testing import create_test_device

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
