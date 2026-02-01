from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer
from netbox_routing.models.objects import *

__all__ = (
    'PrefixListSerializer',
    'PrefixListEntrySerializer',
    'RouteMapSerializer',
    'RouteMapEntrySerializer',
    'ASPathSerializer',
    'ASPathEntrySerializer',
)


class PrefixListSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:prefixlist-detail'
    )

    class Meta:
        model = PrefixList
        fields = (
            'url',
            'id',
            'display',
            'name',
            'description',
            'comments',
            'custom_fields',
        )
        brief_fields = (
            'url',
            'id',
            'display',
            'name',
        )


class PrefixListEntrySerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:prefixlistentry-detail'
    )
    prefix_list = PrefixListSerializer(nested=True)

    class Meta:
        model = PrefixListEntry
        fields = (
            'url',
            'id',
            'display',
            'prefix_list',
            'sequence',
            'action',
            'prefix',
            'le',
            'ge',
            'description',
            'comments',
        )
        brief_fields = (
            'url',
            'id',
            'display',
            'prefix_list',
            'sequence',
            'action',
            'prefix',
            'le',
            'ge',
        )


class RouteMapSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:prefixlist-detail'
    )

    class Meta:
        model = RouteMap
        fields = (
            'url',
            'id',
            'display',
            'name',
            'description',
            'comments',
        )
        brief_fields = ('url', 'id', 'display', 'name')


class RouteMapEntrySerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:prefixlistentry-detail'
    )
    route_map = RouteMapSerializer(nested=True)

    class Meta:
        model = RouteMapEntry
        fields = (
            'url',
            'id',
            'display',
            'route_map',
            'sequence',
            'action',
            'match',
            'set',
            'description',
            'comments',
        )
        brief_fields = (
            'url',
            'id',
            'display',
            'route_map',
            'sequence',
            'action',
            'match',
            'set',
        )


class ASPathSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:aspath-detail'
    )

    class Meta:
        model = ASPath
        fields = (
            'url',
            'id',
            'display',
            'name',
            'description',
            'comments',
        )
        brief_fields = ('url', 'id', 'display', 'name')


class ASPathEntrySerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:aspathentry-detail'
    )
    aspath = ASPathSerializer(nested=True)

    class Meta:
        model = ASPathEntry
        fields = (
            'url',
            'id',
            'display',
            'aspath',
            'sequence',
            'action',
            'pattern',
            'description',
            'comments',
        )
        brief_fields = (
            'url',
            'id',
            'display',
            'aspath',
            'sequence',
            'action',
            'pattern',
        )
