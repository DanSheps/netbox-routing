from netbox.api.viewsets import NetBoxModelViewSet
from netbox_routing import filtersets
from netbox_routing.api.serializers import PrefixListSerializer, PrefixListEntrySerializer, RouteMapSerializer, \
    RouteMapEntrySerializer
from netbox_routing.models import PrefixList, PrefixListEntry, RouteMap, RouteMapEntry


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
