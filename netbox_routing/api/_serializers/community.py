from rest_framework import serializers

from ipam.api.serializers_.roles import RoleSerializer
from netbox.api.serializers import NetBoxModelSerializer
from tenancy.api.serializers_.tenants import TenantSerializer

from netbox_routing.models.community import *

__all__ = (
    'CommunityListSerializer',
    'CommunitySerializer',
    'CommunityListEntrySerializer',
)


class CommunitySerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:community-detail'
    )
    role = RoleSerializer(nested=True, required=False)
    tenant = TenantSerializer(nested=True, required=False)

    class Meta:
        model = Community
        fields = (
            'url',
            'id',
            'display',
            'community',
            'role',
            'status',
            'tenant',
            'description',
            'comments',
        )
        brief_fields = ('url', 'id', 'display', 'community', 'description')


class CommunityListSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:communitylist-detail'
    )
    tenant = TenantSerializer(nested=True, required=False)

    class Meta:
        model = CommunityList
        fields = (
            'url',
            'id',
            'display',
            'name',
            'tenant',
            'description',
            'comments',
        )
        brief_fields = ('url', 'id', 'display', 'name', 'description')


class CommunityListEntrySerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:communitylistentry-detail'
    )

    class Meta:
        model = CommunityListEntry
        fields = (
            'url',
            'id',
            'display',
            'community_list',
            'action',
            'community',
            'description',
            'comments',
        )
        brief_fields = (
            'url',
            'id',
            'display',
            'community_list',
            'action',
            'community',
            'description',
        )
