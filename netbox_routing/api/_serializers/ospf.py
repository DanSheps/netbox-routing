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
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:ospfinstance-detail'
    )
    device = DeviceSerializer(nested=True)
    vrf = VRFSerializer(nested=True, required=False, allow_null=True)

    class Meta:
        model = OSPFInstance
        fields = (
            'url',
            'id',
            'display',
            'name',
            'router_id',
            'process_id',
            'device',
            'vrf',
            'reference_bandwidth',
            'timers_spf_initial',
            'timers_spf_hold',
            'timers_spf_max',
            'timers_lsa_initial',
            'timers_lsa_hold',
            'timers_lsa_max',
            'distance',
            'distance_intra_area',
            'distance_inter_area',
            'distance_external',
            'default_information_originate',
            'default_information_metric',
            'default_information_metric_type',
            'max_metric_router_lsa',
            'max_metric_on_startup',
            'passive_interface_default',
            'description',
            'comments',
            'custom_fields',
        )
        brief_fields = (
            'url',
            'id',
            'display',
            'name',
            'router_id',
            'process_id',
            'device',
            'vrf',
        )


class OSPFAreaSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:ospfarea-detail'
    )

    class Meta:
        model = OSPFArea
        fields = (
            'url',
            'id',
            'display',
            'area_id',
            'area_type',
            'description',
            'comments',
        )
        brief_fields = (
            'url',
            'id',
            'display',
            'area_id',
            'area_type',
        )


class OSPFInterfaceSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:ospfinterface-detail'
    )
    instance = OSPFInstanceSerializer(nested=True)
    area = OSPFAreaSerializer(nested=True)
    interface = InterfaceSerializer(nested=True)

    class Meta:
        model = OSPFInterface
        fields = (
            'url',
            'id',
            'display',
            'instance',
            'area',
            'interface',
            'network_type',
            'passive',
            'priority',
            'bfd',
            'authentication',
            'passphrase',
            'description',
            'comments',
        )
        brief_fields = (
            'url',
            'id',
            'display',
            'instance',
            'area',
            'interface',
            'passive',
        )
