from netbox.api.viewsets import NetBoxModelViewSet
from netbox_routing import filtersets
from netbox_routing.api.serializers import BGPRouterSerializer, BGPSettingSerializer, BGPScopeSerializer, \
    BGPAddressFamilySerializer
from netbox_routing.models import BGPRouter, BGPSetting, BGPScope, BGPAddressFamily

__all__ = (
    'BGPRouterViewSet',
    'BGPScopeViewSet',
    'BGPAddressFamilyViewSet',
    'BGPSettingViewSet',
)


class BGPRouterViewSet(NetBoxModelViewSet):
    queryset = BGPRouter.objects.all()
    serializer_class = BGPRouterSerializer
    filterset_class = filtersets.BGPRouterFilterSet


class BGPScopeViewSet(NetBoxModelViewSet):
    queryset = BGPScope.objects.all()
    serializer_class = BGPScopeSerializer
    filterset_class = filtersets.BGPScopeFilterSet


class BGPAddressFamilyViewSet(NetBoxModelViewSet):
    queryset = BGPAddressFamily.objects.all()
    serializer_class = BGPAddressFamilySerializer
    filterset_class = filtersets.BGPAddressFamilyFilterSet


class BGPSettingViewSet(NetBoxModelViewSet):
    queryset = BGPSetting.objects.all()
    serializer_class = BGPSettingSerializer
    filterset_class = filtersets.BGPSettingFilterSet
