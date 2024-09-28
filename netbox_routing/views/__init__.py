from .static import *

from .objects import PrefixListView, PrefixListEditView, PrefixListListView, PrefixListDeleteView, RouteMapListView, \
    RouteMapView, RouteMapEditView, RouteMapDeleteView, PrefixListEntryListView, PrefixListEntryEditView, \
    PrefixListEntryDeleteView, PrefixListEntryView, RouteMapEntryListView, RouteMapEntryView, RouteMapEntryEditView, \
    RouteMapEntryDeleteView, PrefixListEntriesView, RouteMapEntriesView, RouteMapEntryBulkEditView, \
    RouteMapEntryBulkDeleteView, PrefixListEntryBulkDeleteView, PrefixListEntryBulkEditView

from .ospf import *
from .eigrp import *
from .bgp import *
from .core import *

__all__ = (
    # Core View Extensions
    'DeviceStaticRoutesView',

    # Static
    'StaticRouteListView',
    'StaticRouteView',
    'StaticRouteDevicesView',
    'StaticRouteEditView',
    'StaticRouteBulkEditView',
    'StaticRouteDeleteView',
    'StaticRouteBulkDeleteView',

    # OSPF
    'OSPFInstanceListView',
    'OSPFInstanceView',
    'OSPFInstanceEditView',
    'OSPFInstanceDeleteView',
    'OSPFInstanceInterfacesView',

    'OSPFAreaListView',
    'OSPFAreaView',
    'OSPFAreaInterfacesView',
    'OSPFAreaEditView',
    'OSPFAreaDeleteView',

    'OSPFInterfaceListView',
    'OSPFInterfaceView',
    'OSPFInterfaceEditView',
    'OSPFInterfaceDeleteView',

    # EIGRP
    'EIGRPRouterListView',
    'EIGRPRouterView',
    'EIGRPRouterInterfacesView',
    'EIGRPRouterEditView',
    'EIGRPRouterImportView',
    'EIGRPRouterBulkEditView',
    'EIGRPRouterDeleteView',
    'EIGRPRouterBulkDeleteView',

    'EIGRPAddressFamilyListView',
    'EIGRPAddressFamilyView',
    'EIGRPAddressFamilyInterfacesView',
    'EIGRPAddressFamilyEditView',
    'EIGRPAddressFamilyBulkEditView',
    'EIGRPAddressFamilyDeleteView',
    'EIGRPAddressFamilyBulkDeleteView',

    'EIGRPNetworkListView',
    'EIGRPNetworkView',
    'EIGRPNetworkEditView',
    'EIGRPNetworkBulkEditView',
    'EIGRPNetworkDeleteView',
    'EIGRPNetworkBulkDeleteView',

    'EIGRPInterfaceListView',
    'EIGRPInterfaceView',
    'EIGRPInterfaceEditView',
    'EIGRPInterfaceBulkEditView',
    'EIGRPInterfaceDeleteView',
    'EIGRPInterfaceBulkDeleteView',

    'BGPRouterView',
    'BGPRouterEditView',

    # Routing Objects
    'PrefixListListView',
    'PrefixListView',
    'PrefixListEntriesView',
    'PrefixListEditView',
    'PrefixListDeleteView',
    'PrefixListEntryListView',
    'PrefixListEntryView',
    'PrefixListEntryEditView',
    'PrefixListEntryDeleteView',
    'PrefixListEntryBulkEditView',
    'PrefixListEntryBulkDeleteView',

    'RouteMapListView',
    'RouteMapView',
    'RouteMapEntriesView',
    'RouteMapEditView',
    'RouteMapDeleteView',
    'RouteMapEntryListView',
    'RouteMapEntryView',
    'RouteMapEntryEditView',
    'RouteMapEntryDeleteView',
    'RouteMapEntryBulkEditView',
    'RouteMapEntryBulkDeleteView',

)
