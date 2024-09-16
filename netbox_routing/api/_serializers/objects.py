from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer
from netbox_routing.models import PrefixList, PrefixListEntry, RouteMap, RouteMapEntry


__all__ = (
    'StaticRouteSerializer'
)


class PrefixListSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:prefixlist-detail')

    class Meta:
        model = PrefixList
        fields = ('url', 'id', 'display', 'name', 'description', 'comments',)
        brief_fields = ('url', 'id', 'display', 'name', )


class PrefixListEntrySerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:prefixlistentry-detail')
    prefix_list = PrefixListSerializer(nested=True)

    class Meta:
        model = PrefixListEntry
        fields = (
            'url', 'id', 'display', 'prefix_list', 'sequence', 'type', 'prefix', 'le', 'ge', 'description', 'comments',
        )
        brief_fields = ('url', 'id', 'display', 'prefix_list', 'sequence', 'type', 'prefix', 'le', 'ge')


class RouteMapSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:prefixlist-detail')

    class Meta:
        model = RouteMap
        fields = ('url', 'id', 'display', 'name', 'description', 'comments',)
        brief_fields = ('url', 'id', 'display', 'name')


class RouteMapEntrySerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:prefixlistentry-detail')
    route_map = RouteMapSerializer(nested=True)


    class Meta:
        model = RouteMapEntry
        fields = ('url', 'id', 'display', 'route_map', 'sequence', 'type', 'description', 'comments',)
        brief_fields = ('url', 'id', 'display', 'route_map', 'sequence', 'type')
