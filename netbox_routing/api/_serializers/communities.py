from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer
from tenancy.api.serializers_.tenants import TenantSerializer

from netbox_routing.models.communities import *


__all__ = (
    'CommunityListSerializer',
    'CommunitySerializer',
)


class CommunityListSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:staticroute-detail'
    )
    tenant = TenantSerializer(read_only=True)

    class Meta:
        model = CommunityList
        fields = (
            'url',
            'id',
            'display',
            'name',
            'communities',
            'tenant',
            'description',
            'comments',
        )
        brief_fields = ('url', 'id', 'display', 'name', 'description')


class CommunitySerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:staticroute-detail'
    )
    tenant = TenantSerializer(read_only=True)

    class Meta:
        model = Community
        fields = (
            'url',
            'id',
            'display',
            'community',
            'tenant',
            'description',
            'comments',
        )
        brief_fields = ('url', 'id', 'display', 'community', 'description')
