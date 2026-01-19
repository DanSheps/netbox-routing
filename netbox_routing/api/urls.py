from netbox.api.routers import NetBoxRouter
from .views import *

router = NetBoxRouter()
router.register('static/route', StaticRouteViewSet)
router.register('bgp/setting', BGPSettingViewSet)
router.register('bgp/router', BGPRouterViewSet)
router.register('bgp/scope', BGPScopeViewSet)
router.register('bgp/address-family', BGPAddressFamilyViewSet)
router.register('bgp/peer', BGPPeerViewSet)
router.register('bgp/peer-group', BGPPeerTemplateViewSet)
router.register('bgp/peer-address-family', BGPPeerAddressFamilyViewSet)
router.register('ospf/instance', OSPFInstanceViewSet)
router.register('ospf/area', OSPFAreaViewSet)
router.register('ospf/interface', OSPFInterfaceViewSet)
router.register('eigrp/router', EIGRPRouterViewSet)
router.register('eigrp/address-family', EIGRPAddressFamilyViewSet)
router.register('eigrp/network', EIGRPNetworkViewSet)
router.register('eigrp/interface', EIGRPInterfaceViewSet)
router.register('objects/prefix-list', PrefixListViewSet)
router.register('objects/prefix-list-entry', PrefixListEntryViewSet)
router.register('objects/route-map', RouteMapViewSet)
router.register('objects/route-map-entry', RouteMapEntryViewSet)
urlpatterns = router.urls
