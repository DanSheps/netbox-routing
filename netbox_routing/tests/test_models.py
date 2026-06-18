from netbox_routing.tests.community.test_models import *
from netbox_routing.tests.eigrp.test_models import *
from netbox_routing.tests.isis.test_models import *
from netbox_routing.tests.ospf.test_models import *
from netbox_routing.tests.static.test_models import *

__all__ = (
    'StaticRouteTestCase',
    'OSPFInstanceTestCase',
    'OSPFAreaTestCase',
    'OSPFInterfaceTestCase',
    'ISISInstanceModelTestCase',
    'ISISInterfaceModelTestCase',
    'EIGRPRouterTestCase',
    'EIGRPAddressFamilyTestCase',
    'EIGRPNetworkTestCase',
    'EIGRPInterfaceTestCase',
    'CommunityTestCase',
    'CommunityListTestCase',
    'CommunityListEntryTestCase',
)
