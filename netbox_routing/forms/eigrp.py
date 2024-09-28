from django import forms
from django.core.exceptions import ValidationError
from django.forms import ChoiceField
from django.utils.translation import gettext as _

from dcim.models import Interface, Device
from ipam.choices import IPAddressFamilyChoices
from ipam.models import VRF, Prefix
from netbox.forms import NetBoxModelForm
from netbox_routing.choices.eigrp import EIGRPRouterChoices
from utilities.forms import BOOLEAN_WITH_BLANK_CHOICES, get_field_value
from utilities.forms.fields import DynamicModelChoiceField, CommentField
from utilities.forms.widgets import HTMXSelect

from netbox_routing.models import *


__all__ = (
    'EIGRPRouterForm',
    'EIGRPAddressFamilyForm',
    'EIGRPNetworkForm',
    'EIGRPInterfaceForm',
)


class EIGRPRouterForm(NetBoxModelForm):
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=True,
        selector=True,
        label=_('Device'),
    )
    comments = CommentField()

    class Meta:
        model = EIGRPRouter
        fields = ('device', 'mode', 'name', 'pid', 'rid', 'description', 'comments', )
        widgets = {
            'mode': HTMXSelect(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        mode = get_field_value(self, 'mode')
        if mode == EIGRPRouterChoices.NAMED:
            del self.fields['pid']
        elif mode == EIGRPRouterChoices.CLASSIC:
            del self.fields['name']


class EIGRPAddressFamilyForm(NetBoxModelForm):
    router = DynamicModelChoiceField(
        queryset=EIGRPRouter.objects.all(),
        required=True,
        selector=True,
        label=_('Router'),
    )
    vrf = DynamicModelChoiceField(
        queryset=VRF.objects.all(),
        required=False,
        selector=True,
        label=_('VRF'),
    )
    family = ChoiceField(
        required=True,
        choices=IPAddressFamilyChoices,
        label=_('Family'),
    )
    comments = CommentField()


    class Meta:
        model = EIGRPAddressFamily
        fields = (
            'router', 'vrf', 'family', 'rid', 'description', 'comments',
        )


class EIGRPNetworkForm(NetBoxModelForm):
    router = DynamicModelChoiceField(
        queryset=EIGRPRouter.objects.all(),
        required=True,
        selector=True,
        label=_('Router'),
    )
    address_family = DynamicModelChoiceField(
        queryset=EIGRPAddressFamily.objects.all(),
        required=False,
        selector=True,
        label=_('Address Family'),
    )
    network = DynamicModelChoiceField(
        queryset=Prefix.objects.all(),
        required=True,
        selector=True,
        label=_('Prefix'),
    )
    comments = CommentField()


    class Meta:
        model = EIGRPNetwork
        fields = (
            'router', 'address_family', 'network', 'description', 'comments',
        )


class EIGRPInterfaceForm(NetBoxModelForm):
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
        label=_('Device'),
    )
    router = DynamicModelChoiceField(
        queryset=EIGRPRouter.objects.all(),
        required=True,
        selector=True,
        label=_('EIGRP Router'),
        query_params={
            'device_id': '$device',
        }
    )
    address_family = DynamicModelChoiceField(
        queryset=EIGRPAddressFamily.objects.all(),
        required=False,
        selector=True,
        label=_('Address Family'),
        query_params={
            'router_id': '$router',
        }
    )
    interface = DynamicModelChoiceField(
        queryset=Interface.objects.all(),
        required=True,
        selector=True,
        label=_('Interface'),
        query_params={
            'device_id': '$device',
        }
    )
    passive = forms.BooleanField(
        required=False,
        label='Passive Interface',
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    comments = CommentField()


    class Meta:
        model = EIGRPInterface
        fields = (
            'device', 'router', 'address_family', 'interface', 'passive', 'bfd', 'authentication', 'passphrase',
            'description', 'comments',
        )

        widgets = {
            'bfd': forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial['device'] = self.instance.interface.device.pk

    def clean(self):
        super().clean()
        if self.cleaned_data.get('router') and self.cleaned_data.get('address_family'):
            if self.cleaned_data.get('router') != self.cleaned_data.get('address_family').router:
                raise ValidationError(
                    {
                        'router': _('EIGRP Router and EIGRP Address Family Router must match'),
                        'interface': _('EIGRP Router and EIGRP Address Family Router must match')
                    }
                )
        if self.cleaned_data.get('router') and self.cleaned_data.get('interface'):
            if self.cleaned_data.get('router').device != self.cleaned_data.get('interface').device:
                raise ValidationError(
                    {
                        'router': _('EIGRP Router Device and Interface Device must match'),
                        'interface': _('EIGRP Interface Device and Interface Device must match')
                    }
                )
