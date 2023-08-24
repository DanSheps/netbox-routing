from django.utils.translation import gettext as _

from dcim.models import Interface
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
        queryset=Interface.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Name of device')
    )

    class Meta:
        model = OSPFInstance
        fields = ('name', 'router_id', 'process_id', 'device', 'tags')


class OSPFAreaImportForm(NetBoxModelImportForm):

    class Meta:
        model = OSPFArea
        fields = ('area_id', 'tags')


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
        fields = ('instance', 'area', 'interface', 'tags')
