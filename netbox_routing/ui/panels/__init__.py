from .core import *
from .bgp import *
from .community import *
from .eigrp import *
from .isis import *
from .static import *
from .objects import *
from .ospf import *

__all__ = (
    'SettingsChoicePanel',
    'BGPSettingPanel',
    'BGPPeerTemplatePanel',
    'BGPPolicyTemplatePanel',
    'BGPSessionTemplatePanel',
    'BGPPolicyFilteringPanel',
    'BGPRouterPanel',
    'BGPRouterTemplatesPanel',
    'BGPScopePanel',
    'BGPAddressFamilyPanel',
    'BGPPeerPanel',
    'BGPPeerAddressFamilyPanel',
    'BGPPeerSettingPanel',
    'CommunityListPanel',
    'CommunityPanel',
    'CommunityListEntryPanel',
    'EIGRPRouterPanel',
    'EIGRPAddressFamilyPanel',
    'EIGRPNetworkPanel',
    'EIGRPInterfacePanel',
    'StaticRoutePanel',
    'StaticRouteRoutePanel',
    'BFDProfilePanel',
    'BFDProfileSessionPanel',
    'CustomPrefixPanel',
    'ASPathPanel',
    'ASPathEntryPanel',
    'PrefixListPanel',
    'PrefixListEntryPanel',
    'RouteMapPanel',
    'RouteMapEntryPanel',
    'RouteMapEntryMatchPanel',
    'RouteMapEntrySetPanel',
    'OSPFInstancePanel',
    'OSPFAreaPanel',
    'OSPFInterfacePanel',
    'OSPFInterfaceSettingsPanel',
    'ISISInstancePanel',
    'ISISInstanceSettingsPanel',
    'ISISInterfacePanel',
    'ISISInterfaceSettingsPanel',
    'ISISSettingPanel',
    'ISISLevelPanel',
    'ISISInterfaceLevelPanel',
    'ISISSegmentRoutingPanel',
    'ISISFlexAlgoPanel',
)
