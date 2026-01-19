from .static import StaticRouteViewSet
from .ospf import OSPFInstanceViewSet, OSPFAreaViewSet, OSPFInterfaceViewSet
from .bgp import *
from .objects import (
    PrefixListViewSet,
    PrefixListEntryViewSet,
    RouteMapViewSet,
    RouteMapEntryViewSet,
)
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
)
