from netbox_routing.tests.eigrp.test_filtersets import *
from netbox_routing.tests.ospf.test_filtersets import *
from netbox_routing.tests.static.test_filtersets import *

__all__ = (
    'StaticRouteTestCase',
    'OSPFInstanceTestCase',
    'OSPFAreaTestCase',
    'OSPFInterfaceTestCase',
    'EIGRPRouterTestCase',
    'EIGRPAddressFamilyTestCase',
    'EIGRPNetworkTestCase',
    'EIGRPInterfaceTestCase',
)
