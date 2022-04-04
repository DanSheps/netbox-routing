from netbox.api.viewsets import ModelViewSet
from netbox_routing.api.serializers import PrefixListSerializer, PrefixListEntrySerializer, RouteMapSerializer, \
    RouteMapEntrySerializer
from netbox_routing.models import PrefixList, PrefixListEntry, RouteMap, RouteMapEntry


class PrefixListViewSet(ModelViewSet):
    queryset = PrefixList.objects.all()
    serializer_class = PrefixListSerializer


class PrefixListEntryViewSet(ModelViewSet):
    queryset = PrefixListEntry.objects.all()
    serializer_class = PrefixListEntrySerializer


class RouteMapViewSet(ModelViewSet):
    queryset = RouteMap.objects.all()
    serializer_class = RouteMapSerializer


class RouteMapEntryViewSet(ModelViewSet):
    queryset = RouteMapEntry.objects.all()
    serializer_class = RouteMapEntrySerializer
