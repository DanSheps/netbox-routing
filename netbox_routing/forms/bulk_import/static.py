from django.utils.translation import gettext as _

from dcim.models import Interface, Device
from ipam.models import VRF
from netbox.forms import NetBoxModelImportForm
from utilities.forms.fields import CSVModelChoiceField

from netbox_routing.models import StaticRoute


__all__ = (
    'StaticRouteImportForm',
)


class StaticRouteImportForm(NetBoxModelImportForm):
    device = CSVModelChoiceField(
        queryset=Device.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Name of device')
    )
    # vrf = CSVModelChoiceField(
    #     queryset=VRF.objects.all(),
    #     required=False,
    #     to_field_name='name',
    #     help_text=_('Name of VRF')
    # )

    # prefix = CSVModelChoiceField(
    #     queryset=VRF.objects.all(),
    #     required=True,
    #     to_field_name='prefix',
    #     help_text=_('IPv4 or IPv6 network with mask')
    # )
    # next_hop = CSVModelChoiceField(
    #     queryset=VRF.objects.all(),
    #     required=True,
    #     to_field_name='next_hop',
    #     help_text=_('Next hop IP address')
    # )
    
    class Meta:
        model = StaticRoute
        fields = ('name', 'device', 'vrf', 'prefix', 'next_hop', 'description', 'comments', 'tags',)
