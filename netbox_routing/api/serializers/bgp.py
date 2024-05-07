from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from dcim.api.nested_serializers import NestedDeviceSerializer
from ipam.api.nested_serializers import NestedASNSerializer, NestedVRFSerializer
from netbox.api.serializers import NetBoxModelSerializer
from netbox.constants import NESTED_SERIALIZER_PREFIX
from netbox_routing.api.nested_serializers.bgp import NestedBGPSettingSerializer, NestedBGPRouterSerializer, \
    NestedBGPScopeSerializer

from netbox_routing.models import BGPRouter, BGPSetting, BGPScope, BGPAddressFamily

__all__ = (
    'BGPRouterSerializer',
    'BGPScopeSerializer',
    'BGPAddressFamilySerializer',
    'BGPSettingSerializer',
)


from utilities.api import get_serializer_for_model


class BGPRouterSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:bgprouter-detail')

    device = NestedDeviceSerializer()
    asn = NestedASNSerializer()

    settings = NestedBGPSettingSerializer(many=True)

    class Meta:
        model = BGPRouter
        fields = ('url', 'id', 'display', 'device', 'asn', 'settings')


class BGPScopeSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:bgpscope-detail')

    router = NestedBGPRouterSerializer()
    vrf = NestedVRFSerializer()

    settings = NestedBGPSettingSerializer(many=True)

    class Meta:
        model = BGPScope
        fields = ('url', 'id', 'display', 'router', 'vrf', 'settings')


class BGPAddressFamilySerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:bgpaddressfamily-detail')

    scope = NestedBGPScopeSerializer()

    settings = NestedBGPSettingSerializer(many=True)

    class Meta:
        model = BGPAddressFamily
        fields = ('url', 'id', 'display', 'scope', 'address_family', 'settings')


class BGPSettingSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:bgprouter-detail')

    assigned_object = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BGPSetting
        fields = (
            'url', 'id', 'display', 'assigned_object_type', 'assigned_object_id', 'assigned_object', 'key', 'value'
        )

    @extend_schema_field(serializers.JSONField(allow_null=True))
    def get_assigned_object(self, obj):
        if obj.assigned_object is None:
            return None
        serializer = get_serializer_for_model(obj.assigned_object, prefix=NESTED_SERIALIZER_PREFIX)
        context = {'request': self.context['request']}
        return serializer(obj.assigned_object, context=context).data
