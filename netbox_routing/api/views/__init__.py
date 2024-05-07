from .static import StaticRouteViewSet
from .ospf import OSPFInstanceViewSet, OSPFAreaViewSet, OSPFInterfaceViewSet
from .bgp import BGPRouterViewSet, BGPScopeViewSet, BGPAddressFamilyViewSet, BGPSettingViewSet
from .objects import PrefixListViewSet, PrefixListEntryViewSet, RouteMapViewSet, RouteMapEntryViewSet

__all__ = (
    'StaticRouteViewSet',

    'BGPRouterViewSet',
    'BGPScopeViewSet',
    'BGPAddressFamilyViewSet',
    'BGPSettingViewSet',

    'OSPFInstanceViewSet',
    'OSPFAreaViewSet',
    'OSPFInterfaceViewSet',

    'PrefixListViewSet',
    'PrefixListEntryViewSet',
    'RouteMapViewSet',
    'RouteMapEntryViewSet',
)
