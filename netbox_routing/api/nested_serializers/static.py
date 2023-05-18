from rest_framework import serializers

from netbox.api.serializers import WritableNestedSerializer
from netbox_routing.models import StaticRoute


__all__ = (
    'NestedStaticRouteSerializer'
)


class NestedStaticRouteSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:staticroute-detail')

    class Meta:
        model = StaticRoute
        fields = ('url', 'id', 'display', 'prefix', 'next_hop', 'name', 'metric', 'permanent')