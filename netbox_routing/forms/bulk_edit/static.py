from django import forms
from django.utils.translation import gettext as _

from dcim.models import Device
from ipam.models import VRF
from netbox.forms import NetBoxModelBulkEditForm
from utilities.forms import BOOLEAN_WITH_BLANK_CHOICES
from utilities.forms.fields import DynamicModelChoiceField, DynamicModelMultipleChoiceField, CommentField
from utilities.forms.rendering import FieldSet

from netbox_routing.models import StaticRoute


__all__ = (
    'StaticRouteBulkEditForm',
)


class StaticRouteBulkEditForm(NetBoxModelBulkEditForm):
    devices = DynamicModelMultipleChoiceField(
        label='Device',
        queryset=Device.objects.all(),
        required=False,
        selector=True,
    )
    vrf = DynamicModelChoiceField(
        label='VRF',
        queryset=VRF.objects.all(),
        required=False,
        selector=True,
    )
    metric = forms.IntegerField(label=_('Metric'), required=False)
    permanent = forms.ChoiceField(label=_('Permanent'), choices=BOOLEAN_WITH_BLANK_CHOICES, required=False)

    description = forms.CharField(
        label=_('Description'),
        max_length=200,
        required=False
    )
    comments = CommentField()

    model = StaticRoute
    fieldsets = (
        FieldSet('devices', 'vrf', 'prefix', 'next_hop', name='Route'),
        FieldSet('metric', 'permanent', name='Attributes'),
        FieldSet('description', )
    )
    nullable_fields = ('devices', 'vrf', 'metric', 'permanent', 'description', 'comments')
