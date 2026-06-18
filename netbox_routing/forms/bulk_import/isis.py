# SPDX-License-Identifier: Apache-2.0

from django.utils.translation import gettext_lazy as _

from dcim.models import Device, Interface
from ipam.models import VRF
from netbox.forms import NetBoxModelImportForm
from utilities.forms.fields import CSVModelChoiceField

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
    'ISISInstanceImportForm',
    'ISISInterfaceImportForm',
    'ISISSettingImportForm',
    'ISISLevelImportForm',
    'ISISInterfaceLevelImportForm',
    'ISISSegmentRoutingImportForm',
    'ISISFlexAlgoImportForm',
)


class ISISFlexAlgoImportForm(NetBoxModelImportForm):
    instance = CSVModelChoiceField(
        queryset=ISISInstance.objects.all(), required=True, help_text=_('Primary key of IS-IS Instance')
    )

    class Meta:
        model = ISISFlexAlgo
        fields = (
            'instance', 'algo_id', 'metric_type', 'priority', 'admin_group_exclude',
            'admin_group_include_any', 'admin_group_include_all', 'description', 'comments', 'tags',
        )


class ISISLevelImportForm(NetBoxModelImportForm):
    instance = CSVModelChoiceField(
        queryset=ISISInstance.objects.all(), required=True, help_text=_('Primary key of IS-IS Instance')
    )

    class Meta:
        model = ISISLevel
        fields = (
            'instance', 'level', 'default_metric', 'wide_metrics_only', 'preference',
            'labeled_preference', 'disabled', 'auth_type', 'auth_key', 'description', 'comments', 'tags',
        )


class ISISInterfaceLevelImportForm(NetBoxModelImportForm):
    interface = CSVModelChoiceField(
        queryset=ISISInterface.objects.all(), required=True, help_text=_('Primary key of IS-IS Interface')
    )

    class Meta:
        model = ISISInterfaceLevel
        fields = (
            'interface', 'level', 'metric', 'hello_interval', 'hello_multiplier',
            'priority', 'passive', 'description', 'comments', 'tags',
        )


class ISISSegmentRoutingImportForm(NetBoxModelImportForm):
    instance = CSVModelChoiceField(
        queryset=ISISInstance.objects.all(), required=True, help_text=_('Primary key of IS-IS Instance')
    )

    class Meta:
        model = ISISSegmentRouting
        fields = (
            'instance', 'enabled', 'prefix_sid_range', 'srgb_start', 'srgb_range',
            'node_sid_index', 'node_sid_label', 'node_sid_v6_index', 'node_sid_v6_label',
            'maximum_sid_depth', 'tunnel_table_pref',
            'description', 'comments', 'tags',
        )


class ISISInstanceImportForm(NetBoxModelImportForm):
    device = CSVModelChoiceField(
        queryset=Device.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Name of device'),
    )
    vrf = CSVModelChoiceField(
        queryset=VRF.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Name of VRF'),
    )

    class Meta:
        model = ISISInstance
        fields = (
            'device',
            'vrf',
            'process_tag',
            'net',
            'is_type',
            'metric_style',
            'overload_bit',
            'overload_on_startup',
            'overload_timeout',
            'distance',
            'maximum_paths',
            'reference_bandwidth',
            'spf_initial_wait',
            'spf_max_wait',
            'lsp_initial_wait',
            'lsp_max_wait',
            'lsp_lifetime',
            'lsp_refresh_interval',
            'lsp_mtu',
            'te_enabled',
            'sr_enabled',
            'sr_node_msd',
            'description',
            'comments',
            'tags',
        )


class ISISInterfaceImportForm(NetBoxModelImportForm):
    device = CSVModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Name of device'),
    )
    instance = CSVModelChoiceField(
        queryset=ISISInstance.objects.all(),
        required=True,
        help_text=_('Primary key of IS-IS Instance'),
    )
    interface = CSVModelChoiceField(
        queryset=Interface.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Name of interface'),
    )

    class Meta:
        model = ISISInterface
        fields = (
            'device',
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
            'tags',
        )


class ISISSettingImportForm(NetBoxModelImportForm):
    class Meta:
        model = ISISSetting
        fields = (
            'assigned_object_type',
            'assigned_object_id',
            'key',
            'value',
            'description',
            'comments',
            'tags',
        )
