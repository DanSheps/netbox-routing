from .static import StaticRouteListView, StaticRouteEditView, StaticRouteView, StaticRouteDeleteView

from .objects import PrefixListView, PrefixListEditView, PrefixListListView, PrefixListDeleteView, RouteMapListView, \
    RouteMapView, RouteMapEditView, RouteMapDeleteView, PrefixListEntryListView, PrefixListEntryEditView, \
    PrefixListEntryDeleteView, PrefixListEntryView, RouteMapEntryListView, RouteMapEntryView, RouteMapEntryEditView, \
    RouteMapEntryDeleteView

__all__ = (
    'StaticRouteListView',
    'StaticRouteView',
    'StaticRouteEditView',
    'StaticRouteDeleteView',

    'PrefixListListView',
    'PrefixListView',
    'PrefixListEditView',
    'PrefixListDeleteView',
    'PrefixListEntryListView',
    'PrefixListEntryView',
    'PrefixListEntryEditView',
    'PrefixListEntryDeleteView',

    'RouteMapListView',
    'RouteMapView',
    'RouteMapEditView',
    'RouteMapDeleteView',
    'RouteMapEntryListView',
    'RouteMapEntryView',
    'RouteMapEntryEditView',
    'RouteMapEntryDeleteView'

)
