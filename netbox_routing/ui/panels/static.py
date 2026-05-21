from django.utils.translation import gettext_lazy as _

from netbox.ui import attrs, panels

__all__ = (
    'StaticRoutePanel',
    'StaticRouteRoutePanel',
)


class StaticRoutePanel(panels.ObjectAttributesPanel):
    display = attrs.TextAttr('__str__', label=_('Display Name'))
    description = attrs.TextAttr('description', label=_('Description'))


class StaticRouteRoutePanel(panels.ObjectAttributesPanel):
    name = attrs.TextAttr('name', label=_('Route Name'))
    vrf = attrs.RelatedObjectAttr('vrf', linkify=True, label=_('VRF'))
    prefix = attrs.TextAttr('prefix', label=_('Prefix'))
    next_hop = attrs.TextAttr('next_hop', label=_('Next Hop'))
    interface_next_hop = attrs.TextAttr(
        'interface_next_hop', label=_('Interface Next Hop')
    )
    metric = attrs.TextAttr('metric', label=_('Metric'))
    tag = attrs.TextAttr('tag', label=_('Route Tag'))
    permanent = attrs.BooleanAttr('permanent', label=_('Permanent'))
