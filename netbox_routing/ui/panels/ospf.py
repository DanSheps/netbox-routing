from django.utils.translation import gettext_lazy as _

from netbox.ui import attrs, panels

__all__ = (
    'OSPFInstancePanel',
    'OSPFInstanceSettingsPanel',
    'OSPFAreaPanel',
    'OSPFInterfacePanel',
    'OSPFInterfaceSettingsPanel',
)


class OSPFInstancePanel(panels.ObjectAttributesPanel):
    name = attrs.TextAttr('name', label=_('Name'))
    process_id = attrs.NumericAttr('process_id', label=_('Process ID'))
    router_id = attrs.TextAttr('router_id', label=_('Router ID'))
    device = attrs.RelatedObjectAttr('device', label=_('Device'))
    vrf = attrs.RelatedObjectAttr('vrf', linkify=True)
    description = attrs.TextAttr('description', label=_('Description'))


class OSPFInstanceSettingsPanel(panels.ObjectAttributesPanel):
    reference_bandwidth = attrs.NumericAttr(
        'reference_bandwidth', label=_('Reference Bandwidth (Mbps)')
    )
    passive_interface_default = attrs.BooleanAttr(
        'passive_interface_default', label=_('Passive Interface Default')
    )
    timers_spf_initial = attrs.NumericAttr(
        'timers_spf_initial', label=_('SPF Initial Delay (ms)')
    )
    timers_spf_hold = attrs.NumericAttr(
        'timers_spf_hold', label=_('SPF Hold Time (ms)')
    )
    timers_spf_max = attrs.NumericAttr('timers_spf_max', label=_('SPF Max Wait (ms)'))
    timers_lsa_initial = attrs.NumericAttr(
        'timers_lsa_initial', label=_('LSA Initial Delay (ms)')
    )
    timers_lsa_hold = attrs.NumericAttr(
        'timers_lsa_hold', label=_('LSA Hold Time (ms)')
    )
    timers_lsa_max = attrs.NumericAttr('timers_lsa_max', label=_('LSA Max Wait (ms)'))
    distance = attrs.NumericAttr('distance', label=_('Distance'))
    distance_intra_area = attrs.NumericAttr(
        'distance_intra_area', label=_('Intra-Area Distance')
    )
    distance_inter_area = attrs.NumericAttr(
        'distance_inter_area', label=_('Inter-Area Distance')
    )
    distance_external = attrs.NumericAttr(
        'distance_external', label=_('External Distance')
    )
    default_information_originate = attrs.ChoiceAttr(
        'default_information_originate', label=_('Default Information Originate')
    )
    default_information_metric = attrs.NumericAttr(
        'default_information_metric', label=_('Default Information Metric')
    )
    default_information_metric_type = attrs.ChoiceAttr(
        'default_information_metric_type',
        label=_('Default Information Metric Type'),
    )
    max_metric_router_lsa = attrs.BooleanAttr(
        'max_metric_router_lsa', label=_('Max Metric Router LSA')
    )
    max_metric_on_startup = attrs.NumericAttr(
        'max_metric_on_startup', label=_('Max Metric On Startup (s)')
    )


class OSPFAreaPanel(panels.ObjectAttributesPanel):
    area_id = attrs.NumericAttr('area_id', label=_('Area ID'))
    area_type = attrs.ChoiceAttr('area_type', label=_('Area Type'))
    description = attrs.TextAttr('description', label=_('Description'))


class OSPFInterfacePanel(panels.ObjectAttributesPanel):
    area = attrs.RelatedObjectAttr('area', label=_('Area'))
    device = attrs.RelatedObjectAttr('instance.device', label=_('Device'))
    instance = attrs.RelatedObjectAttr('instance', label=_('Instance'))
    interface = attrs.RelatedObjectAttr('interface', label=_('Interface'))


class OSPFInterfaceSettingsPanel(panels.ObjectAttributesPanel):
    network_type = attrs.ChoiceAttr('network_type', label=_('Network Type'))
    priority = attrs.NumericAttr('priority', label=_('Priority'))
    passive = attrs.BooleanAttr('passive', label=_('Passive'))
    bfd = attrs.BooleanAttr('bfd', label=_('BFD'))
    authentication = attrs.ChoiceAttr('authentication', label=_('Authentication'))
    passphrase = attrs.TextAttr('passphrase', label=_('Passphrase'))
