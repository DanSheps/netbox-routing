from netbox_routing.tests.eigrp.test_forms import *
from netbox_routing.tests.ospf.test_forms import *
from netbox_routing.tests.static.test_forms import *

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
