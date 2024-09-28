from django import forms
from django.forms import CharField
from django.utils.translation import gettext as _

from dcim.models import Device
from ipam.models import VRF
from netbox.forms import NetBoxModelBulkEditForm
from netbox_routing.models import EIGRPRouter, EIGRPAddressFamily, EIGRPNetwork, EIGRPInterface
from utilities.forms import BOOLEAN_WITH_BLANK_CHOICES, add_blank_choice
from utilities.forms.fields import DynamicModelChoiceField, CommentField
from utilities.forms.rendering import FieldSet

from netbox_routing import choices

__all__ = (
    'EIGRPRouterBulkEditForm',
    'EIGRPAddressFamilyBulkEditForm',
    'EIGRPNetworkBulkEditForm',
    'EIGRPInterfaceBulkEditForm',
)


class EIGRPRouterBulkEditForm(NetBoxModelBulkEditForm):
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        label=_('Device'),
        required=False,
        selector=True
    )

    description = forms.CharField(
        label=_('Description'),
        max_length=200,
        required=False
    )
    comments = CommentField()

    model = EIGRPRouter
    fieldsets = (
        FieldSet('device', 'mode', name='EIGRP'),
        FieldSet('description', ),
    )
    nullable_fields = ()


class EIGRPAddressFamilyBulkEditForm(NetBoxModelBulkEditForm):
    vrf = DynamicModelChoiceField(
        queryset=VRF.objects.all(),
        label=_('VRF'),
        required=False,
        selector=True
    )
    family = CharField(max_length=4)

    description = forms.CharField(
        label=_('Description'),
        max_length=200,
        required=False
    )
    comments = CommentField()

    model = EIGRPAddressFamily
    fieldsets = (
        FieldSet('description'),
    )
    nullable_fields = ()


class EIGRPNetworkBulkEditForm(NetBoxModelBulkEditForm):
    router = DynamicModelChoiceField(
        queryset=EIGRPRouter.objects.all(),
        label=_('Router'),
        required=False,
        selector=True
    )
    address_family = DynamicModelChoiceField(
        queryset=EIGRPAddressFamily.objects.all(),
        label=_('Router'),
        required=False,
        selector=True
    )

    description = forms.CharField(
        label=_('Description'),
        max_length=200,
        required=False
    )
    comments = CommentField()

    model = EIGRPNetwork
    fieldsets = (
        FieldSet('description'),
    )
    nullable_fields = ()


class EIGRPInterfaceBulkEditForm(NetBoxModelBulkEditForm):
    router = DynamicModelChoiceField(
        queryset=EIGRPRouter.objects.all(),
        label=_('EIGRP Router'),
        required=False,
        selector=True
    )
    address_family = DynamicModelChoiceField(
        queryset=EIGRPAddressFamily.objects.all(),
        label=_('EIGRP Address Family'),
        required=False,
        selector=True
    )
    passive = forms.ChoiceField(label=_('Passive'), choices=BOOLEAN_WITH_BLANK_CHOICES, required=False)
    bfd = forms.ChoiceField(label=_('BFD'), choices=BOOLEAN_WITH_BLANK_CHOICES, required=False)
    authentication = forms.ChoiceField(
        label=_('Authentication'),
        choices=add_blank_choice(choices.AuthenticationChoices),
        required=False
    )
    passphrase = forms.CharField(label=_('Passphrase'), required=False)

    description = forms.CharField(
        label=_('Description'),
        max_length=200,
        required=False
    )
    comments = CommentField()

    model = EIGRPInterface
    fieldsets = (
        FieldSet('router', 'address_family', name='EIGRP'),
        FieldSet('priority', 'bfd', 'authentication', 'passphrase', name='Attributes'),
        FieldSet('description'),
    )
    nullable_fields = ()
