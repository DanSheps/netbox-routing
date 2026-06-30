# SPDX-License-Identifier: Apache-2.0

from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from dcim.api.serializers_.device_components import InterfaceSerializer
from dcim.api.serializers_.devices import DeviceSerializer
from ipam.api.serializers_.vrfs import VRFSerializer
from netbox.api.fields import ContentTypeField
from netbox.api.gfk_fields import GFKSerializerField
from netbox.api.serializers import NetBoxModelSerializer

from netbox_routing.constants.isis import ISISSETTING_ASSIGNMENT_MODELS
from netbox_routing.models import (
    ISISInstance,
    ISISInterface,
    ISISSetting,
    ISISLevel,
    ISISInterfaceLevel,
    ISISSegmentRouting,
    ISISFlexAlgo,
)

__all__ = (
    'ISISInstanceSerializer',
    'ISISInterfaceSerializer',
    'ISISSettingSerializer',
    'ISISLevelSerializer',
    'ISISInterfaceLevelSerializer',
    'ISISSegmentRoutingSerializer',
    'ISISFlexAlgoSerializer',
)


class ISISFlexAlgoSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:isisflexalgo-detail'
    )

    class Meta:
        model = ISISFlexAlgo
        fields = (
            'url', 'id', 'display', 'instance', 'algo_id', 'metric_type', 'priority',
            'admin_group_exclude', 'admin_group_include_any', 'admin_group_include_all',
            'description', 'comments', 'custom_fields',
        )
        brief_fields = ('url', 'id', 'display', 'instance', 'algo_id', 'metric_type')


class ISISLevelSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:isislevel-detail'
    )

    class Meta:
        model = ISISLevel
        fields = (
            'url', 'id', 'display', 'instance', 'level', 'default_metric',
            'wide_metrics_only', 'preference', 'labeled_preference', 'disabled',
            'auth_type', 'auth_key', 'description', 'comments', 'custom_fields',
        )
        brief_fields = ('url', 'id', 'display', 'level', 'default_metric')


class ISISInterfaceLevelSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:isisinterfacelevel-detail'
    )

    class Meta:
        model = ISISInterfaceLevel
        fields = (
            'url', 'id', 'display', 'interface', 'level', 'metric',
            'hello_interval', 'hello_multiplier', 'priority', 'passive',
            'description', 'comments', 'custom_fields',
        )
        brief_fields = ('url', 'id', 'display', 'level', 'metric')


class ISISSegmentRoutingSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:isissegmentrouting-detail'
    )

    class Meta:
        model = ISISSegmentRouting
        fields = (
            'url', 'id', 'display', 'instance', 'enabled', 'prefix_sid_range',
            'srgb_start', 'srgb_range', 'node_sid_index', 'node_sid_label',
            'node_sid_v6_index', 'node_sid_v6_label',
            'maximum_sid_depth', 'tunnel_table_pref',
            'description', 'comments', 'custom_fields',
        )
        brief_fields = ('url', 'id', 'display', 'enabled', 'prefix_sid_range')


class ISISSettingSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:isissetting-detail'
    )

    assigned_object_type = ContentTypeField(
        queryset=ContentType.objects.filter(ISISSETTING_ASSIGNMENT_MODELS),
        required=False,
        allow_null=True,
    )
    assigned_object = GFKSerializerField(read_only=True)

    class Meta:
        model = ISISSetting
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


class ISISInstanceSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:isisinstance-detail'
    )
    device = DeviceSerializer(nested=True)
    vrf = VRFSerializer(nested=True, required=False, allow_null=True)

    class Meta:
        model = ISISInstance
        fields = (
            'url',
            'id',
            'display',
            'device',
            'vrf',
            'process_tag',
            'net',
            'is_type',
            'metric_style',
            'overload_bit',
            'overload_on_startup',
            'overload_timeout',
            'area_auth_type',
            'area_auth_key',
            'domain_auth_type',
            'domain_auth_key',
            'spf_initial_wait',
            'spf_max_wait',
            'lsp_initial_wait',
            'lsp_max_wait',
            'lsp_lifetime',
            'lsp_refresh_interval',
            'lsp_mtu',
            'te_enabled',
            'distance',
            'maximum_paths',
            'reference_bandwidth',
            'description',
            'comments',
            'custom_fields',
        )
        brief_fields = (
            'url',
            'id',
            'display',
            'device',
            'vrf',
            'process_tag',
            'net',
            'is_type',
        )


class ISISInterfaceSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_routing-api:isisinterface-detail'
    )
    instance = ISISInstanceSerializer(nested=True)
    interface = InterfaceSerializer(nested=True)

    class Meta:
        model = ISISInterface
        fields = (
            'url',
            'id',
            'display',
            'instance',
            'interface',
            'address_family',
            'circuit_type',
            'network_type',
            'metric',
            'passive',
            'hello_auth_type',
            'hello_auth_key',
            'bfd_enabled',
            'csnp_interval',
            'retransmit_interval',
            'lsp_interval',
            'mesh_group',
            'description',
            'comments',
            'custom_fields',
        )
        brief_fields = (
            'url',
            'id',
            'display',
            'instance',
            'interface',
            'address_family',
        )
