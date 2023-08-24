from django.utils.translation import gettext as _

from netbox.forms import NetBoxModelBulkEditForm
from netbox_routing.models import OSPFArea, OSPFInstance, OSPFInterface
from utilities.forms.fields import DynamicModelChoiceField


__all__ = (
    'OSPFInterfaceBulkEditForm',
)


class OSPFInterfaceBulkEditForm(NetBoxModelBulkEditForm):
    instance = DynamicModelChoiceField(
        queryset=OSPFInstance.objects.all(),
        label=_('Route Map'),
        required=False,
        selector=True
    )
    area = DynamicModelChoiceField(
        queryset=OSPFArea.objects.all(),
        label=_('Route Map'),
        required=False,
        selector=True
    )

    model = OSPFInterface
    fieldsets = (
        ('OSPF', ('instance', 'area')),
        ('Attributes', ('priority', 'bfd', 'authentication', 'passphrase')),
    )
    nullable_fields = ()
