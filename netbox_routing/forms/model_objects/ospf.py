from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.forms import ChoiceField

from dcim.models import Interface, Device
from ipam.models import VRF
from netbox.forms import NetBoxModelForm
from utilities.forms import BOOLEAN_WITH_BLANK_CHOICES
from utilities.forms.fields import DynamicModelChoiceField, CommentField
from utilities.forms.rendering import FieldSet

from netbox_routing.choices import OSPFNetworkTypeChoices
from netbox_routing.models import OSPFArea, OSPFInstance, OSPFInterface

__all__ = (
    'OSPFAreaForm',
    'OSPFInstanceForm',
    'OSPFInterfaceForm',
)


class OSPFInstanceForm(NetBoxModelForm):
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=True,
        selector=True,
        label=_('Device'),
    )
    vrf = DynamicModelChoiceField(
        queryset=VRF.objects.all(),
        required=False,
        selector=True,
        label=_('VRF'),
    )
    comments = CommentField()

    fieldsets = (
        FieldSet(
            'name',
            'description',
        ),
        FieldSet(
            'device',
            name=_('Device'),
        ),
        FieldSet(
            'process_id',
            'router_id',
            'vrf',
            name=_('Instance'),
        ),
    )

    class Meta:
        model = OSPFInstance
        fields = (
            'name',
            'router_id',
            'process_id',
            'device',
            'vrf',
            'description',
            'comments',
        )


class OSPFAreaForm(NetBoxModelForm):
    comments = CommentField()

    class Meta:
        model = OSPFArea
        fields = (
            'area_id',
            'area_type',
            'description',
            'comments',
        )


class OSPFInterfaceForm(NetBoxModelForm):
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
        label=_('Device'),
    )
    instance = DynamicModelChoiceField(
        queryset=OSPFInstance.objects.all(),
        required=True,
        selector=True,
        label=_('Instance'),
        query_params={
            'device_id': '$device',
        },
    )
    area = DynamicModelChoiceField(
        queryset=OSPFArea.objects.all(),
        required=True,
        selector=True,
        label=_('Area'),
    )
    interface = DynamicModelChoiceField(
        queryset=Interface.objects.all(),
        required=True,
        selector=True,
        label=_('Interface'),
        query_params={
            'device_id': '$device',
        },
    )
    network_type = ChoiceField(
        choices=OSPFNetworkTypeChoices,
        required=True,
        label=_('Network Type'),
    )
    comments = CommentField()

    fieldsets = (
        FieldSet(
            'area',
            'description',
            name=_('Session'),
        ),
        FieldSet(
            'device',
            'instance',
            name=_('Instance'),
        ),
        FieldSet(
            'interface',
            'network_type',
            'priority',
            'passive',
            'bfd',
            name=_('Interface'),
        ),
        FieldSet(
            'authentication',
            'passphrase',
            name=_('Authentication'),
        ),
    )

    class Meta:
        model = OSPFInterface
        fields = (
            'device',
            'instance',
            'area',
            'interface',
            'network_type',
            'passive',
            'priority',
            'bfd',
            'authentication',
            'passphrase',
            'description',
            'comments',
        )

        widgets = {
            'bfd': forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
            'passive': forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial['device'] = self.instance.interface.device.pk

    def clean(self):
        super().clean()
        if self.cleaned_data.get('instance') and self.cleaned_data.get('interface'):
            if (
                self.cleaned_data.get('instance').device
                != self.cleaned_data.get('interface').device
            ):
                raise ValidationError(
                    {
                        'instance': _(
                            'OSPF Instance Device and Interface Device must match'
                        ),
                        'interface': _(
                            'OSPF Instance Device and Interface Device must match'
                        ),
                    }
                )
