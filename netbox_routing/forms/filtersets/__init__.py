from .static import StaticRouteFilterForm
from .bgp import BGPRouterFilterForm, BGPScopeFilterForm, BGPAddressFamilyFilterForm, BGPSettingFilterForm
from .ospf import OSPFAreaFilterForm, OSPFInstanceFilterForm, OSPFInterfaceFilterForm
from .objects import PrefixListFilterForm, PrefixListEntryFilterForm, RouteMapFilterForm,\
    RouteMapEntryFilterForm
from .eigrp import *

__all__ = (
    # Static
    'StaticRouteFilterForm',

    # BGP
    'BGPRouterFilterForm',
    'BGPScopeFilterForm',
    'BGPAddressFamilyFilterForm',
    'BGPSettingFilterForm',

    # EIGRP
    'EIGRPRouterFilterForm',
    'EIGRPAddressFamilyFilterForm',
    'EIGRPNetworkFilterForm',
    'EIGRPInterfaceFilterForm',

    # OSPF
    'OSPFAreaFilterForm',
    'OSPFInstanceFilterForm',
    'OSPFInterfaceFilterForm',

    # Routing Objects
    'PrefixListFilterForm',
    'PrefixListEntryFilterForm',
    'RouteMapFilterForm',
    'RouteMapEntryFilterForm'
)
