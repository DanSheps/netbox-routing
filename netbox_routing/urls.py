from django.urls import path

from netbox.views.generic import ObjectChangeLogView

from . import views
from .models import StaticRoute, PrefixList, PrefixListEntry, RouteMap, RouteMapEntry

urlpatterns = [
    path('routes/static/', views.StaticRouteListView.as_view(), name='staticroute_list'),
    path('routes/static/add/', views.StaticRouteEditView.as_view(), name='staticroute_add'),
    path('routes/static/import/', views.StaticRouteListView.as_view(), name='staticroute_import'),
    path('routes/static/<int:pk>/', views.StaticRouteView.as_view(), name='staticroute'),
    path('routes/static/<int:pk>/edit/', views.StaticRouteEditView.as_view(), name='staticroute_edit'),
    path('routes/static/<int:pk>/devices/', views.StaticRouteDevicesView.as_view(), name='staticroute_devices'),
    path('routes/static/<int:pk>/delete/', views.StaticRouteDeleteView.as_view(), name='staticroute_delete'),
    path('routes/static/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='staticroute_changelog', kwargs={'model': StaticRoute}),

    path('prefix-list/', views.PrefixListListView.as_view(), name='prefixlist_list'),
    path('prefix-list/add/', views.PrefixListEditView.as_view(), name='prefixlist_add'),
    path('prefix-list/import/', views.PrefixListListView.as_view(), name='prefixlist_import'),
    path('prefix-list/<int:pk>/', views.PrefixListView.as_view(), name='prefixlist'),
    path('prefix-list/<int:pk>/edit/', views.PrefixListView.as_view(), name='prefixlist_edit'),
    path('prefix-list/<int:pk>/entries/', views.PrefixListEntriesView.as_view(), name='prefixlist_entries'),
    path('prefix-list/<int:pk>/delete/', views.PrefixListView.as_view(), name='prefixlist_delete'),
    path('prefix-list/<int:pk>/changelog/', views.PrefixListView.as_view(), name='prefixlist_changelog', kwargs={'model': PrefixList}),

    path('prefix-list-entry/', views.PrefixListEntryListView.as_view(), name='prefixlistentry_list'),
    path('prefix-list-entry/add/', views.PrefixListEntryEditView.as_view(), name='prefixlistentry_add'),
    path('prefix-list-entry/edit/', views.PrefixListEntryBulkEditView.as_view(), name='prefixlistentry_bulk_edit'),
    path('prefix-list-entry/delete/', views.PrefixListEntryBulkDeleteView.as_view(), name='prefixlistentry_bulk_delete'),
    path('prefix-list-entry/import/', views.PrefixListEntryListView.as_view(), name='prefixlistentry_import'),
    path('prefix-list-entry/<int:pk>/', views.PrefixListEntryView.as_view(), name='prefixlistentry'),
    path('prefix-list-entry/<int:pk>/edit/', views.PrefixListEntryEditView.as_view(), name='prefixlistentry_edit'),
    path('prefix-list-entry/<int:pk>/delete/', views.PrefixListEntryDeleteView.as_view(), name='prefixlistentry_delete'),
    path('prefix-list-entry/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='prefixlistentry_changelog', kwargs={'model': PrefixListEntry}),

    path('route-map/', views.RouteMapListView.as_view(), name='routemap_list'),
    path('route-map/add/', views.RouteMapEditView.as_view(), name='routemap_add'),
    path('route-map/import/', views.RouteMapListView.as_view(), name='routemap_import'),
    path('route-map/<int:pk>/', views.RouteMapView.as_view(), name='routemap'),
    path('route-map/<int:pk>/entries/', views.RouteMapEntriesView.as_view(), name='routemap_entries'),
    path('route-map/<int:pk>/edit/', views.RouteMapView.as_view(), name='routemap_edit'),
    path('route-map/<int:pk>/delete/', views.RouteMapView.as_view(), name='routemap_delete'),
    path('route-map/<int:pk>/changelog/', views.RouteMapView.as_view(), name='routemap_changelog', kwargs={'model': RouteMap}),

    path('route-map-entry/', views.RouteMapEntryListView.as_view(), name='routemapentry_list'),
    path('route-map-entry/add/', views.RouteMapEntryEditView.as_view(), name='routemapentry_add'),
    path('route-map-entry/edit/', views.RouteMapEntryBulkEditView.as_view(), name='routemapentry_bulk_edit'),
    path('route-map-entry/delete/', views.RouteMapEntryBulkDeleteView.as_view(), name='routemapentry_bulk_delete'),
    path('route-map-entry/import/', views.RouteMapEntryListView.as_view(), name='routemapentry_import'),
    path('route-map-entry/<int:pk>/', views.RouteMapEntryView.as_view(), name='routemapentry'),
    path('route-map-entry/<int:pk>/edit/', views.RouteMapEntryEditView.as_view(), name='routemapentry_edit'),
    path('route-map-entry/<int:pk>/delete/', views.RouteMapEntryDeleteView.as_view(), name='routemapentry_delete'),
    path('route-map-entry/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='routemapentry_changelog', kwargs={'model': RouteMapEntry}),
]
