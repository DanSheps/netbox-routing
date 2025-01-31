from django import forms
from django.utils.translation import gettext as _

from dcim.models import Device
from ipam.models import VRF
from netbox.forms import NetBoxModelBulkEditForm, NetBoxModelImportForm
from utilities.forms import BOOLEAN_WITH_BLANK_CHOICES
from utilities.forms.fields import DynamicModelChoiceField, DynamicModelMultipleChoiceField, CommentField, \
    CSVModelMultipleChoiceField, CSVModelChoiceField
from utilities.forms.rendering import FieldSet

from netbox_routing.models import StaticRoute


__all__ = (
    'StaticRouteBulkImportForm',
)


class StaticRouteBulkImportForm(NetBoxModelImportForm):
    devices = CSVModelMultipleChoiceField(
        label=_('Device'),
        queryset=Device.objects.all(),
        required=False,
    )
    vrf = CSVModelChoiceField(
        label=_('VRF'),
        queryset=VRF.objects.all(),
        to_field_name='rd',
        required=False,
    )


    class Meta:
        model = StaticRoute
        fields = (
            'devices', 'vrf', 'prefix', 'next_hop', 'name', 'metric', 'permanent', 'description', 'comments', 'tags',
        )
