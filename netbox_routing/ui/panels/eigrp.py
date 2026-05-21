from django.utils.translation import gettext_lazy as _

from netbox.ui import attrs, panels

__all__ = (
    'EIGRPRouterPanel',
    'EIGRPAddressFamilyPanel',
    'EIGRPNetworkPanel',
    'EIGRPInterfacePanel',
)


class EIGRPRouterPanel(panels.ObjectAttributesPanel):
    device = attrs.RelatedObjectAttr('device', label=_('Device'))
    mode = attrs.ChoiceAttr('mode', label=_('Mode'))
    name = attrs.TextAttr('__str__', label=_('Display Name'))
    process_id = attrs.NumericAttr('process_id', label=_('Process ID'))
    router_id = attrs.TextAttr('router_id', label=_('Router ID'))
    description = attrs.TextAttr('description', label=_('Description'))


class EIGRPAddressFamilyPanel(panels.ObjectAttributesPanel):
    scope = attrs.RelatedObjectAttr('router', linkify=True)
    address_family = attrs.ChoiceAttr('address_family', label=_('Address Family'))
    description = attrs.TextAttr('description', label=_('Description'))


class EIGRPNetworkPanel(panels.ObjectAttributesPanel):
    router = attrs.RelatedObjectAttr('router', linkify=True)
    address_family = attrs.RelatedObjectAttr('address_family', linkify=True)
    network = attrs.RelatedObjectAttr('network', linkify=True)
    description = attrs.TextAttr('description', label=_('Description'))


class EIGRPInterfacePanel(panels.ObjectAttributesPanel):
    device = attrs.RelatedObjectAttr('device', label=_('Device'))
    router = attrs.RelatedObjectAttr('router', linkify=True)
    address_family = attrs.RelatedObjectAttr('address_family', linkify=True)
    interface = attrs.RelatedObjectAttr('interface', label=_('Interface'))
    description = attrs.TextAttr('description', label=_('Description'))


class EIGRPInterfaceSettingsPanel(panels.ObjectAttributesPanel):
    passive_interface = attrs.BooleanAttr(
        'passive_interface', label=_('Passive Interface')
    )
    bfd = attrs.BooleanAttr('bfd', label=_('BFD'))
    authentication = attrs.ChoiceAttr('authentication', label=_('Authentication'))
    passphrase = attrs.TextAttr('passphrase', label=_('Passphrase'))
