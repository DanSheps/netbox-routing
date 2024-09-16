from django import forms
from django.utils.translation import gettext as _

from netbox.forms import NetBoxModelBulkEditForm
from utilities.forms import BOOLEAN_WITH_BLANK_CHOICES, add_blank_choice
from utilities.forms.fields import DynamicModelChoiceField

from netbox_routing import choices
from netbox_routing.models import OSPFArea, OSPFInstance, OSPFInterface

__all__ = (
    'OSPFInterfaceBulkEditForm',
)

from utilities.forms.rendering import FieldSet


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
    priority = forms.IntegerField(label=_('Priority'), required=False)
    bfd = forms.ChoiceField(label=_('BFD'), choices=BOOLEAN_WITH_BLANK_CHOICES, required=False)
    authentication = forms.ChoiceField(
        label=_('Authentication'),
        choices=add_blank_choice(choices.AuthenticationChoices),
        required=False
    )
    passphrase = forms.CharField(label=_('Passphrase'), required=False)

    model = OSPFInterface
    fieldsets = (
        FieldSet('instance', 'area', name='OSPF'),
        FieldSet('priority', 'bfd', 'authentication', 'passphrase', name='Attributes'),
    )
    nullable_fields = ()
