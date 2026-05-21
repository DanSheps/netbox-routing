from django.utils.translation import gettext_lazy as _

from netbox.ui import attrs, panels

__all__ = (
    'CustomPrefixPanel',
    'ASPathPanel',
    'ASPathEntryPanel',
    'PrefixListPanel',
    'PrefixListEntryPanel',
    'RouteMapPanel',
    'RouteMapEntryPanel',
    'RouteMapEntryMatchPanel',
    'RouteMapEntrySetPanel',
)


class CustomPrefixPanel(panels.ObjectAttributesPanel):
    prefix = attrs.TextAttr('prefix', label=_('Prefix'))
    description = attrs.TextAttr('description', label=_('Description'))


class ASPathPanel(panels.ObjectAttributesPanel):
    name = attrs.TextAttr('name', label=_('Name'))
    description = attrs.TextAttr('description', label=_('Description'))


class ASPathEntryPanel(panels.ObjectAttributesPanel):
    name = attrs.TextAttr('name', label=_('Name'))
    sequence = attrs.NumericAttr('sequence', label=_('Sequence'))
    action = attrs.ChoiceAttr('action', label=_('Action'))
    pattern = attrs.TextAttr('pattern', label=_('Pattern'))
    description = attrs.TextAttr('description', label=_('Description'))


class PrefixListPanel(panels.ObjectAttributesPanel):
    name = attrs.TextAttr('name', label=_('Name'))
    family = attrs.ChoiceAttr('family', label=_('Family'))
    description = attrs.TextAttr('description', label=_('Description'))


class PrefixListEntryPanel(panels.ObjectAttributesPanel):
    name = attrs.TextAttr('name', label=_('Name'))
    sequence = attrs.NumericAttr('sequence', label=_('Sequence'))
    action = attrs.ChoiceAttr('action', label=_('Action'))
    assigned_prefix = attrs.RelatedObjectAttr(
        'assigned_prefix', linkify=True, label=_('Prefix')
    )
    le = attrs.NumericAttr('le', label=_('Less Then'))
    ge = attrs.NumericAttr('ge', label=_('Greater Then'))
    description = attrs.TextAttr('description', label=_('Description'))


class RouteMapPanel(panels.ObjectAttributesPanel):
    name = attrs.TextAttr('name', label=_('Name'))
    description = attrs.TextAttr('description', label=_('Description'))


class RouteMapEntryPanel(panels.ObjectAttributesPanel):
    name = attrs.TextAttr('name', label=_('Name'))
    sequence = attrs.NumericAttr('sequence', label=_('Sequence'))
    action = attrs.ChoiceAttr('action', label=_('Action'))
    flow_control = attrs.NumericAttr('flow_control', label=_('Flow Control'))
    description = attrs.TextAttr('description', label=_('Description'))


class RouteMapEntryMatchPanel(panels.ObjectAttributesPanel):
    match_prefix_list = attrs.RelatedObjectListAttr(
        'match_prefix_list', linkify=True, label=_('Prefix List')
    )
    match_aspath = attrs.RelatedObjectListAttr(
        'match_as_path_list', linkify=True, label=_('AS Path List')
    )
    match_community_list = attrs.RelatedObjectListAttr(
        'match_community_list', linkify=True, label=_('Community List')
    )
    match_community = attrs.RelatedObjectListAttr(
        'match_community', linkify=True, label=_('Community')
    )


class RouteMapEntrySetPanel(panels.ObjectAttributesPanel):
    pass
