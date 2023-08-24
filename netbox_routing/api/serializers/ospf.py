from rest_framework import serializers

from dcim.api.nested_serializers import NestedInterfaceSerializer, NestedDeviceSerializer
from netbox.api.serializers import NetBoxModelSerializer
from netbox_routing.api.nested_serializers.ospf import NestedOSPFInstanceSerializer, NestedOSPFAreaSerializer
from netbox_routing.models import OSPFInstance, OSPFArea, OSPFInterface


__all__ = (
    'OSPFInstanceSerializer',
    'OSPFAreaSerializer',
    'OSPFInterfaceSerializer',
)


class OSPFInstanceSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:ospfinstance-detail')
    device = NestedDeviceSerializer()

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
    instance = NestedOSPFInstanceSerializer()
    area = NestedOSPFAreaSerializer()
    interface = NestedInterfaceSerializer()

    class Meta:
        model = OSPFInterface
        fields = (
            'url', 'id', 'display', 'instance', 'area', 'interface', 'priority', 'bfd', 'authentication', 'passphrase'
        )
