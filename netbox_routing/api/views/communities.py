
from netbox.api.viewsets import NetBoxModelViewSet
from netbox_routing import filtersets
from netbox_routing.api._serializers.communities import *
from netbox_routing.models.communities import *


__all__ = (
    'CommunityListViewSet',
    'CommunityViewSet',
)


class CommunityListViewSet(NetBoxModelViewSet):
    queryset = CommunityList.objects.all()
    serializer_class = CommunityListSerializer
    filterset_class = filtersets.CommunityListFilterSet


class CommunityViewSet(NetBoxModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    filterset_class = filtersets.CommunityFilterSet
