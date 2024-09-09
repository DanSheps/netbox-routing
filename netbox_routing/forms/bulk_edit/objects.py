
from django.utils.translation import gettext as _

from netbox.forms import NetBoxModelBulkEditForm
from netbox_routing.models import PrefixList, PrefixListEntry, RouteMapEntry, RouteMap
from utilities.forms.fields import DynamicModelChoiceField


__all__ = (
    'PrefixListEntryBulkEditForm',
    'RouteMapEntryBulkEditForm'
)

from utilities.forms.rendering import FieldSet


class PrefixListEntryBulkEditForm(NetBoxModelBulkEditForm):
    prefix_list = DynamicModelChoiceField(
        queryset=PrefixList.objects.all(),
        label=_('Prefix List'),
        required=False,
        selector=True
    )

    model = PrefixListEntry
    fieldsets = (
       FieldSet('prefix_list'),
    )
    nullable_fields = ()


class RouteMapEntryBulkEditForm(NetBoxModelBulkEditForm):
    route_map = DynamicModelChoiceField(
        queryset=RouteMap.objects.all(),
        label=_('Route Map'),
        required=False,
        selector=True
    )

    model = RouteMapEntry
    fieldsets = (
       FieldSet('route_map'),
    )
    nullable_fields = ()
