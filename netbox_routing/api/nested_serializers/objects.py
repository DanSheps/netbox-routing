from rest_framework import serializers

from netbox.api.serializers import WritableNestedSerializer
from netbox_routing.models import PrefixList, PrefixListEntry, RouteMap, RouteMapEntry


__all__ = (
    'NestedStaticRouteSerializer'
)


class NestedPrefixListSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:prefixlist-detail')

    class Meta:
        model = PrefixList
        fields = ('url', 'id', 'name')


class NestedPrefixListEntrySerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:prefixlist-detail')
    prefix_list = NestedPrefixListSerializer

    class Meta:
        model = PrefixListEntry
        fields = ('url', 'id', 'prefix_list')


class NestedRouteMapSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:prefixlist-detail')

    class Meta:
        model = RouteMap
        fields = ('url', 'id', 'name')


class NestedRouteMapEntrySerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:prefixlist-detail')
    route_map = NestedRouteMapSerializer

    class Meta:
        model = RouteMapEntry
        fields = ('url', 'id', 'route_map')
