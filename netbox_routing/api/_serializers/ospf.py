from rest_framework import serializers

from dcim.api.serializers_.device_components import InterfaceSerializer
from dcim.api.serializers_.devices import DeviceSerializer
from ipam.api.serializers_.vrfs import VRFSerializer
from netbox.api.serializers import NetBoxModelSerializer
from netbox_routing.models import OSPFInstance, OSPFArea, OSPFInterface


__all__ = (
    'OSPFInstanceSerializer',
    'OSPFAreaSerializer',
    'OSPFInterfaceSerializer',
)


class OSPFInstanceSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:ospfinstance-detail')
    device = DeviceSerializer(nested=True)
    vrf = VRFSerializer(nested=True)

    class Meta:
        model = OSPFInstance
        fields = (
            'url', 'id', 'display', 'name', 'router_id', 'process_id', 'device', 'vrf', 'description', 'comments',
        )
        brief_fields = ('url', 'id', 'display', 'name', 'router_id', 'process_id', 'device', 'vrf', )


class OSPFAreaSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:ospfarea-detail')

    class Meta:
        model = OSPFArea
        fields = ('url', 'id', 'display', 'area_id', 'description', 'comments',)
        brief_fields = ('url', 'id', 'display', 'area_id',)


class OSPFInterfaceSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:ospfarea-detail')
    instance = OSPFInstanceSerializer(nested=True)
    area = OSPFAreaSerializer(nested=True)
    interface = InterfaceSerializer(nested=True)

    class Meta:
        model = OSPFInterface
        fields = (
            'url', 'id', 'display', 'instance', 'area', 'interface', 'passive', 'priority', 'bfd', 'authentication',
            'passphrase', 'description', 'comments',
        )
        brief_fields = (
            'url', 'id', 'display', 'instance', 'area', 'interface', 'passive',
        )
