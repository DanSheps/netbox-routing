from netbox.api.routers import NetBoxRouter
from .views import StaticRouteViewSet, PrefixListViewSet, RouteMapViewSet, PrefixListEntryViewSet, \
    RouteMapEntryViewSet, OSPFInstanceViewSet, OSPFAreaViewSet, OSPFInterfaceViewSet

router = NetBoxRouter()
router.register('staticroute', StaticRouteViewSet)
router.register('ospf-instance', OSPFInstanceViewSet)
router.register('ospf-area', OSPFAreaViewSet)
router.register('ospf-interface', OSPFInterfaceViewSet)
router.register('prefix-list', PrefixListViewSet)
router.register('prefix-list-entry', PrefixListEntryViewSet)
router.register('route-map', RouteMapViewSet)
router.register('route-map-entry', RouteMapEntryViewSet)
urlpatterns = router.urls
