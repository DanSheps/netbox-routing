from netbox.api.viewsets import NetBoxModelViewSet
from netbox_routing.api.serializers import PrefixListSerializer, PrefixListEntrySerializer, RouteMapSerializer, \
    RouteMapEntrySerializer
from netbox_routing.models import PrefixList, PrefixListEntry, RouteMap, RouteMapEntry


class PrefixListViewSet(NetBoxModelViewSet):
    queryset = PrefixList.objects.all()
    serializer_class = PrefixListSerializer


class PrefixListEntryViewSet(NetBoxModelViewSet):
    queryset = PrefixListEntry.objects.all()
    serializer_class = PrefixListEntrySerializer


class RouteMapViewSet(NetBoxModelViewSet):
    queryset = RouteMap.objects.all()
    serializer_class = RouteMapSerializer


class RouteMapEntryViewSet(NetBoxModelViewSet):
    queryset = RouteMapEntry.objects.all()
    serializer_class = RouteMapEntrySerializer
