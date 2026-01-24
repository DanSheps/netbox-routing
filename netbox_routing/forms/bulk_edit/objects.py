from django.utils.translation import gettext as _

from netbox.forms import NetBoxModelBulkEditForm
from utilities.forms.fields import DynamicModelChoiceField
from utilities.forms.rendering import FieldSet

from netbox_routing.models.objects import *

__all__ = (
    'PrefixListBulkEditForm',
    'PrefixListEntryBulkEditForm',
    'RouteMapBulkEditForm',
    'RouteMapEntryBulkEditForm',
    'ASPathBulkEditForm',
    'ASPathEntryBulkEditForm',
)


class PrefixListBulkEditForm(NetBoxModelBulkEditForm):

    model = PrefixList
    fieldsets = (
        FieldSet(
            'description',
        ),
    )
    nullable_fields = ('description',)


class PrefixListEntryBulkEditForm(NetBoxModelBulkEditForm):
    prefix_list = DynamicModelChoiceField(
        queryset=PrefixList.objects.all(),
        label=_('Prefix List'),
        required=False,
        selector=True,
    )

    model = PrefixListEntry
    fieldsets = (
        FieldSet(
            'prefix_list',
            'description',
        ),
    )
    nullable_fields = ('description',)


class RouteMapBulkEditForm(NetBoxModelBulkEditForm):

    model = RouteMap
    fieldsets = (
        FieldSet(
            'description',
        ),
    )
    nullable_fields = ('description',)


class RouteMapEntryBulkEditForm(NetBoxModelBulkEditForm):
    route_map = DynamicModelChoiceField(
        queryset=RouteMap.objects.all(),
        label=_('Route Map'),
        required=False,
        selector=True,
    )

    model = RouteMapEntry
    fieldsets = (
        FieldSet(
            'route_map',
            'description',
        ),
    )
    nullable_fields = ('description',)


class ASPathBulkEditForm(NetBoxModelBulkEditForm):

    model = ASPath
    fieldsets = (
        FieldSet(
            'description',
        ),
    )
    nullable_fields = ('description',)


class ASPathEntryBulkEditForm(NetBoxModelBulkEditForm):
    aspath = DynamicModelChoiceField(
        queryset=ASPath.objects.all(),
        label=_('AS Path'),
        required=False,
        selector=True,
    )

    model = ASPathEntry
    fieldsets = (
        FieldSet(
            'aspath',
            'description',
        ),
    )
    nullable_fields = ('description',)
