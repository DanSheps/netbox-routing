from netbox_routing.tests.eigrp.test_forms import *
from netbox_routing.tests.isis.test_forms import *
from netbox_routing.tests.ospf.test_forms import *
from netbox_routing.tests.static.test_forms import *

__all__ = (
    'StaticRouteTestCase',
    'OSPFInstanceTestCase',
    'OSPFAreaTestCase',
    'OSPFInterfaceTestCase',
    'ISISBulkEditFieldsetTestCase',
    'ISISInstanceFormTestCase',
    'ISISInterfaceFormTestCase',
    'ISISInterfaceImportFormTestCase',
    'ISISInstanceImportFormTestCase',
    'ISISSettingFormInitialTestCase',
    'EIGRPRouterTestCase',
    'EIGRPAddressFamilyTestCase',
    'EIGRPNetworkTestCase',
    'EIGRPInterfaceTestCase',
)
