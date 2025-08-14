from django.urls import path, include

from utilities.urls import get_model_urls

from . import views  # noqa F401

urlpatterns = [
    path(
        'routes/static/',
        include(get_model_urls('netbox_routing', 'staticroute', detail=False)),
    ),
    path(
        'routes/static/<int:pk>/',
        include(get_model_urls('netbox_routing', 'staticroute')),
    ),
    path(
        'ospf/instance/',
        include(get_model_urls('netbox_routing', 'ospfinstance', detail=False)),
    ),
    path(
        'ospf/instance/<int:pk>/',
        include(get_model_urls('netbox_routing', 'ospfinstance')),
    ),
    path(
        'ospf/area/',
        include(get_model_urls('netbox_routing', 'ospfarea', detail=False)),
    ),
    path('ospf/area/<int:pk>/', include(get_model_urls('netbox_routing', 'ospfarea'))),
    path(
        'ospf/interface/',
        include(get_model_urls('netbox_routing', 'ospfinterface', detail=False)),
    ),
    path(
        'ospf/interface/<int:pk>/',
        include(get_model_urls('netbox_routing', 'ospfinterface')),
    ),
    path(
        'eigrp/router/',
        include(get_model_urls('netbox_routing', 'eigrprouter', detail=False)),
    ),
    path(
        'eigrp/router/<int:pk>/',
        include(get_model_urls('netbox_routing', 'eigrprouter')),
    ),
    path(
        'eigrp/address-family/',
        include(get_model_urls('netbox_routing', 'eigrpaddressfamily', detail=False)),
    ),
    path(
        'eigrp/address-family/<int:pk>/',
        include(get_model_urls('netbox_routing', 'eigrpaddressfamily')),
    ),
    path(
        'eigrp/network/',
        include(get_model_urls('netbox_routing', 'eigrpnetwork', detail=False)),
    ),
    path(
        'eigrp/network/<int:pk>/',
        include(get_model_urls('netbox_routing', 'eigrpnetwork')),
    ),
    path(
        'eigrp/interface/',
        include(get_model_urls('netbox_routing', 'eigrpinterface', detail=False)),
    ),
    path(
        'eigrp/interface/<int:pk>/',
        include(get_model_urls('netbox_routing', 'eigrpinterface')),
    ),
    path(
        'bgp/router/',
        include(get_model_urls('netbox_routing', 'bgprouter', detail=False)),
    ),
    path(
        'bgp/router/<int:pk>/', include(get_model_urls('netbox_routing', 'bgprouter'))
    ),
    path(
        'bgp/scope/',
        include(get_model_urls('netbox_routing', 'bgpscope', detail=False)),
    ),
    path('bgp/scope/<int:pk>/', include(get_model_urls('netbox_routing', 'bgpscope'))),
    path(
        'bgp/address-family/',
        include(get_model_urls('netbox_routing', 'bgpaddressfamily', detail=False)),
    ),
    path(
        'bgp/address-family/<int:pk>/',
        include(get_model_urls('netbox_routing', 'bgpaddressfamily')),
    ),
    path(
        'prefix-list/',
        include(get_model_urls('netbox_routing', 'prefixlist', detail=False)),
    ),
    path(
        'prefix-list/<int:pk>/', include(get_model_urls('netbox_routing', 'prefixlist'))
    ),
    path(
        'prefix-list-entry/',
        include(get_model_urls('netbox_routing', 'prefixlistentry', detail=False)),
    ),
    path(
        'prefix-list-entry/<int:pk>/',
        include(get_model_urls('netbox_routing', 'prefixlistentry')),
    ),
    path(
        'route-map/',
        include(get_model_urls('netbox_routing', 'routemap', detail=False)),
    ),
    path('route-map/<int:pk>/', include(get_model_urls('netbox_routing', 'routemap'))),
    path(
        'route-map-entry/',
        include(get_model_urls('netbox_routing', 'routemapentry', detail=False)),
    ),
    path(
        'route-map-entry/<int:pk>/',
        include(get_model_urls('netbox_routing', 'routemapentry')),
    ),
]
