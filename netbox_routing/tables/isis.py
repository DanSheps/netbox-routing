# SPDX-License-Identifier: Apache-2.0

import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable, columns
from netbox_routing.models import (
    ISISInstance,
    ISISInterface,
    ISISSetting,
    ISISLevel,
    ISISInterfaceLevel,
    ISISSegmentRouting,
    ISISFlexAlgo,
    ISISPrefixSID,
    ISISSRv6Locator,
)

__all__ = (
    'ISISInstanceTable',
    'ISISInterfaceTable',
    'ISISSettingTable',
    'ISISLevelTable',
    'ISISInterfaceLevelTable',
    'ISISSegmentRoutingTable',
    'ISISFlexAlgoTable',
    'ISISPrefixSIDTable',
    'ISISSRv6LocatorTable',
)


class ISISFlexAlgoTable(NetBoxTable):
    instance = tables.Column(verbose_name=_('Instance'), linkify=True)

    class Meta(NetBoxTable.Meta):
        model = ISISFlexAlgo
        fields = ('pk', 'id', 'instance', 'algo_id', 'metric_type', 'priority', 'admin_group_exclude')
        default_columns = ('pk', 'id', 'instance', 'algo_id', 'metric_type', 'priority')


class ISISPrefixSIDTable(NetBoxTable):
    interface = tables.Column(verbose_name=_('Interface'), linkify=True)

    class Meta(NetBoxTable.Meta):
        model = ISISPrefixSID
        fields = (
            'pk', 'id', 'interface', 'algorithm', 'sid_index', 'sid_label',
            'n_flag', 'no_php', 'explicit_null', 'readvertise',
        )
        default_columns = ('pk', 'id', 'interface', 'algorithm', 'sid_index', 'sid_label')


class ISISSRv6LocatorTable(NetBoxTable):
    instance = tables.Column(verbose_name=_('Instance'), linkify=True)

    class Meta(NetBoxTable.Meta):
        model = ISISSRv6Locator
        fields = (
            'pk', 'id', 'instance', 'name', 'prefix', 'algorithm',
            'is_micro_segment', 'flavor', 'enabled',
        )
        default_columns = ('pk', 'id', 'instance', 'name', 'prefix', 'enabled')


class ISISLevelTable(NetBoxTable):
    instance = tables.Column(verbose_name=_('Instance'), linkify=True)

    class Meta(NetBoxTable.Meta):
        model = ISISLevel
        fields = (
            'pk', 'id', 'instance', 'level', 'default_metric', 'wide_metrics_only',
            'preference', 'labeled_preference', 'disabled',
        )
        default_columns = ('pk', 'id', 'instance', 'level', 'default_metric', 'wide_metrics_only')


class ISISInterfaceLevelTable(NetBoxTable):
    interface = tables.Column(verbose_name=_('Interface'), linkify=True)

    class Meta(NetBoxTable.Meta):
        model = ISISInterfaceLevel
        fields = (
            'pk', 'id', 'interface', 'level', 'metric', 'hello_interval',
            'hello_multiplier', 'priority', 'passive',
        )
        default_columns = ('pk', 'id', 'interface', 'level', 'metric')


class ISISSegmentRoutingTable(NetBoxTable):
    instance = tables.Column(verbose_name=_('Instance'), linkify=True)

    class Meta(NetBoxTable.Meta):
        model = ISISSegmentRouting
        fields = (
            'pk', 'id', 'instance', 'enabled', 'srv6_enabled', 'prefix_sid_range',
            'srgb_start', 'srgb_range', 'srlb_start', 'srlb_range',
            'maximum_sid_depth', 'tunnel_table_pref',
        )
        default_columns = ('pk', 'id', 'instance', 'enabled', 'srv6_enabled', 'prefix_sid_range')


class ISISSettingTable(NetBoxTable):
    assigned_object_type = columns.ContentTypeColumn(verbose_name=_('Object Type'))
    assigned_object = tables.Column(
        linkify=True, orderable=False, verbose_name=_('Object')
    )

    class Meta(NetBoxTable.Meta):
        model = ISISSetting
        fields = ('pk', 'id', 'assigned_object_type', 'assigned_object', 'key', 'value')
        default_columns = (
            'pk',
            'id',
            'assigned_object_type',
            'assigned_object',
            'key',
            'value',
        )


class ISISInstanceTable(NetBoxTable):
    device = tables.Column(verbose_name=_('Device'), linkify=True)
    vrf = tables.Column(verbose_name=_('VRF'), linkify=True)

    class Meta(NetBoxTable.Meta):
        model = ISISInstance
        fields = ('pk', 'id', 'device', 'vrf', 'process_tag', 'net', 'is_type')
        default_columns = ('pk', 'id', 'device', 'process_tag', 'net', 'is_type')


class ISISInterfaceTable(NetBoxTable):
    instance = tables.Column(verbose_name=_('Instance'), linkify=True)
    device = tables.Column(
        verbose_name=_('Device'),
        linkify=True,
        accessor='instance__device',
    )
    interface = tables.Column(verbose_name=_('Interface'), linkify=True)

    class Meta(NetBoxTable.Meta):
        model = ISISInterface
        fields = (
            'pk',
            'id',
            'instance',
            'device',
            'interface',
            'address_family',
            'circuit_type',
            'network_type',
            'metric',
            'passive',
            'hello_auth_type',
            'bfd_enabled',
            'frr_enabled',
            'frr_protection',
        )
        default_columns = (
            'pk',
            'id',
            'instance',
            'interface',
            'address_family',
            'passive',
        )
