from netbox.api.routers import NetBoxRouter
from .views import StaticRouteViewSet, PrefixListViewSet, RouteMapViewSet, PrefixListEntryViewSet, RouteMapEntryViewSet

router = NetBoxRouter()
router.register('staticroute', StaticRouteViewSet)
router.register('prefix-list', PrefixListViewSet)
router.register('prefix-list-entry', PrefixListEntryViewSet)
router.register('route-map', RouteMapViewSet)
router.register('route-map-entry', RouteMapEntryViewSet)
urlpatterns = router.urls
