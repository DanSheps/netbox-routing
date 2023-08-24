from django import forms
from django.utils.translation import gettext as _

from dcim.models import Interface, Device
from netbox.forms import NetBoxModelFilterSetForm
from netbox_routing.choices import AuthenticationChoices
from utilities.forms import BOOLEAN_WITH_BLANK_CHOICES, add_blank_choice
from utilities.forms.fields import TagFilterField, DynamicModelMultipleChoiceField

from netbox_routing.models import OSPFInstance, OSPFArea, OSPFInterface


__all__ = (
    'OSPFAreaFilterForm',
    'OSPFInstanceFilterForm',
    'OSPFInterfaceFilterForm',
)


class OSPFInstanceFilterForm(NetBoxModelFilterSetForm):
    device = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
        label=_('Device'),
    )
    model = OSPFInstance
    fieldsets = (
        (None, ('q', 'filter_id', 'tag', 'device')),
    )
    tag = TagFilterField(model)


class OSPFAreaFilterForm(NetBoxModelFilterSetForm):
    model = OSPFArea
    fieldsets = (
        (None, ('q', 'filter_id', 'tag', )),
    )
    tag = TagFilterField(model)


class OSPFInterfaceFilterForm(NetBoxModelFilterSetForm):
    model = OSPFInterface
    fieldsets = (
        (None, ('q', 'filter_id', 'tag', )),
        ('OSPF', ('instance', 'area')),
        ('Device', ('interface', )),
        ('Attributes', ('priority', 'bfd', 'authentication')),
    )
    instance = DynamicModelMultipleChoiceField(
        queryset=OSPFInstance.objects.all(),
        required=False,
        selector=True,
        label=_('Instance'),
    )
    area = DynamicModelMultipleChoiceField(
        queryset=OSPFArea.objects.all(),
        required=False,
        selector=True,
        label=_('Area'),
    )
    interface = DynamicModelMultipleChoiceField(
        queryset=Interface.objects.all(),
        required=False,
        selector=True,
        label=_('Interface'),
    )
    bfd = forms.NullBooleanField(
        required=False,
        label='BFD Enabled',
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    priority = forms.IntegerField(
        required=False
    )
    authentication = forms.ChoiceField(
        choices=add_blank_choice(AuthenticationChoices),
        required=False
    )
    tag = TagFilterField(model)
