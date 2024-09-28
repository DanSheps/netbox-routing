from django import forms
from django.utils.translation import gettext as _

from dcim.models import Interface, Device
from ipam.models import VRF
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

from utilities.forms.rendering import FieldSet


class OSPFInstanceFilterForm(NetBoxModelFilterSetForm):
    device = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
        label=_('Device'),
    )
    vrf = DynamicModelMultipleChoiceField(
        queryset=VRF.objects.all(),
        required=False,
        selector=True,
        label=_('VRF'),
    )
    model = OSPFInstance
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag', 'device'),
    )
    tag = TagFilterField(model)


class OSPFAreaFilterForm(NetBoxModelFilterSetForm):
    model = OSPFArea
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
    )
    tag = TagFilterField(model)


class OSPFInterfaceFilterForm(NetBoxModelFilterSetForm):
    model = OSPFInterface
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
        FieldSet('instance', 'area', name=_('OSPF')),
        FieldSet('interface', name=_('Device')),
        FieldSet('priority', 'bfd', 'authentication', name=_('Attributes'))
    )
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
        label=_('Device'),
    )
    vrf_id = DynamicModelMultipleChoiceField(
        queryset=VRF.objects.all(),
        required=False,
        selector=True,
        label=_('VRF'),
    )
    instance_id = DynamicModelMultipleChoiceField(
        queryset=OSPFInstance.objects.all(),
        required=False,
        selector=True,
        label=_('Instance'),
    )
    area_id = DynamicModelMultipleChoiceField(
        queryset=OSPFArea.objects.all(),
        required=False,
        selector=True,
        label=_('Area'),
    )
    interface_id = DynamicModelMultipleChoiceField(
        queryset=Interface.objects.all(),
        required=False,
        selector=True,
        label=_('Interface'),
    )
    passive = forms.NullBooleanField(
        required=False,
        label='Passive Interface',
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
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
