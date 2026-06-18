# SPDX-License-Identifier: Apache-2.0

from django.contrib.contenttypes.prefetch import GenericPrefetch

from netbox.api.viewsets import NetBoxModelViewSet

from netbox_routing import filtersets
from netbox_routing.api.serializers import (
    ISISInstanceSerializer,
    ISISInterfaceSerializer,
    ISISSettingSerializer,
    ISISLevelSerializer,
    ISISInterfaceLevelSerializer,
    ISISSegmentRoutingSerializer,
    ISISFlexAlgoSerializer,
)
from netbox_routing.models import (
    ISISInstance,
    ISISInterface,
    ISISSetting,
    ISISLevel,
    ISISInterfaceLevel,
    ISISSegmentRouting,
    ISISFlexAlgo,
)

__all__ = (
    'ISISInstanceViewSet',
    'ISISInterfaceViewSet',
    'ISISSettingViewSet',
    'ISISLevelViewSet',
    'ISISInterfaceLevelViewSet',
    'ISISSegmentRoutingViewSet',
    'ISISFlexAlgoViewSet',
)


class ISISFlexAlgoViewSet(NetBoxModelViewSet):
    # display renders str(self) -> str(instance) -> instance.device, so pull the
    # whole chain in one join to keep the list view query count flat.
    queryset = ISISFlexAlgo.objects.select_related('instance__device')
    serializer_class = ISISFlexAlgoSerializer
    filterset_class = filtersets.ISISFlexAlgoFilterSet


class ISISSettingViewSet(NetBoxModelViewSet):
    # The serializer renders assigned_object (a GenericForeignKey); without a
    # GenericPrefetch each row would fetch its target separately (N+1).
    queryset = ISISSetting.objects.prefetch_related(
        GenericPrefetch(
            'assigned_object',
            [
                ISISInstance.objects.select_related('device', 'vrf'),
                ISISInterface.objects.select_related('instance__device', 'instance__vrf', 'interface'),
            ],
        )
    )
    serializer_class = ISISSettingSerializer
    filterset_class = filtersets.ISISSettingFilterSet


class ISISLevelViewSet(NetBoxModelViewSet):
    # str(self) -> str(instance) -> instance.device
    queryset = ISISLevel.objects.select_related('instance__device')
    serializer_class = ISISLevelSerializer
    filterset_class = filtersets.ISISLevelFilterSet


class ISISInterfaceLevelViewSet(NetBoxModelViewSet):
    # str(self) -> str(ISISInterface) -> ISISInterface.interface (dcim Interface)
    queryset = ISISInterfaceLevel.objects.select_related('interface__interface')
    serializer_class = ISISInterfaceLevelSerializer
    filterset_class = filtersets.ISISInterfaceLevelFilterSet


class ISISSegmentRoutingViewSet(NetBoxModelViewSet):
    # str(self) -> str(instance) -> instance.device
    queryset = ISISSegmentRouting.objects.select_related('instance__device')
    serializer_class = ISISSegmentRoutingSerializer
    filterset_class = filtersets.ISISSegmentRoutingFilterSet


class ISISInstanceViewSet(NetBoxModelViewSet):
    queryset = ISISInstance.objects.select_related('device', 'vrf')
    serializer_class = ISISInstanceSerializer
    filterset_class = filtersets.ISISInstanceFilterSet


class ISISInterfaceViewSet(NetBoxModelViewSet):
    queryset = ISISInterface.objects.select_related('instance__device', 'instance__vrf', 'interface')
    serializer_class = ISISInterfaceSerializer
    filterset_class = filtersets.ISISInterfaceFilterSet
