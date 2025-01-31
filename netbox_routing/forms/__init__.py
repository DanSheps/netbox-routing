from .filtersets import *
from .bulk_edit import *
from .bulk_import import *
from .model_objects.objects import PrefixListForm, PrefixListEntryForm, RouteMapForm, RouteMapEntryForm
from .ospf import OSPFAreaForm, OSPFInstanceForm, OSPFInterfaceForm
from .bgp import *
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
    'BGPRouterFilterForm',
    'BGPScopeFilterForm',
    'BGPSessionTemplateFilterForm',
    'BGPPolicyTemplateFilterForm',
    'BGPPeerTemplateFilterForm',
    'BGPAddressFamilyFilterForm',
    'BGPPeerFilterForm',
    'BGPPeerAddressFamilyFilterForm',
    'BGPSettingFilterForm',

    # Objects
    'PrefixListFilterForm',
    'PrefixListEntryFilterForm',
    'RouteMapFilterForm',
    'RouteMapEntryFilterForm'
)
