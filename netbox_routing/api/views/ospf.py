from netbox.api.viewsets import NetBoxModelViewSet
from netbox_routing import filtersets
from netbox_routing.api.serializers import OSPFInstanceSerializer, OSPFAreaSerializer, OSPFInterfaceSerializer
from netbox_routing.models import OSPFInstance, OSPFArea, OSPFInterface


__all__ = (
    'OSPFInstanceViewSet',
    'OSPFAreaViewSet',
    'OSPFInterfaceViewSet',
)


class OSPFInstanceViewSet(NetBoxModelViewSet):
    queryset = OSPFInstance.objects.all()
    serializer_class = OSPFInstanceSerializer
    filterset_class = filtersets.OSPFInstanceFilterSet


class OSPFAreaViewSet(NetBoxModelViewSet):
    queryset = OSPFArea.objects.all()
    serializer_class = OSPFAreaSerializer
    filterset_class = filtersets.OSPFAreaFilterSet


class OSPFInterfaceViewSet(NetBoxModelViewSet):
    queryset = OSPFInterface.objects.all()
    serializer_class = OSPFInterfaceSerializer
    filterset_class = filtersets.OSPFInterfaceFilterSet
