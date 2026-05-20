from django.urls import path, include

from utilities.urls import get_model_urls

from . import views  # noqa F401

app_name = 'netbox_routing'

urlpatterns = [
    path(
        'routes/static/', include(get_model_urls(app_name, 'staticroute', detail=False))
    ),
    path('routes/static/<int:pk>/', include(get_model_urls(app_name, 'staticroute'))),
    # OSPF
    path(
        'ospf/instance/',
        include(get_model_urls(app_name, 'ospfinstance', detail=False)),
    ),
    path('ospf/instance/<int:pk>/', include(get_model_urls(app_name, 'ospfinstance'))),
    path('ospf/area/', include(get_model_urls(app_name, 'ospfarea', detail=False))),
    path('ospf/area/<int:pk>/', include(get_model_urls(app_name, 'ospfarea'))),
    path(
        'ospf/interface/',
        include(get_model_urls(app_name, 'ospfinterface', detail=False)),
    ),
    path(
        'ospf/interface/<int:pk>/', include(get_model_urls(app_name, 'ospfinterface'))
    ),
    # EIGRP
    path(
        'eigrp/router/', include(get_model_urls(app_name, 'eigrprouter', detail=False))
    ),
    path('eigrp/router/<int:pk>/', include(get_model_urls(app_name, 'eigrprouter'))),
    path(
        'eigrp/address-family/',
        include(get_model_urls(app_name, 'eigrpaddressfamily', detail=False)),
    ),
    path(
        'eigrp/address-family/<int:pk>/',
        include(get_model_urls(app_name, 'eigrpaddressfamily')),
    ),
    path(
        'eigrp/network/',
        include(get_model_urls(app_name, 'eigrpnetwork', detail=False)),
    ),
    path('eigrp/network/<int:pk>/', include(get_model_urls(app_name, 'eigrpnetwork'))),
    path(
        'eigrp/interface/',
        include(get_model_urls(app_name, 'eigrpinterface', detail=False)),
    ),
    path(
        'eigrp/interface/<int:pk>/', include(get_model_urls(app_name, 'eigrpinterface'))
    ),
    # BFD
    path('bfd/profile/', include(get_model_urls(app_name, 'bfdprofile', detail=False))),
    path('bfd/profile/<int:pk>/', include(get_model_urls(app_name, 'bfdprofile'))),
    # BGP
    path('bgp/setting/', include(get_model_urls(app_name, 'bgpsetting', detail=False))),
    path('bgp/setting/<int:pk>/', include(get_model_urls(app_name, 'bgpsetting'))),
    path(
        'bgp/peer-template/',
        include(get_model_urls(app_name, 'bgppeertemplate', detail=False)),
    ),
    path(
        'bgp/peer-template/<int:pk>/',
        include(get_model_urls(app_name, 'bgppeertemplate')),
    ),
    path(
        'bgp/policy-template/',
        include(get_model_urls(app_name, 'bgppolicytemplate', detail=False)),
    ),
    path(
        'bgp/policy-template/<int:pk>/',
        include(get_model_urls(app_name, 'bgppolicytemplate')),
    ),
    path(
        'bgp/session-template/',
        include(get_model_urls(app_name, 'bgpsessiontemplate', detail=False)),
    ),
    path(
        'bgp/session-template/<int:pk>/',
        include(get_model_urls(app_name, 'bgpsessiontemplate')),
    ),
    path('bgp/router/', include(get_model_urls(app_name, 'bgprouter', detail=False))),
    path('bgp/router/<int:pk>/', include(get_model_urls(app_name, 'bgprouter'))),
    path('bgp/scope/', include(get_model_urls(app_name, 'bgpscope', detail=False))),
    path('bgp/scope/<int:pk>/', include(get_model_urls(app_name, 'bgpscope'))),
    path('bgp/scope/', include(get_model_urls(app_name, 'bgpscope', detail=False))),
    path('bgp/scope/<int:pk>/', include(get_model_urls(app_name, 'bgpscope'))),
    path(
        'bgp/address-family/',
        include(get_model_urls(app_name, 'bgpaddressfamily', detail=False)),
    ),
    path(
        'bgp/address-family/<int:pk>/',
        include(get_model_urls(app_name, 'bgpaddressfamily')),
    ),
    path('bgp/peer/', include(get_model_urls(app_name, 'bgppeer', detail=False))),
    path('bgp/peer/<int:pk>/', include(get_model_urls(app_name, 'bgppeer'))),
    path(
        'bgp/peer-address-family/',
        include(get_model_urls(app_name, 'bgppeeraddressfamily', detail=False)),
    ),
    path(
        'bgp/peer-address-family/<int:pk>/',
        include(get_model_urls(app_name, 'bgppeeraddressfamily')),
    ),
    # Objects: Community
    path(
        'objects/community-list/',
        include(get_model_urls(app_name, 'communitylist', detail=False)),
    ),
    path(
        'objects/community-list/<int:pk>/',
        include(get_model_urls(app_name, 'communitylist')),
    ),
    path(
        'objects/community/',
        include(get_model_urls(app_name, 'community', detail=False)),
    ),
    path('objects/community/<int:pk>/', include(get_model_urls(app_name, 'community'))),
    path(
        'objects/community-list-entry/',
        include(get_model_urls(app_name, 'communitylistentry', detail=False)),
    ),
    path(
        'objects/community-list-entry/<int:pk>/',
        include(get_model_urls(app_name, 'communitylistentry')),
    ),
    # Objects: Custom Prefix
    path(
        'objects/custom-prefix/',
        include(get_model_urls(app_name, 'customprefix', detail=False)),
    ),
    path(
        'objects/custom-prefix/<int:pk>/',
        include(get_model_urls(app_name, 'customprefix')),
    ),
    # Objects: Prefix List
    path(
        'objects/prefix-list/',
        include(get_model_urls(app_name, 'prefixlist', detail=False)),
    ),
    path(
        'objects/prefix-list/<int:pk>/', include(get_model_urls(app_name, 'prefixlist'))
    ),
    path(
        'objects/prefix-list-entry/',
        include(get_model_urls(app_name, 'prefixlistentry', detail=False)),
    ),
    path(
        'objects/prefix-list-entry/<int:pk>/',
        include(get_model_urls(app_name, 'prefixlistentry')),
    ),
    # Objects: Route Map
    path(
        'objects/route-map/',
        include(get_model_urls(app_name, 'routemap', detail=False)),
    ),
    path('objects/route-map/<int:pk>/', include(get_model_urls(app_name, 'routemap'))),
    path(
        'objects/route-map-entry/',
        include(get_model_urls(app_name, 'routemapentry', detail=False)),
    ),
    path(
        'objects/route-map-entry/<int:pk>/',
        include(get_model_urls(app_name, 'routemapentry')),
    ),
    # Objects: AS Path
    path(
        'objects/as-path/',
        include(get_model_urls(app_name, 'aspath', detail=False)),
    ),
    path('objects/as-path/<int:pk>/', include(get_model_urls(app_name, 'aspath'))),
    path(
        'objects/as-path-entry/',
        include(get_model_urls(app_name, 'aspathentry', detail=False)),
    ),
    path(
        'objects/as-path-entry/<int:pk>/',
        include(get_model_urls(app_name, 'aspathentry')),
    ),
]
