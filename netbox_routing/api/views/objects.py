from netbox.api.viewsets import NetBoxModelViewSet
from netbox_routing import filtersets
from netbox_routing.api._serializers.objects import *
from netbox_routing.models.objects import *

__all__ = (
    'PrefixListViewSet',
    'PrefixListEntryViewSet',
    'RouteMapViewSet',
    'RouteMapEntryViewSet',
    'ASPathViewSet',
    'ASPathEntryViewSet',
)


class PrefixListViewSet(NetBoxModelViewSet):
    queryset = PrefixList.objects.all()
    serializer_class = PrefixListSerializer
    filterset_class = filtersets.PrefixListFilterSet


class PrefixListEntryViewSet(NetBoxModelViewSet):
    queryset = PrefixListEntry.objects.all()
    serializer_class = PrefixListEntrySerializer
    filterset_class = filtersets.PrefixListEntryFilterSet


class RouteMapViewSet(NetBoxModelViewSet):
    queryset = RouteMap.objects.all()
    serializer_class = RouteMapSerializer
    filterset_class = filtersets.RouteMapFilterSet


class RouteMapEntryViewSet(NetBoxModelViewSet):
    queryset = RouteMapEntry.objects.all()
    serializer_class = RouteMapEntrySerializer
    filterset_class = filtersets.RouteMapEntryFilterSet


class ASPathViewSet(NetBoxModelViewSet):
    queryset = ASPath.objects.all()
    serializer_class = ASPathSerializer
    filterset_class = filtersets.ASPathFilterSet


class ASPathEntryViewSet(NetBoxModelViewSet):
    queryset = ASPathEntry.objects.all()
    serializer_class = ASPathEntrySerializer
    filterset_class = filtersets.ASPathEntryFilterSet
