# SPDX-License-Identifier: Apache-2.0

from django.utils.translation import gettext_lazy as _

from netbox.ui import attrs, panels
from netbox_routing.ui.attributes import ContentTypeAttribute

__all__ = (
    'ISISInstancePanel',
    'ISISInstanceSettingsPanel',
    'ISISInterfacePanel',
    'ISISInterfaceSettingsPanel',
    'ISISSettingPanel',
    'ISISLevelPanel',
    'ISISInterfaceLevelPanel',
    'ISISSegmentRoutingPanel',
    'ISISFlexAlgoPanel',
)


class ISISFlexAlgoPanel(panels.ObjectAttributesPanel):
    instance = attrs.RelatedObjectAttr('instance', linkify=True, label=_('Instance'))
    algo_id = attrs.NumericAttr('algo_id', label=_('Algorithm ID'))
    metric_type = attrs.TextAttr('metric_type', label=_('Metric Type'))
    priority = attrs.NumericAttr('priority', label=_('Priority'))
    admin_group_exclude = attrs.TextAttr('admin_group_exclude', label=_('Admin-group Exclude'))
    admin_group_include_any = attrs.TextAttr('admin_group_include_any', label=_('Admin-group Include-Any'))
    admin_group_include_all = attrs.TextAttr('admin_group_include_all', label=_('Admin-group Include-All'))


class ISISLevelPanel(panels.ObjectAttributesPanel):
    instance = attrs.RelatedObjectAttr('instance', linkify=True, label=_('Instance'))
    level = attrs.NumericAttr('level', label=_('Level'))
    default_metric = attrs.NumericAttr('default_metric', label=_('Default Metric'))
    wide_metrics_only = attrs.BooleanAttr('wide_metrics_only', label=_('Wide Metrics Only'))
    preference = attrs.NumericAttr('preference', label=_('Preference'))
    labeled_preference = attrs.NumericAttr('labeled_preference', label=_('Labeled Preference'))
    disabled = attrs.BooleanAttr('disabled', label=_('Disabled'))
    auth_type = attrs.ChoiceAttr('auth_type', label=_('Auth Type'))
    auth_key = attrs.TextAttr('auth_key', label=_('Auth Key'))


class ISISInterfaceLevelPanel(panels.ObjectAttributesPanel):
    interface = attrs.RelatedObjectAttr('interface', linkify=True, label=_('Interface'))
    level = attrs.NumericAttr('level', label=_('Level'))
    metric = attrs.NumericAttr('metric', label=_('Metric'))
    hello_interval = attrs.NumericAttr('hello_interval', label=_('Hello Interval'))
    hello_multiplier = attrs.NumericAttr('hello_multiplier', label=_('Hello Multiplier'))
    priority = attrs.NumericAttr('priority', label=_('Priority'))
    passive = attrs.BooleanAttr('passive', label=_('Passive'))


class ISISSegmentRoutingPanel(panels.ObjectAttributesPanel):
    instance = attrs.RelatedObjectAttr('instance', linkify=True, label=_('Instance'))
    enabled = attrs.BooleanAttr('enabled', label=_('Enabled'))
    prefix_sid_range = attrs.TextAttr('prefix_sid_range', label=_('Prefix-SID Range'))
    srgb_start = attrs.NumericAttr('srgb_start', label=_('SRGB Start'))
    srgb_range = attrs.NumericAttr('srgb_range', label=_('SRGB Range'))
    node_sid_index = attrs.NumericAttr('node_sid_index', label=_('Node-SID Index (IPv4)'))
    node_sid_label = attrs.NumericAttr('node_sid_label', label=_('Node-SID Label (IPv4)'))
    node_sid_v6_index = attrs.NumericAttr('node_sid_v6_index', label=_('Node-SID Index (IPv6)'))
    node_sid_v6_label = attrs.NumericAttr('node_sid_v6_label', label=_('Node-SID Label (IPv6)'))
    maximum_sid_depth = attrs.NumericAttr('maximum_sid_depth', label=_('Maximum SID Depth'))
    tunnel_table_pref = attrs.NumericAttr('tunnel_table_pref', label=_('Tunnel-Table Pref'))


class ISISInstancePanel(panels.ObjectAttributesPanel):
    device = attrs.RelatedObjectAttr('device', label=_('Device'))
    vrf = attrs.RelatedObjectAttr('vrf', linkify=True)
    process_tag = attrs.TextAttr('process_tag', label=_('Process Tag'))
    net = attrs.TextAttr('net', label=_('NET'))
    is_type = attrs.ChoiceAttr('is_type', label=_('IS Type'))
    description = attrs.TextAttr('description', label=_('Description'))


class ISISInstanceSettingsPanel(panels.ObjectAttributesPanel):
    metric_style = attrs.ChoiceAttr('metric_style', label=_('Metric Style'))
    area_auth_type = attrs.ChoiceAttr('area_auth_type', label=_('Area Auth Type'))
    area_auth_key = attrs.TextAttr('area_auth_key', label=_('Area Auth Key'))
    domain_auth_type = attrs.ChoiceAttr('domain_auth_type', label=_('Domain Auth Type'))
    domain_auth_key = attrs.TextAttr('domain_auth_key', label=_('Domain Auth Key'))
    overload_bit = attrs.BooleanAttr('overload_bit', label=_('Overload Bit'))
    overload_on_startup = attrs.BooleanAttr('overload_on_startup', label=_('Overload on Startup'))
    overload_timeout = attrs.NumericAttr('overload_timeout', label=_('Overload Timeout'))
    spf_initial_wait = attrs.NumericAttr('spf_initial_wait', label=_('SPF Initial Wait'))
    spf_max_wait = attrs.NumericAttr('spf_max_wait', label=_('SPF Max Wait'))
    lsp_initial_wait = attrs.NumericAttr('lsp_initial_wait', label=_('LSP-gen Initial Wait'))
    lsp_max_wait = attrs.NumericAttr('lsp_max_wait', label=_('LSP-gen Max Wait'))
    lsp_lifetime = attrs.NumericAttr('lsp_lifetime', label=_('LSP Lifetime'))
    lsp_refresh_interval = attrs.NumericAttr('lsp_refresh_interval', label=_('LSP Refresh Interval'))
    lsp_mtu = attrs.NumericAttr('lsp_mtu', label=_('LSP MTU'))
    te_enabled = attrs.BooleanAttr('te_enabled', label=_('Traffic Engineering'))
    sr_enabled = attrs.BooleanAttr('sr_enabled', label=_('Segment Routing'))
    sr_node_msd = attrs.NumericAttr('sr_node_msd', label=_('SR Maximum SID Depth'))
    distance = attrs.NumericAttr('distance', label=_('Distance'))
    maximum_paths = attrs.NumericAttr('maximum_paths', label=_('Maximum Paths'))
    reference_bandwidth = attrs.NumericAttr('reference_bandwidth', label=_('Reference Bandwidth'))


class ISISInterfacePanel(panels.ObjectAttributesPanel):
    instance = attrs.RelatedObjectAttr('instance', label=_('Instance'))
    interface = attrs.RelatedObjectAttr('interface', label=_('Interface'))
    address_family = attrs.ChoiceAttr('address_family', label=_('Address Family'))


class ISISInterfaceSettingsPanel(panels.ObjectAttributesPanel):
    circuit_type = attrs.ChoiceAttr('circuit_type', label=_('Circuit Type'))
    network_type = attrs.ChoiceAttr('network_type', label=_('Network Type'))
    metric = attrs.NumericAttr('metric', label=_('Metric'))
    passive = attrs.BooleanAttr('passive', label=_('Passive'))
    csnp_interval = attrs.NumericAttr('csnp_interval', label=_('CSNP Interval'))
    retransmit_interval = attrs.NumericAttr('retransmit_interval', label=_('Retransmit Interval'))
    lsp_interval = attrs.NumericAttr('lsp_interval', label=_('LSP Interval'))
    mesh_group = attrs.TextAttr('mesh_group', label=_('Mesh Group'))
    hello_auth_type = attrs.ChoiceAttr('hello_auth_type', label=_('Hello Auth Type'))
    hello_auth_key = attrs.TextAttr('hello_auth_key', label=_('Hello Auth Key'))
    description = attrs.TextAttr('description', label=_('Description'))


class ISISSettingPanel(panels.ObjectAttributesPanel):
    assigned_object_type = ContentTypeAttribute('assigned_object_type', label=_('Type'))
    assigned_object = attrs.RelatedObjectAttr('assigned_object', linkify=True)
    name = attrs.TextAttr('key', label=_('Name'))
    value = attrs.TextAttr('value')
