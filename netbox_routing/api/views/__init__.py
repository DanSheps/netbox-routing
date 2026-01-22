from .community import *
from .static import StaticRouteViewSet
from .ospf import OSPFInstanceViewSet, OSPFAreaViewSet, OSPFInterfaceViewSet
from .bgp import *
from .objects import *
from .eigrp import (
    EIGRPRouterViewSet,
    EIGRPAddressFamilyViewSet,
    EIGRPNetworkViewSet,
    EIGRPInterfaceViewSet,
)

__all__ = (
    'StaticRouteViewSet',
    'BGPSettingViewSet',
    'BGPRouterViewSet',
    'BGPScopeViewSet',
    'BGPAddressFamilyViewSet',
    'BGPPeerViewSet',
    'BGPPeerTemplateViewSet',
    'BGPPolicyTemplateViewSet',
    'BGPSessionTemplateViewSet',
    'BGPPeerAddressFamilyViewSet',
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
    'CommunityViewSet',
    'CommunityListViewSet',
    'CommunityListEntryViewSet',
    'ASPathViewSet',
    'ASPathEntryViewSet',
)
