from rest_framework import serializers

from dcim.api.serializers_.devices import DeviceSerializer
from ipam.api.serializers_.vrfs import VRFSerializer
from netbox.api.serializers import NetBoxModelSerializer

from netbox_routing.api.field_serializers import IPAddressField
from netbox_routing.models import StaticRoute


__all__ = (
    'StaticRouteSerializer'
)


class StaticRouteSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:staticroute-detail')
    devices = DeviceSerializer(many=True, nested=True, required=False, allow_null=True)
    vrf = VRFSerializer(nested=True, required=False, allow_null=True)
    next_hop = IPAddressField()

    class Meta:
        model = StaticRoute
        fields = (
            'url', 'id', 'display', 'devices', 'vrf', 'prefix', 'next_hop', 'name', 'metric', 'permanent',
            'description', 'comments'
        )
        brief_fields = ('url', 'id', 'display', 'name', 'prefix', 'next_hop', 'description')

    def create(self, validated_data):
        devices = validated_data.pop('devices', None)
        instance = super(StaticRouteSerializer, self).create(validated_data)
        
        return self._update_devices(instance, devices)
    
    def update(self, instance, validated_data):
        devices = validated_data.pop('devices', None)
        instance = super(StaticRouteSerializer, self).update(instance, validated_data)
        
        return self._update_devices(instance, devices)
    
    def _update_devices(self, instance: StaticRoute, devices: object) -> StaticRoute:
        if devices:
            instance.devices.set(devices)
        elif devices is not None:
            instance.devices.clear()
        
        return instance
        
