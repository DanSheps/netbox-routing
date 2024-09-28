from rest_framework import serializers

from dcim.api.serializers_.device_components import InterfaceSerializer
from dcim.api.serializers_.devices import DeviceSerializer
from ipam.api.serializers_.ip import PrefixSerializer
from netbox.api.serializers import NetBoxModelSerializer
from netbox_routing.models import (
    EIGRPRouter, EIGRPAddressFamily, EIGRPNetwork, EIGRPInterface
)


__all__ = (
    'EIGRPRouterSerializer',
    'EIGRPAddressFamilySerializer',
    'EIGRPNetworkSerializer',
    'EIGRPInterfaceSerializer',
)


class EIGRPRouterSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:eigrprouter-detail')
    device = DeviceSerializer(nested=True)

    class Meta:
        model = EIGRPRouter
        fields = ('url', 'id', 'display', 'name', 'pid', 'rid', 'device', 'description', 'comments', )
        brief_fields = ('url', 'id', 'display', 'name', 'pid', 'rid', 'device', )


class EIGRPAddressFamilySerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:eigrpaddressfamily-detail')
    router = EIGRPRouterSerializer(nested=True)


    class Meta:
        model = EIGRPAddressFamily
        fields = (
            'url', 'id', 'display', 'router', 'family', 'description', 'comments',
        )
        brief_fields = ('url', 'id', 'display', 'router', 'family',)


class EIGRPNetworkSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:eigrpnetwork-detail')
    router = EIGRPRouterSerializer(nested=True)
    address_family = EIGRPAddressFamilySerializer(nested=True)
    network = PrefixSerializer(nested=True)

    class Meta:
        model = EIGRPNetwork
        fields = (
            'url', 'id', 'display', 'router', 'address_family', 'network', 'description', 'comments',
        )
        brief_fields = ('url', 'id', 'display', 'router', 'address_family', 'network',)


class EIGRPInterfaceSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:eigrpinterface-detail')
    router = EIGRPRouterSerializer(nested=True)
    address_family = EIGRPAddressFamilySerializer(nested=True)
    interface = InterfaceSerializer(nested=True)

    class Meta:
        model = EIGRPInterface
        fields = (
            'url', 'id', 'display', 'router', 'address_family', 'interface', 'passive', 'bfd',
            'authentication', 'passphrase', 'description', 'comments',
        )
        brief_fields = (
            'url', 'id', 'display', 'router', 'address_family', 'interface',
        )
