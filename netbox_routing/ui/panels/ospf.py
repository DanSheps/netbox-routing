from django.utils.translation import gettext_lazy as _

from netbox.ui import attrs, panels

__all__ = (
    'OSPFInstancePanel',
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
    priority = attrs.NumericAttr('priority', label=_('Priority'))
    passive = attrs.BooleanAttr('passive', label=_('Passive'))
    bfd = attrs.BooleanAttr('bfd', label=_('BFD'))
    authentication = attrs.ChoiceAttr('authentication', label=_('Authentication'))
    passphrase = attrs.TextAttr('passphrase', label=_('Passphrase'))
