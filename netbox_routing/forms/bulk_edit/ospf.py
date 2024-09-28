from django import forms
from django.utils.translation import gettext as _

from dcim.models import Device
from ipam.models import VRF
from netbox.forms import NetBoxModelBulkEditForm
from utilities.forms import BOOLEAN_WITH_BLANK_CHOICES, add_blank_choice
from utilities.forms.fields import DynamicModelChoiceField, CommentField

from netbox_routing import choices
from netbox_routing.models import OSPFArea, OSPFInstance, OSPFInterface

__all__ = (
    'OSPFInterfaceBulkEditForm',
    'OSPFInstanceBulkEditForm',
    'OSPFAreaBulkEditForm',
)

from utilities.forms.rendering import FieldSet


class OSPFInstanceBulkEditForm(NetBoxModelBulkEditForm):
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        label=_('Device'),
        required=False,
        selector=True
    )
    vrf = DynamicModelChoiceField(
        queryset=VRF.objects.all(),
        label=_('VRF'),
        required=False,
        selector=True
    )

    description = forms.CharField(
        label=_('Description'),
        max_length=200,
        required=False
    )
    comments = CommentField()

    model = OSPFInstance
    fieldsets = (
        FieldSet('device', 'vrf', name='OSPF'),
        FieldSet('description', ),
    )
    nullable_fields = ('vrf', 'description', )


class OSPFAreaBulkEditForm(NetBoxModelBulkEditForm):

    description = forms.CharField(
        label=_('Description'),
        max_length=200,
        required=False
    )
    comments = CommentField()

    model = OSPFArea
    fieldsets = (
        FieldSet('description'),
    )
    nullable_fields = ()


class OSPFInterfaceBulkEditForm(NetBoxModelBulkEditForm):
    instance = DynamicModelChoiceField(
        queryset=OSPFInstance.objects.all(),
        label=_('OSPF Instance'),
        required=False,
        selector=True
    )
    area = DynamicModelChoiceField(
        queryset=OSPFArea.objects.all(),
        label=_('OSPF Area'),
        required=False,
        selector=True
    )
    passive = forms.ChoiceField(label=_('Passive'), choices=BOOLEAN_WITH_BLANK_CHOICES, required=False)
    priority = forms.IntegerField(label=_('Priority'), required=False)
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

    model = OSPFInterface
    fieldsets = (
        FieldSet('instance', 'area', name='OSPF'),
        FieldSet('passive', 'priority', 'bfd', 'authentication', 'passphrase', name='Attributes'),
        FieldSet('description'),
    )
    nullable_fields = ()
