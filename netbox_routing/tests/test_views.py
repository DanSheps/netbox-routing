from netbox_routing.tests.eigrp.test_views import *
from netbox_routing.tests.isis.test_views import *
from netbox_routing.tests.ospf.test_views import *
from netbox_routing.tests.static.test_views import *

__all__ = (
    'StaticRouteTestCase',
    'OSPFInstanceTestCase',
    'OSPFAreaTestCase',
    'OSPFInterfaceTestCase',
    'ISISInstanceViewTestCase',
    'ISISInterfaceViewTestCase',
    # 'EIGRPRouterTestCase',
    # 'EIGRPAddressFamilyTestCase',
    # 'EIGRPNetworkTestCase',
    # 'EIGRPInterfaceTestCase',
)
