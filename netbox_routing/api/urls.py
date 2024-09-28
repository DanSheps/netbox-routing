from netbox.api.routers import NetBoxRouter
from .views import StaticRouteViewSet, PrefixListViewSet, RouteMapViewSet, PrefixListEntryViewSet, \
    RouteMapEntryViewSet, OSPFInstanceViewSet, OSPFAreaViewSet, OSPFInterfaceViewSet, BGPRouterViewSet, \
    BGPScopeViewSet, BGPAddressFamilyViewSet, BGPSettingViewSet, EIGRPRouterViewSet, EIGRPAddressFamilyViewSet, \
    EIGRPNetworkViewSet, EIGRPInterfaceViewSet

router = NetBoxRouter()
router.register('staticroute', StaticRouteViewSet)
router.register('bgp-router', BGPRouterViewSet)
router.register('bgp-scope', BGPScopeViewSet)
router.register('bgp-addressfamily', BGPAddressFamilyViewSet)
router.register('bgp-setting', BGPSettingViewSet)
router.register('ospf-instance', OSPFInstanceViewSet)
router.register('ospf-area', OSPFAreaViewSet)
router.register('ospf-interface', OSPFInterfaceViewSet)
router.register('eigrp-router', EIGRPRouterViewSet)
router.register('eigrp-address-family', EIGRPAddressFamilyViewSet)
router.register('eigrp-network', EIGRPNetworkViewSet)
router.register('eigrp-interface', EIGRPInterfaceViewSet)
router.register('prefix-list', PrefixListViewSet)
router.register('prefix-list-entry', PrefixListEntryViewSet)
router.register('route-map', RouteMapViewSet)
router.register('route-map-entry', RouteMapEntryViewSet)
urlpatterns = router.urls
