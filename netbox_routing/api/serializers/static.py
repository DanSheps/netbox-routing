from rest_framework import serializers

from dcim.api.nested_serializers import NestedDeviceSerializer
from ipam.api.nested_serializers import NestedVRFSerializer
from netbox.api.serializers import NetBoxModelSerializer
from netbox_routing.models import StaticRoute


__all__ = (
    'StaticRouteSerializer'
)


class StaticRouteSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:staticroute-detail')
    devices = NestedDeviceSerializer(many=True)
    vrf = NestedVRFSerializer()

    class Meta:
        model = StaticRoute
        fields = ('url', 'id', 'display', 'devices', 'vrf', 'prefix', 'next_hop', 'name', 'metric', 'permanent')
