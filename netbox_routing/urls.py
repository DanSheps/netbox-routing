from django.urls import path

from netbox.views.generic import ObjectChangeLogView

from . import views
from .models import StaticRoute, PrefixList, PrefixListEntry, RouteMap, RouteMapEntry, OSPFInstance, OSPFArea, \
    OSPFInterface, BGPRouter, BGPScope, BGPAddressFamily

urlpatterns = [
    path('routes/static/', views.StaticRouteListView.as_view(), name='staticroute_list'),
    path('routes/static/add/', views.StaticRouteEditView.as_view(), name='staticroute_add'),
    path('routes/static/import/', views.StaticRouteListView.as_view(), name='staticroute_import'),
    path('routes/static/<int:pk>/', views.StaticRouteView.as_view(), name='staticroute'),
    path('routes/static/<int:pk>/edit/', views.StaticRouteEditView.as_view(), name='staticroute_edit'),
    path('routes/static/<int:pk>/devices/', views.StaticRouteDevicesView.as_view(), name='staticroute_devices'),
    path('routes/static/<int:pk>/delete/', views.StaticRouteDeleteView.as_view(), name='staticroute_delete'),
    path('routes/static/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='staticroute_changelog', kwargs={'model': StaticRoute}),

    path('ospf/instance/', views.OSPFInstanceListView.as_view(), name='ospfinstance_list'),
    path('ospf/instance/add/', views.OSPFInstanceEditView.as_view(), name='ospfinstance_add'),
    path('ospf/instance/import/', views.OSPFInstanceListView.as_view(), name='ospfinstance_import'),
    path('ospf/instance/<int:pk>/', views.OSPFInstanceView.as_view(), name='ospfinstance'),
    path('ospf/instance/<int:pk>/edit/', views.OSPFInstanceEditView.as_view(), name='ospfinstance_edit'),
    path('ospf/instance/<int:pk>/interfaces/', views.OSPFInstanceInterfacesView.as_view(), name='ospfinstance_interfaces'),
    path('ospf/instance/<int:pk>/delete/', views.OSPFInstanceDeleteView.as_view(), name='ospfinstance_delete'),
    path('ospf/instance/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='ospfinstance_changelog', kwargs={'model': OSPFInstance}),

    path('ospf/area/', views.OSPFAreaListView.as_view(), name='ospfarea_list'),
    path('ospf/area/add/', views.OSPFAreaEditView.as_view(), name='ospfarea_add'),
    path('ospf/area/import/', views.OSPFAreaListView.as_view(), name='ospfarea_import'),
    path('ospf/area/<int:pk>/', views.OSPFAreaView.as_view(), name='ospfarea'),
    path('ospf/area/<int:pk>/edit/', views.OSPFAreaEditView.as_view(), name='ospfarea_edit'),
    path('ospf/area/<int:pk>/interfaces/', views.OSPFAreaInterfacesView.as_view(), name='ospfarea_interfaces'),
    path('ospf/area/<int:pk>/delete/', views.OSPFAreaDeleteView.as_view(), name='ospfarea_delete'),
    path('ospf/area/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='ospfarea_changelog', kwargs={'model': OSPFArea}),

    path('ospf/interface/', views.OSPFInterfaceListView.as_view(), name='ospfinterface_list'),
    path('ospf/interface/add/', views.OSPFInterfaceEditView.as_view(), name='ospfinterface_add'),
    path('ospf/interface/import/', views.OSPFInterfaceListView.as_view(), name='ospfinterface_import'),
    path('ospf/interface/<int:pk>/', views.OSPFInterfaceView.as_view(), name='ospfinterface'),
    path('ospf/interface/<int:pk>/edit/', views.OSPFInterfaceEditView.as_view(), name='ospfinterface_edit'),
    path('ospf/interface/<int:pk>/delete/', views.OSPFInterfaceDeleteView.as_view(), name='ospfinterface_delete'),
    path('ospf/interface/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='ospfinterface_changelog', kwargs={'model': OSPFInterface}),

    path('bgp/router/', views.BGPRouterListView.as_view(), name='bgprouter_list'),
    path('bgp/router/add/', views.BGPRouterEditView.as_view(), name='bgprouter_add'),
    path('bgp/router/<int:pk>/', views.BGPRouterView.as_view(), name='bgprouter'),
    path('bgp/router/<int:pk>/edit', views.BGPRouterEditView.as_view(), name='bgprouter_edit'),
    path('bgp/router/<int:pk>/delete', views.BGPRouterEditView.as_view(), name='bgprouter_delete'),
    path('bgp/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='bgprouter_changelog', kwargs={'model': BGPRouter}),

    path('bgp/scope/', views.BGPScopeListView.as_view(), name='bgpscope_list'),
    path('bgp/scope/add/', views.BGPScopeEditView.as_view(), name='bgpscope_add'),
    path('bgp/scope/<int:pk>/', views.BGPScopeView.as_view(), name='bgpscope'),
    path('bgp/scope/<int:pk>/edit', views.BGPScopeEditView.as_view(), name='bgpscope_edit'),
    path('bgp/scope/<int:pk>/delete', views.BGPScopeEditView.as_view(), name='bgpscope_delete'),
    path('bgp/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='bgpscope_changelog', kwargs={'model': BGPScope}),

    path('bgp/address_family/', views.BGPAddressFamilyListView.as_view(), name='bgpaddressfamily_list'),
    path('bgp/address_family/add/', views.BGPAddressFamilyEditView.as_view(), name='bgpaddressfamily_add'),
    path('bgp/address_family/<int:pk>/', views.BGPAddressFamilyView.as_view(), name='bgpaddressfamily'),
    path('bgp/address_family/<int:pk>/edit', views.BGPAddressFamilyEditView.as_view(), name='bgpaddressfamily_edit'),
    path('bgp/address_family/<int:pk>/delete', views.BGPAddressFamilyEditView.as_view(), name='bgpaddressfamily_delete'),
    path('bgp/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='bgpaddressfamily_changelog', kwargs={'model': BGPAddressFamily}),

    path('prefix-list/', views.PrefixListListView.as_view(), name='prefixlist_list'),
    path('prefix-list/add/', views.PrefixListEditView.as_view(), name='prefixlist_add'),
    path('prefix-list/import/', views.PrefixListListView.as_view(), name='prefixlist_import'),
    path('prefix-list/<int:pk>/', views.PrefixListView.as_view(), name='prefixlist'),
    path('prefix-list/<int:pk>/edit/', views.PrefixListEditView.as_view(), name='prefixlist_edit'),
    path('prefix-list/<int:pk>/entries/', views.PrefixListEntriesView.as_view(), name='prefixlist_entries'),
    path('prefix-list/<int:pk>/delete/', views.PrefixListView.as_view(), name='prefixlist_delete'),
    path('prefix-list/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='prefixlist_changelog', kwargs={'model': PrefixList}),

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
    path('route-map/<int:pk>/edit/', views.RouteMapEditView.as_view(), name='routemap_edit'),
    path('route-map/<int:pk>/delete/', views.RouteMapView.as_view(), name='routemap_delete'),
    path('route-map/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='routemap_changelog', kwargs={'model': RouteMap}),

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
