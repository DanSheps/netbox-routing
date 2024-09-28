from django.utils.translation import gettext as _

from dcim.models import Interface, Device
from ipam.models import VRF
from netbox.forms import NetBoxModelImportForm
from utilities.forms.fields import CSVModelChoiceField

from netbox_routing.models import OSPFInstance, OSPFArea, OSPFInterface


__all__ = (
    'OSPFInstanceImportForm',
    'OSPFAreaImportForm',
    'OSPFInterfaceImportForm',
)


class OSPFInstanceImportForm(NetBoxModelImportForm):
    device = CSVModelChoiceField(
        queryset=Device.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Name of device')
    )
    vrf = CSVModelChoiceField(
        queryset=VRF.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Name of VRF')
    )

    class Meta:
        model = OSPFInstance
        fields = ('name', 'router_id', 'process_id', 'device', 'vrf', 'description', 'comments', 'tags',)


class OSPFAreaImportForm(NetBoxModelImportForm):

    class Meta:
        model = OSPFArea
        fields = ('area_id', 'description', 'comments', 'tags',)


class OSPFInterfaceImportForm(NetBoxModelImportForm):
    instance = CSVModelChoiceField(
        queryset=OSPFInstance.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Name of OSPF Instance')
    )
    area = CSVModelChoiceField(
        queryset=OSPFArea.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Area ID')
    )
    interface = CSVModelChoiceField(
        queryset=Interface.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Name of interface')
    )

    class Meta:
        model = OSPFInterface
        fields = ('instance', 'area', 'interface', 'passive', 'description', 'comments', 'tags',)
