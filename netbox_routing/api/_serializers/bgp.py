from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from dcim.api.serializers_.devices import DeviceSerializer
from ipam.api.serializers_.asns import ASNSerializer
from ipam.api.serializers_.vrfs import VRFSerializer
from netbox.api.serializers import NetBoxModelSerializer
from utilities.api import get_serializer_for_model

from netbox_routing.models import BGPRouter, BGPSetting, BGPScope, BGPAddressFamily

__all__ = (
    'BGPRouterSerializer',
    'BGPScopeSerializer',
    'BGPAddressFamilySerializer',
    'BGPSettingSerializer',
)




class BGPSettingSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:bgprouter-detail')

    assigned_object = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BGPSetting
        fields = (
            'url', 'id', 'display', 'assigned_object_type', 'assigned_object_id', 'assigned_object', 'key', 'value',
            'description', 'comments',
        )
        brief_fields = ('url', 'id', 'display', 'assigned_object', 'key', )

    @extend_schema_field(serializers.JSONField(allow_null=True))
    def get_assigned_object(self, obj):
        if obj.assigned_object is None:
            return None
        serializer = get_serializer_for_model(obj.assigned_object)
        context = {'request': self.context['request']}
        return serializer(obj.assigned_object, context=context, nested=True).data


class BGPRouterSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:bgprouter-detail')

    device = DeviceSerializer(nested=True)
    asn = ASNSerializer(nested=True)

    settings = BGPSettingSerializer(many=True)

    class Meta:
        model = BGPRouter
        fields = ('url', 'id', 'display', 'device', 'asn', 'settings', 'description', 'comments',)
        brief_fields = ('url', 'id', 'display', 'device', 'asn', )


class BGPScopeSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:bgpscope-detail')

    router = BGPRouterSerializer(nested=True)
    vrf = VRFSerializer(nested=True)

    settings = BGPSettingSerializer(many=True)

    class Meta:
        model = BGPScope
        fields = ('url', 'id', 'display', 'router', 'vrf', 'settings', 'description', 'comments',)
        brief_fields = ('url', 'id', 'display', 'router', 'vrf', )


class BGPAddressFamilySerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:bgpaddressfamily-detail')

    scope = BGPScopeSerializer(nested=True)
    settings = BGPSettingSerializer(many=True)

    class Meta:
        model = BGPAddressFamily
        fields = ('url', 'id', 'display', 'scope', 'address_family', 'settings', 'description', 'comments',)
        brief_fields = ('url', 'id', 'display', 'scope', 'address_family', )
