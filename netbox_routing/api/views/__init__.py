from .static import StaticRouteViewSet
from .ospf import OSPFInstanceViewSet, OSPFAreaViewSet, OSPFInterfaceViewSet
from .objects import PrefixListViewSet, PrefixListEntryViewSet, RouteMapViewSet, RouteMapEntryViewSet

__all__ = (
    'StaticRouteViewSet',
    'OSPFInstanceViewSet',
    'OSPFAreaViewSet',
    'OSPFInterfaceViewSet',
    'PrefixListViewSet',
    'PrefixListEntryViewSet',
    'RouteMapViewSet',
    'RouteMapEntryViewSet',
)
