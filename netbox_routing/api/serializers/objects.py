from rest_framework import serializers

from netbox_routing.api.nested_serializers import NestedPrefixListSerializer, NestedRouteMapSerializer
from netbox.api.serializers import NetBoxModelSerializer
from netbox_routing.models import PrefixList, PrefixListEntry, RouteMap, RouteMapEntry


__all__ = (
    'StaticRouteSerializer'
)


class PrefixListSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:prefixlist-detail')

    class Meta:
        model = PrefixList
        fields = ('url', 'id', 'display', 'name')


class PrefixListEntrySerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:prefixlistentry-detail')
    prefix_list = NestedPrefixListSerializer()

    class Meta:
        model = PrefixListEntry
        fields = ('url', 'id', 'display', 'prefix_list', 'sequence', 'type', 'prefix', 'le', 'ge')


class RouteMapSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:prefixlist-detail')

    class Meta:
        model = RouteMap
        fields = ('url', 'id', 'display', 'name')


class RouteMapEntrySerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:prefixlistentry-detail')
    route_map = NestedRouteMapSerializer()


    class Meta:
        model = RouteMapEntry
        fields = ('url', 'id', 'display', 'route_map', 'sequence', 'type')
