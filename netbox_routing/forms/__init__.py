from .filtersets import *
from .bulk_edit import *
from .bulk_import import *
from .objects import (
    PrefixListForm,
    PrefixListEntryForm,
    RouteMapForm,
    RouteMapEntryForm,
)
from netbox_routing.forms.model_objects.ospf import *
from netbox_routing.forms.model_objects.isis import *
from netbox_routing.forms.model_objects.bgp import *
from netbox_routing.forms.model_objects.static import StaticRouteForm
from netbox_routing.forms.model_objects.eigrp import *

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
    # IS-IS
    'ISISInstanceForm',
    'ISISInstanceBulkEditForm',
    'ISISInstanceFilterForm',
    'ISISInstanceImportForm',
    'ISISInterfaceForm',
    'ISISInterfaceFilterForm',
    'ISISInterfaceBulkEditForm',
    'ISISInterfaceImportForm',
    'ISISSettingForm',
    'ISISSettingFilterForm',
    'ISISSettingBulkEditForm',
    'ISISSettingImportForm',
    'ISISLevelForm',
    'ISISLevelFilterForm',
    'ISISLevelImportForm',
    'ISISInterfaceLevelForm',
    'ISISInterfaceLevelFilterForm',
    'ISISInterfaceLevelImportForm',
    'ISISSegmentRoutingForm',
    'ISISSegmentRoutingFilterForm',
    'ISISSegmentRoutingImportForm',
    'ISISFlexAlgoForm',
    'ISISFlexAlgoFilterForm',
    'ISISFlexAlgoImportForm',
    'ISISPrefixSIDForm',
    'ISISPrefixSIDFilterForm',
    'ISISPrefixSIDImportForm',
    'ISISSRv6LocatorForm',
    'ISISSRv6LocatorFilterForm',
    'ISISSRv6LocatorImportForm',
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
    'BGPSettingForm',
    'BGPRouterForm',
    'BGPScopeForm',
    'BGPAddressFamilyForm',
    'BGPRouterFilterForm',
    'BGPScopeFilterForm',
    'BGPAddressFamilyFilterForm',
    'BGPSettingFilterForm',
    # BFD
    'BFDProfileForm',
    'BFDProfileBulkEditForm',
    'BFDProfileFilterForm',
    # Objects
    'PrefixListForm',
    'PrefixListEntryForm',
    'RouteMapForm',
    'RouteMapEntryForm',
    'PrefixListFilterForm',
    'PrefixListEntryFilterForm',
    'RouteMapFilterForm',
    'RouteMapEntryFilterForm',
)
