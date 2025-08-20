from django.utils.translation import gettext as _

from dcim.models import Device
from ipam.models import VRF
from netbox.forms import NetBoxModelImportForm
from utilities.forms.fields import CSVModelChoiceField

from netbox_routing.models import StaticRoute


__all__ = ("StaticRouteImportForm",)


class StaticRouteImportForm(NetBoxModelImportForm):
    device = CSVModelChoiceField(
        queryset=Device.objects.all(),
        required=True,
        to_field_name="name",
        help_text=_("Name of device"),
    )
    vrf = CSVModelChoiceField(
        queryset=VRF.objects.all(),
        required=False,
        to_field_name="name",
        help_text=_("Name of VRF"),
    )

    class Meta:
        model = StaticRoute
        fields = (
            "name",
            "device",
            "vrf",
            "prefix",
            "next_hop",
            "metric",
            "permanent",
            "description",
            "comments",
            "tags",
        )
