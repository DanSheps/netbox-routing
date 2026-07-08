from .community import *
from .static import StaticRouteViewSet
from .ospf import OSPFInstanceViewSet, OSPFAreaViewSet, OSPFInterfaceViewSet
from .isis import (
    ISISInstanceViewSet,
    ISISInterfaceViewSet,
    ISISSettingViewSet,
    ISISLevelViewSet,
    ISISInterfaceLevelViewSet,
    ISISSegmentRoutingViewSet,
    ISISFlexAlgoViewSet,
    ISISPrefixSIDViewSet,
    ISISSRv6LocatorViewSet,
)
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
    'BFDProfileViewSet',
    'EIGRPRouterViewSet',
    'EIGRPAddressFamilyViewSet',
    'EIGRPNetworkViewSet',
    'EIGRPInterfaceViewSet',
    'OSPFInstanceViewSet',
    'OSPFAreaViewSet',
    'OSPFInterfaceViewSet',
    'ISISInstanceViewSet',
    'ISISInterfaceViewSet',
    'ISISSettingViewSet',
    'ISISLevelViewSet',
    'ISISInterfaceLevelViewSet',
    'ISISSegmentRoutingViewSet',
    'ISISFlexAlgoViewSet',
    'ISISPrefixSIDViewSet',
    'ISISSRv6LocatorViewSet',
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
