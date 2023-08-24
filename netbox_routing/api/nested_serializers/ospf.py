from rest_framework import serializers

from dcim.api.nested_serializers import NestedInterfaceSerializer
from netbox.api.serializers import WritableNestedSerializer
from netbox_routing.models import OSPFInstance, OSPFArea, OSPFInterface


__all__ = (
    'NestedOSPFInstanceSerializer',
    'NestedOSPFAreaSerializer',
    'NestedOSPFInterfaceSerializer',
)


class NestedOSPFInstanceSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:ospfinstance-detail')

    class Meta:
        model = OSPFInstance
        fields = ('url', 'id', 'display', 'name', 'router_id', 'process_id')


class NestedOSPFAreaSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:ospfarea-detail')

    class Meta:
        model = OSPFArea
        fields = ('url', 'id', 'display', 'area_id')


class NestedOSPFInterfaceSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:ospfarea-detail')
    instance = NestedOSPFInstanceSerializer()
    area = NestedOSPFAreaSerializer()
    interface = NestedInterfaceSerializer()

    class Meta:
        model = OSPFInterface
        fields = ('url', 'id', 'display', 'instance', 'area', 'interface')
