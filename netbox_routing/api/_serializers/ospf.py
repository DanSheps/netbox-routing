from rest_framework import serializers

from dcim.api.serializers_.device_components import InterfaceSerializer
from dcim.api.serializers_.devices import DeviceSerializer
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

    class Meta:
        model = OSPFInstance
        fields = ('url', 'id', 'display', 'name', 'router_id', 'process_id', 'device')


class OSPFAreaSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:ospfarea-detail')

    class Meta:
        model = OSPFArea
        fields = ('url', 'id', 'display', 'area_id')


class OSPFInterfaceSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:ospfarea-detail')
    instance = OSPFInstanceSerializer(nested=True)
    area = OSPFAreaSerializer(nested=True)
    interface = InterfaceSerializer(nested=True)

    class Meta:
        model = OSPFInterface
        fields = (
            'url', 'id', 'display', 'instance', 'area', 'interface', 'priority', 'bfd', 'authentication', 'passphrase'
        )
