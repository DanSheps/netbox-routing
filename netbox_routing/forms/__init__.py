from .filtersets import *
from .bulk_edit import *
from .bulk_import import *
from .objects import PrefixListForm, PrefixListEntryForm, RouteMapForm, RouteMapEntryForm
from .ospf import OSPFAreaForm, OSPFInstanceForm, OSPFInterfaceForm
from .bgp import BGPRouterForm, BGPScopeForm, BGPAddressFamilyForm
from .static import StaticRouteForm
from .eigrp import *

__all__ = (
    
    # Static Routes
    'StaticRouteForm',
    'StaticRouteFilterForm',

    # OSPF
    'OSPFAreaForm',
    'OSPFAreaBulkEditForm',
    'OSPFAreaImportForm',
    'OSPFAreaFilterForm',

    'OSPFInstanceForm',
    'OSPFInstanceBulkEditForm',
    'OSPFInstanceFilterForm',
    'OSPFInstanceImportForm',

    'OSPFInterfaceForm',
    'OSPFInterfaceFilterForm',
    'OSPFInterfaceBulkEditForm',
    'OSPFInterfaceImportForm',

    # EIGRP
    'EIGRPRouterForm',
    'EIGRPRouterBulkEditForm',
    'EIGRPRouterFilterForm',
    'EIGRPRouterImportForm',

    'EIGRPAddressFamilyForm',
    'EIGRPAddressFamilyBulkEditForm',
    'EIGRPAddressFamilyFilterForm',
    'EIGRPAddressFamilyImportForm',

    'EIGRPNetworkForm',
    'EIGRPNetworkBulkEditForm',
    'EIGRPNetworkFilterForm',
    'EIGRPNetworkImportForm',

    'EIGRPInterfaceForm',
    'EIGRPInterfaceBulkEditForm',
    'EIGRPInterfaceFilterForm',
    'EIGRPInterfaceImportForm',

    # BGP
    'BGPRouterForm',
    'BGPScopeForm',
    'BGPAddressFamilyForm',
    'BGPRouterFilterForm',
    'BGPScopeFilterForm',
    'BGPAddressFamilyFilterForm',
    'BGPSettingFilterForm',

    # Objects
    'PrefixListForm',
    'PrefixListEntryForm',
    'RouteMapForm',
    'RouteMapEntryForm',
    'PrefixListFilterForm',
    'PrefixListEntryFilterForm',
    'RouteMapFilterForm',
    'RouteMapEntryFilterForm'
)
