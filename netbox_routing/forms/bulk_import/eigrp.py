from django.utils.translation import gettext as _

from dcim.models import Interface
from ipam.models import Prefix
from netbox.forms import NetBoxModelImportForm
from utilities.forms.fields import CSVModelChoiceField

from netbox_routing.models import *


__all__ = (
    'EIGRPRouterImportForm',
    'EIGRPAddressFamilyImportForm',
    'EIGRPNetworkImportForm',
    'EIGRPInterfaceImportForm',
)


class EIGRPRouterImportForm(NetBoxModelImportForm):
    device = CSVModelChoiceField(
        queryset=Interface.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Name of device')
    )

    class Meta:
        model = EIGRPRouter
        fields = ('device', 'rid', 'mode', 'name', 'pid', 'description', 'comments', 'tags',)


class EIGRPAddressFamilyImportForm(NetBoxModelImportForm):

    class Meta:
        model = EIGRPAddressFamily
        fields = ('router', 'family', 'rid', 'description', 'comments', 'tags',)


class EIGRPNetworkImportForm(NetBoxModelImportForm):
    router = CSVModelChoiceField(
        queryset=EIGRPRouter.objects.all(),
        required=True,
        help_text=_('PK of Router Instance')
    )
    address_family = CSVModelChoiceField(
        queryset=EIGRPAddressFamily.objects.all(),
        required=False,
        help_text=_('PK of Address Family')
    )
    network = CSVModelChoiceField(
        queryset=Prefix.objects.all(),
        required=True,
        to_field_name='prefix',
        help_text=_('Prefix of Network')
    )

    class Meta:
        model = EIGRPNetwork
        fields = ('router', 'address_family', 'network', 'description', 'comments', 'tags',)


class EIGRPInterfaceImportForm(NetBoxModelImportForm):
    router = CSVModelChoiceField(
        queryset=EIGRPRouter.objects.all(),
        required=True,
        help_text=_('PK of Router Instance')
    )
    address_family = CSVModelChoiceField(
        queryset=EIGRPAddressFamily.objects.all(),
        required=False,
        help_text=_('PK of Address Family')
    )
    interface = CSVModelChoiceField(
        queryset=Interface.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Name of interface')
    )

    class Meta:
        model = EIGRPInterface
        fields = ('router', 'address_family', 'interface', 'description', 'comments', 'tags',)
