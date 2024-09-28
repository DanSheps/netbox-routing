from netbox.api.viewsets import NetBoxModelViewSet
from netbox_routing import filtersets
from netbox_routing.api.serializers import (
    EIGRPRouterSerializer, EIGRPRouterSerializer, EIGRPAddressFamilySerializer,
    EIGRPInterfaceSerializer, EIGRPNetworkSerializer
)
from netbox_routing.models import (
    EIGRPRouter, EIGRPAddressFamily, EIGRPNetwork, EIGRPInterface
)


__all__ = (
    'EIGRPRouterViewSet',
    'EIGRPAddressFamilyViewSet',
    'EIGRPNetworkViewSet',
    'EIGRPInterfaceViewSet',
)


class EIGRPRouterViewSet(NetBoxModelViewSet):
    queryset = EIGRPRouter.objects.all()
    serializer_class = EIGRPRouterSerializer
    filterset_class = filtersets.EIGRPRouterFilterSet


class EIGRPAddressFamilyViewSet(NetBoxModelViewSet):
    queryset = EIGRPAddressFamily.objects.all()
    serializer_class = EIGRPAddressFamilySerializer
    filterset_class = filtersets.EIGRPAddressFamilyFilterSet


class EIGRPNetworkViewSet(NetBoxModelViewSet):
    queryset = EIGRPNetwork.objects.all()
    serializer_class = EIGRPNetworkSerializer
    filterset_class = filtersets.EIGRPNetworkFilterSet


class EIGRPInterfaceViewSet(NetBoxModelViewSet):
    queryset = EIGRPInterface.objects.all()
    serializer_class = EIGRPInterfaceSerializer
    filterset_class = filtersets.EIGRPInterfaceFilterSet
