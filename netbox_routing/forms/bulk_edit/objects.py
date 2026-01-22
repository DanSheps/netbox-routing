from django.utils.translation import gettext as _

from netbox.forms import NetBoxModelBulkEditForm
from utilities.forms.fields import DynamicModelChoiceField
from utilities.forms.rendering import FieldSet

from netbox_routing.models.objects import *


__all__ = (
    'PrefixListEntryBulkEditForm',
    'RouteMapEntryBulkEditForm',
    'ASPathBulkEditForm',
    'ASPathEntryBulkEditForm',
)


class PrefixListEntryBulkEditForm(NetBoxModelBulkEditForm):
    prefix_list = DynamicModelChoiceField(
        queryset=PrefixList.objects.all(),
        label=_('Prefix List'),
        required=False,
        selector=True,
    )

    model = PrefixListEntry
    fieldsets = (FieldSet('prefix_list'),)
    nullable_fields = ()


class RouteMapEntryBulkEditForm(NetBoxModelBulkEditForm):
    route_map = DynamicModelChoiceField(
        queryset=RouteMap.objects.all(),
        label=_('Route Map'),
        required=False,
        selector=True,
    )

    model = RouteMapEntry
    fieldsets = (FieldSet('route_map'),)
    nullable_fields = ()


class ASPathBulkEditForm(NetBoxModelBulkEditForm):

    model = ASPath
    fieldsets = ()
    nullable_fields = ()


class ASPathEntryBulkEditForm(NetBoxModelBulkEditForm):
    aspath = DynamicModelChoiceField(
        queryset=ASPath.objects.all(),
        label=_('AS Path'),
        required=False,
        selector=True,
    )

    model = ASPathEntry
    fieldsets = (FieldSet('aspath'),)
    nullable_fields = ()
