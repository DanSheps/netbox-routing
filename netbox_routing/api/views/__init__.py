from .static import StaticRouteViewSet
from .ospf import OSPFInstanceViewSet, OSPFAreaViewSet, OSPFInterfaceViewSet
from .bgp import BGPRouterViewSet, BGPScopeViewSet, BGPAddressFamilyViewSet, BGPSettingViewSet
from .objects import PrefixListViewSet, PrefixListEntryViewSet, RouteMapViewSet, RouteMapEntryViewSet
from .eigrp import (
    EIGRPRouterViewSet, EIGRPAddressFamilyViewSet,
    EIGRPNetworkViewSet, EIGRPInterfaceViewSet
)

__all__ = (
    'StaticRouteViewSet',

    'BGPRouterViewSet',
    'BGPScopeViewSet',
    'BGPAddressFamilyViewSet',
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
)
