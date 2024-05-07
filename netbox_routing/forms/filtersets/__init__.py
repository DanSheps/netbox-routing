from .static import StaticRouteFilterForm
from .bgp import BGPRouterFilterForm, BGPScopeFilterForm, BGPAddressFamilyFilterForm, BGPSettingFilterForm
from .ospf import OSPFAreaFilterForm, OSPFInstanceFilterForm, OSPFInterfaceFilterForm
from .objects import PrefixListFilterForm, PrefixListEntryFilterForm, RouteMapFilterForm,\
    RouteMapEntryFilterForm

__all__ = (
    # Static
    'StaticRouteFilterForm',

    # BGP
    'BGPRouterFilterForm',
    'BGPScopeFilterForm',
    'BGPAddressFamilyFilterForm',
    'BGPSettingFilterForm',

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
