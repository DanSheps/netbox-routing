from .static import StaticRouteViewSet
from .ospf import OSPFInstanceViewSet, OSPFAreaViewSet, OSPFInterfaceViewSet
from .bgp import *
from .communities import *
from .objects import PrefixListViewSet, PrefixListEntryViewSet, RouteMapViewSet, RouteMapEntryViewSet
from .eigrp import *

__all__ = (
    'StaticRouteViewSet',

    'BGPRouterViewSet',
    'BGPScopeViewSet',
    'BGPSessionTemplateViewSet',
    'BGPPolicyTemplateViewSet',
    'BGPPeerTemplateViewSet',
    'BGPAddressFamilyViewSet',
    'BGPPeerViewSet',
    'BGPPeerAddressFamilyViewSet',
    'BGPSettingViewSet',

    'EIGRPRouterViewSet',
    'EIGRPAddressFamilyViewSet',
    'EIGRPNetworkViewSet',
    'EIGRPInterfaceViewSet',

    'OSPFInstanceViewSet',
    'OSPFAreaViewSet',
    'OSPFInterfaceViewSet',

    'PrefixListViewSet',
    'PrefixListEntryViewSet',
    'RouteMapViewSet',
    'RouteMapEntryViewSet',

    'CommunityListViewSet',
    'CommunityViewSet',
)
