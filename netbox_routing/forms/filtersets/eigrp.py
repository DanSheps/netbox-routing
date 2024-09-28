from django import forms
from django.utils.translation import gettext as _

from dcim.models import Interface, Device
from ipam.choices import IPAddressFamilyChoices
from ipam.forms.filtersets import PREFIX_MASK_LENGTH_CHOICES
from ipam.models import VRF, Prefix
from netbox.forms import NetBoxModelFilterSetForm
from netbox_routing.choices import AuthenticationChoices
from utilities.forms import BOOLEAN_WITH_BLANK_CHOICES, add_blank_choice
from utilities.forms.fields import TagFilterField, DynamicModelMultipleChoiceField, DynamicModelChoiceField
from utilities.forms.rendering import FieldSet

from netbox_routing.models import EIGRPRouter, EIGRPAddressFamily, EIGRPNetwork, EIGRPInterface


__all__ = (
    'EIGRPRouterFilterForm',
    'EIGRPAddressFamilyFilterForm',
    'EIGRPNetworkFilterForm',
    'EIGRPInterfaceFilterForm',
)


class EIGRPRouterFilterForm(NetBoxModelFilterSetForm):
    model = EIGRPRouter
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag', 'device', 'mode'),
    )

    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
        label=_('Device'),
    )
    tag = TagFilterField(model)


class EIGRPAddressFamilyFilterForm(NetBoxModelFilterSetForm):
    model = EIGRPAddressFamily
    fieldsets = (
        FieldSet('q', 'filter_id', 'router_id', 'vrf_id', 'family', 'tag'),
    )

    router_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
        label=_('EIGRP Router'),
    )
    vrf_id = DynamicModelMultipleChoiceField(
        queryset=VRF.objects.all(),
        required=False,
        selector=True,
        label=_('VRF'),
    )
    family = forms.ChoiceField(
        required=False,
        choices=add_blank_choice(IPAddressFamilyChoices),
        label=_('Address family')
    )
    tag = TagFilterField(model)


class EIGRPNetworkFilterForm(NetBoxModelFilterSetForm):
    model = EIGRPNetwork
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
        FieldSet('router_id', 'address_family', name=_('EIGRP')),
        FieldSet(
            'prefix_id', 'vrf_id', 'present_in_vrf_id', 'family', 'mask_length__lte', 'within_include',
            'mask_length', name=_('Prefix')
        ),
    )
    prefix_id = DynamicModelMultipleChoiceField(
        queryset=Prefix.objects.all(),
        required=False,
        selector=True,
        label=_('Prefix'),
    )
    router_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
        label=_('EIGRP Router'),
    )
    address_family_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
        label=_('EIGRP Address Family'),
    )
    vrf_id = DynamicModelMultipleChoiceField(
        queryset=VRF.objects.all(),
        required=False,
        label=_('Assigned VRF'),
        null_option='Global'
    )
    present_in_vrf_id = DynamicModelChoiceField(
        queryset=VRF.objects.all(),
        required=False,
        label=_('Present in VRF')
    )
    family = forms.ChoiceField(
        required=False,
        choices=add_blank_choice(IPAddressFamilyChoices),
        label=_('Address family')
    )
    mask_length__lte = forms.IntegerField(
        widget=forms.HiddenInput()
    )
    within_include = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Prefix',
            }
        ),
        label=_('Search within')
    )
    mask_length = forms.MultipleChoiceField(
        required=False,
        choices=PREFIX_MASK_LENGTH_CHOICES,
        label=_('Mask length')
    )
    tag = TagFilterField(model)


class EIGRPInterfaceFilterForm(NetBoxModelFilterSetForm):
    model = EIGRPInterface
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
        FieldSet('router_id', 'address_family_id', name=_('EIGRP')),
        FieldSet('device_id', 'interface_id', name=_('Device')),
        FieldSet('passive', 'bfd', 'authentication', name=_('Attributes'))
    )
    router_id = DynamicModelMultipleChoiceField(
        queryset=EIGRPRouter.objects.all(),
        required=False,
        selector=True,
        label=_('EIGRP Router'),
    )
    address_family_id = DynamicModelMultipleChoiceField(
        queryset=EIGRPAddressFamily.objects.all(),
        required=False,
        selector=True,
        label=_('EIGRP Address Family'),
    )
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
        label=_('Device'),
    )
    interface_id = DynamicModelMultipleChoiceField(
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
    passive = forms.BooleanField(
        required=False,
        label='Passive Interface',
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    authentication = forms.ChoiceField(
        choices=add_blank_choice(AuthenticationChoices),
        required=False
    )
    tag = TagFilterField(model)
