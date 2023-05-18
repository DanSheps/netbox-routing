from .static import StaticRouteListView, StaticRouteDevicesView, StaticRouteEditView, StaticRouteView, \
    StaticRouteDeleteView

from .objects import PrefixListView, PrefixListEditView, PrefixListListView, PrefixListDeleteView, RouteMapListView, \
    RouteMapView, RouteMapEditView, RouteMapDeleteView, PrefixListEntryListView, PrefixListEntryEditView, \
    PrefixListEntryDeleteView, PrefixListEntryView, RouteMapEntryListView, RouteMapEntryView, RouteMapEntryEditView, \
    RouteMapEntryDeleteView, PrefixListEntriesView, RouteMapEntriesView, RouteMapEntryBulkEditView, \
    RouteMapEntryBulkDeleteView, PrefixListEntryBulkDeleteView, PrefixListEntryBulkEditView

__all__ = (
    'StaticRouteListView',
    'StaticRouteView',
    'StaticRouteDevicesView',
    'StaticRouteEditView',
    'StaticRouteDeleteView',

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
