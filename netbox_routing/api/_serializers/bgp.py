from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from dcim.api.serializers_.devices import DeviceSerializer
from ipam.api.serializers_.asns import ASNSerializer
from ipam.api.serializers_.ip import IPAddressSerializer
from ipam.api.serializers_.vrfs import VRFSerializer
from netbox.api.fields import ContentTypeField
from netbox.api.serializers import NetBoxModelSerializer
from tenancy.api.serializers_.tenants import TenantSerializer
from utilities.api import get_serializer_for_model

from netbox_routing.models.bgp import *

__all__ = (
    'BGPRouterSerializer',
    'BGPScopeSerializer',
    'BGPAddressFamilySerializer',
    'BGPSettingSerializer',
)


class BGPSettingSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:bgprouter-detail'
    )

    assigned_object = serializers.SerializerMethodField(read_only=True)

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


class BGPRouterSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:bgprouter-detail'
    )

    device = DeviceSerializer(nested=True)
    asn = ASNSerializer(nested=True)
    settings = BGPSettingSerializer(many=True)
    tenant = TenantSerializer(nested=True)

    class Meta:
        model = BGPRouter
        fields = (
            'url',
            'id',
            'display',
            'device',
            'asn',
            'settings',
            'tenant',
            'description',
            'comments',
        )
        brief_fields = (
            'url',
            'id',
            'display',
            'device',
            'asn',
        )


class BGPScopeSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:bgpscope-detail'
    )

    router = BGPRouterSerializer(nested=True)
    vrf = VRFSerializer(nested=True)
    settings = BGPSettingSerializer(many=True)
    tenant = TenantSerializer(nested=True)

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
    settings = BGPSettingSerializer(many=True)
    tenant = TenantSerializer(nested=True)

    class Meta:
        model = BGPAddressFamily
        fields = (
            'url',
            'id',
            'display',
            'scope',
            'address_family',
            'settings',
            'tenant',
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


class BGPSessionTemplateSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:bgpscope-detail'
    )

    router = BGPRouterSerializer(nested=True)
    asn = ASNSerializer(nested=True)
    tenant = TenantSerializer(nested=True)

    class Meta:
        model = BGPSessionTemplate
        fields = (
            'url',
            'id',
            'display',
            'name',
            'router',
            'parent',
            'enabled',
            'asn',
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
            'router',
            'parent',
        )


class BGPPolicyTemplateSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:bgpscope-detail'
    )

    router = BGPRouterSerializer(nested=True)
    tenant = TenantSerializer(nested=True)

    class Meta:
        model = BGPPolicyTemplate
        fields = (
            'url',
            'id',
            'display',
            'name',
            'router',
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
            'router',
        )


class BGPPeerTemplateSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:bgpaddressfamily-detail'
    )

    remote_as = ASNSerializer(nested=True)
    tenant = TenantSerializer(nested=True)

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


class BGPPeerSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:bgpaddressfamily-detail'
    )

    scope = BGPScopeSerializer(nested=True)
    peer = IPAddressSerializer(nested=True)
    remote_as = ASNSerializer(nested=True)
    local_as = ASNSerializer(nested=True)
    tenant = TenantSerializer(nested=True)

    class Meta:
        model = BGPPeer
        fields = (
            'url',
            'id',
            'display',
            'scope',
            'peer',
            'remote_as',
            'local_as',
            'enabled',
            'bfd',
            'password',
            'tenant',
            'description',
            'comments',
        )
        brief_fields = ('url', 'id', 'display', 'scope', 'peer', 'remote_as', 'enabled')


class BGPPeerAddressFamilySerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:bgpaddressfamily-detail'
    )
    assigned_object_type = ContentTypeField(
        queryset=ContentType.objects.filter(BGPPEERAF_ASSIGNMENT_MODELS),
        required=False,
        allow_null=True,
    )
    assigned_object = serializers.SerializerMethodField(read_only=True)
    tenant = TenantSerializer(nested=True)

    class Meta:
        model = BGPPeer
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
            'tenant',
            'description',
            'comments',
        )
        brief_fields = ('url', 'id', 'display', 'scope', 'peer', 'remote_as', 'enabled')
