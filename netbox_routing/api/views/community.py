from netbox.api.viewsets import NetBoxModelViewSet
from netbox_routing import filtersets
from netbox_routing.api._serializers.community import *
from netbox_routing.models.community import *


__all__ = (
    'CommunityListViewSet',
    'CommunityViewSet',
    'CommunityListEntryViewSet',
)


class CommunityListViewSet(NetBoxModelViewSet):
    queryset = CommunityList.objects.all()
    serializer_class = CommunityListSerializer
    filterset_class = filtersets.CommunityListFilterSet


class CommunityViewSet(NetBoxModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    filterset_class = filtersets.CommunityFilterSet


class CommunityListEntryViewSet(NetBoxModelViewSet):
    queryset = CommunityListEntry.objects.all()
    serializer_class = CommunityListEntrySerializer
    filterset_class = filtersets.CommunityListEntryFilterSet
