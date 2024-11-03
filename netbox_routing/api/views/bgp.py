from netbox.api.viewsets import NetBoxModelViewSet
from netbox_routing import filtersets
from netbox_routing.api._serializers.bgp import *
from netbox_routing.models.bgp import *

__all__ = (
    'BGPRouterViewSet',
    'BGPScopeViewSet',
    'BGPSessionTemplateViewSet',
    'BGPPolicyTemplateViewSet',
    'BGPPeerTemplateViewSet',
    'BGPAddressFamilyViewSet',
    'BGPPeerViewSet',
    'BGPPeerAddressFamilyViewSet',
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


class BGPSessionTemplateViewSet(NetBoxModelViewSet):
    queryset = BGPSessionTemplate.objects.all()
    serializer_class = BGPSessionTemplateSerializer
    filterset_class = filtersets.BGPSessionTemplateFilterSet


class BGPPolicyTemplateViewSet(NetBoxModelViewSet):
    queryset = BGPPolicyTemplate.objects.all()
    serializer_class = BGPPolicyTemplateSerializer
    filterset_class = filtersets.BGPPolicyTemplateFilterSet


class BGPAddressFamilyViewSet(NetBoxModelViewSet):
    queryset = BGPAddressFamily.objects.all()
    serializer_class = BGPAddressFamilySerializer
    filterset_class = filtersets.BGPAddressFamilyFilterSet


class BGPPeerTemplateViewSet(NetBoxModelViewSet):
    queryset = BGPPeerTemplate.objects.all()
    serializer_class = BGPPeerTemplateSerializer
    filterset_class = filtersets.BGPPeerTemplateFilterSet


class BGPPeerViewSet(NetBoxModelViewSet):
    queryset = BGPPeer.objects.all()
    serializer_class = BGPPeerSerializer
    filterset_class = filtersets.BGPPeerFilterSet


class BGPPeerAddressFamilyViewSet(NetBoxModelViewSet):
    queryset = BGPPeerAddressFamily.objects.all()
    serializer_class = BGPPeerAddressFamilySerializer
    filterset_class = filtersets.BGPPeerAddressFamilyFilterSet


class BGPSettingViewSet(NetBoxModelViewSet):
    queryset = BGPSetting.objects.all()
    serializer_class = BGPSettingSerializer
    filterset_class = filtersets.BGPSettingFilterSet
