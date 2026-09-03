from django.urls import reverse
from rest_framework import status

from utilities.testing import APITestCase

from netbox_routing.tests.eigrp.test_api import *
from netbox_routing.tests.isis.test_api import *
from netbox_routing.tests.ospf.test_api import *
from netbox_routing.tests.static.test_api import *

__all__ = (
    'AppTest',
    'StaticRouteTestCase',
    'OSPFInstanceTestCase',
    'OSPFAreaTestCase',
    'OSPFInterfaceTestCase',
    'ISISInstanceAPITestCase',
    'ISISInterfaceAPITestCase',
    'ISISSettingAPITestCase',
    'ISISLevelAPITestCase',
    'ISISInterfaceLevelAPITestCase',
    'ISISSegmentRoutingAPITestCase',
    'ISISFlexAlgoAPITestCase',
    'ISISPrefixSIDAPITestCase',
    'ISISSRv6LocatorAPITestCase',
    'ISISSettingPrefetchAPITestCase',
    'ISISChildDisplayPrefetchAPITestCase',
    'ISISSettingAssignmentAPITestCase',
    'EIGRPRouterTestCase',
    'EIGRPAddressFamilyTestCase',
    'EIGRPNetworkTestCase',
    'EIGRPInterfaceTestCase',
)


class AppTest(APITestCase):
    def test_root(self):
        url = reverse("plugins-api:netbox_routing-api:api-root")
        response = self.client.get(f"{url}?format=api", **self.header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
