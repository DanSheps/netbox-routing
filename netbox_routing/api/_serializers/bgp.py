from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from ipam.api.serializers_.asns import ASNSerializer
from ipam.api.serializers_.ip import IPAddressSerializer
from ipam.api.serializers_.vrfs import VRFSerializer
from netbox.api.fields import ContentTypeField
from netbox.api.gfk_fields import GFKSerializerField
from netbox.api.serializers import NetBoxModelSerializer
from tenancy.api.serializers_.tenants import TenantSerializer
from utilities.api import get_serializer_for_model

from netbox_routing.models.bgp import *

__all__ = (
    'BGPSettingSerializer',
    'BGPRouterSerializer',
    'BGPScopeSerializer',
    'BGPAddressFamilySerializer',
    'BGPPeerSerializer',
    'BGPPeerTemplateSerializer',
    'BGPPolicyTemplateSerializer',
    'BGPSessionTemplateSerializer',
    'BGPPeerAddressFamilySerializer',
)


class BGPSettingSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:bgpsetting-detail'
    )

    assigned_object = GFKSerializerField(read_only=True)

    class Meta:
        model = BGPSetting
        fields = (
            'url',
            'id',
            'display',
            'assigned_object_type',
            'assigned_object_id',
            'assigned_object',
            'key',
            'value',
            'description',
            'comments',
            'custom_fields',
        )
        brief_fields = (
            'url',
            'id',
            'display',
            'assigned_object',
            'key',
        )

    @extend_schema_field(serializers.JSONField(allow_null=True))
    def get_assigned_object(self, obj):
        if obj.assigned_object is None:
            return None
        serializer = get_serializer_for_model(obj.assigned_object)
        context = {'request': self.context['request']}
        return serializer(obj.assigned_object, context=context, nested=True).data


class BGPSessionTemplateSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:bgpscope-detail'
    )

    remote_as = ASNSerializer(nested=True, required=False)
    local_as = ASNSerializer(nested=True, required=False)
    tenant = TenantSerializer(nested=True, required=False)

    class Meta:
        model = BGPSessionTemplate
        fields = (
            'url',
            'id',
            'display',
            'name',
            'parent',
            'enabled',
            'remote_as',
            'local_as',
            'bfd',
            'password',
            'tenant',
            'description',
            'comments',
        )
        brief_fields = (
            'url',
            'id',
            'display',
            'name',
            'parent',
        )


class BGPPolicyTemplateSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:bgpscope-detail'
    )

    tenant = TenantSerializer(nested=True, required=False)

    class Meta:
        model = BGPPolicyTemplate
        fields = (
            'url',
            'id',
            'display',
            'name',
            'enabled',
            'prefixlist_in',
            'prefixlist_out',
            'routemap_in',
            'routemap_out',
            'tenant',
            'description',
            'comments',
        )
        brief_fields = (
            'url',
            'id',
            'display',
            'name',
        )


class BGPPeerTemplateSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:bgpaddressfamily-detail'
    )

    remote_as = ASNSerializer(nested=True, required=False)
    tenant = TenantSerializer(nested=True, required=False)

    class Meta:
        model = BGPPeerTemplate
        fields = (
            'url',
            'id',
            'display',
            'name',
            'remote_as',
            'enabled',
            'tenant',
            'description',
            'comments',
        )
        brief_fields = (
            'url',
            'id',
            'display',
            'name',
            'remote_as',
        )


class BGPRouterSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:bgprouter-detail'
    )

    assigned_object = GFKSerializerField(read_only=True)
    asn = ASNSerializer(nested=True)
    settings = BGPSettingSerializer(many=True, required=False)
    tenant = TenantSerializer(nested=True, required=False)
    peer_templates = BGPSessionTemplateSerializer(
        many=True, nested=True, required=False
    )
    policy_templates = BGPSessionTemplateSerializer(
        many=True, nested=True, required=False
    )
    session_templates = BGPSessionTemplateSerializer(
        many=True, nested=True, required=False
    )

    class Meta:
        model = BGPRouter
        fields = (
            'url',
            'id',
            'display',
            'name',
            'asn',
            'assigned_object',
            'assigned_object_type',
            'assigned_object_id',
            'session_templates',
            'policy_templates',
            'peer_templates',
            'settings',
            'tenant',
            'description',
            'comments',
        )
        brief_fields = ('url', 'id', 'display', 'asn', 'assigned_object', 'name')

    @extend_schema_field(serializers.JSONField(allow_null=True))
    def get_assigned_object(self, obj):
        if obj.assigned_object is None:
            return None
        serializer = get_serializer_for_model(obj.assigned_object)
        context = {'request': self.context['request']}
        return serializer(obj.assigned_object, context=context, nested=True).data


class BGPScopeSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:bgpscope-detail'
    )

    router = BGPRouterSerializer(nested=True)
    vrf = VRFSerializer(nested=True)
    settings = BGPSettingSerializer(many=True, required=False)
    tenant = TenantSerializer(nested=True, required=False)

    class Meta:
        model = BGPScope
        fields = (
            'url',
            'id',
            'display',
            'router',
            'vrf',
            'settings',
            'tenant',
            'description',
            'comments',
        )
        brief_fields = (
            'url',
            'id',
            'display',
            'router',
            'vrf',
        )


class BGPAddressFamilySerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:bgpaddressfamily-detail'
    )

    scope = BGPScopeSerializer(nested=True)
    settings = BGPSettingSerializer(many=True, required=False)

    class Meta:
        model = BGPAddressFamily
        fields = (
            'url',
            'id',
            'display',
            'scope',
            'address_family',
            'settings',
            'description',
            'comments',
        )
        brief_fields = (
            'url',
            'id',
            'display',
            'scope',
            'address_family',
        )


class BGPPeerSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:bgppeer-detail'
    )

    scope = BGPScopeSerializer(nested=True)
    peer = IPAddressSerializer(nested=True)
    source = IPAddressSerializer(nested=True, required=False)
    remote_as = ASNSerializer(nested=True, required=False)
    local_as = ASNSerializer(nested=True, required=False)
    tenant = TenantSerializer(nested=True, required=False)

    class Meta:
        model = BGPPeer
        fields = (
            'url',
            'id',
            'display',
            'scope',
            'peer',
            'source',
            'name',
            'remote_as',
            'local_as',
            'status',
            'enabled',
            'bfd',
            'password',
            'tenant',
            'description',
            'comments',
        )
        brief_fields = (
            'url',
            'id',
            'display',
            'name',
            'scope',
            'peer',
            'remote_as',
            'enabled',
            'status',
        )


class BGPPeerAddressFamilySerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:bgppeeraddressfamily-detail'
    )
    assigned_object_type = ContentTypeField(
        queryset=ContentType.objects.filter(BGPPEERAF_ASSIGNMENT_MODELS),
        required=False,
        allow_null=True,
    )
    assigned_object = GFKSerializerField(read_only=True)
    # tenant = TenantSerializer(nested=True)

    class Meta:
        model = BGPPeerAddressFamily
        fields = (
            'url',
            'id',
            'display',
            'assigned_object_type',
            'assigned_object_id',
            'assigned_object',
            'address_family',
            'enabled',
            'peer_policy',
            'prefixlist_in',
            'prefixlist_out',
            'routemap_in',
            'routemap_out',
            'description',
            'comments',
        )
        brief_fields = (
            'url',
            'id',
            'display',
            'assigned_object',
            'address_family',
            'enabled',
        )

    @extend_schema_field(serializers.JSONField(allow_null=True))
    def get_assigned_object(self, obj):
        if obj.assigned_object is None:
            return None
        serializer = get_serializer_for_model(obj.assigned_object)
        context = {'request': self.context['request']}
        return serializer(obj.assigned_object, context=context, nested=True).data
