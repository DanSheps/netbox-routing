from ipam.models import VRF
from dcim.models import Device
from netbox.forms import NetBoxModelFilterSetForm
from netbox_routing.models import StaticRoute
from utilities.forms.fields import DynamicModelMultipleChoiceField, TagFilterField
from django.utils.translation import gettext as _

from utilities.forms.rendering import FieldSet
from django import forms


class StaticRouteFilterForm(NetBoxModelFilterSetForm):
    model = StaticRoute
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
        FieldSet(
            'device_id',
            'vrf_id',
            'prefix',
            'next_hop',
            'name',
            name=_('Route Attributes'),
        ),
    )
    vrf_id = DynamicModelMultipleChoiceField(
        queryset=VRF.objects.all(),
        required=False,
        selector=True,
        label=_('VRF'),
    )
    prefix = forms.CharField(
        required=False,
        label=_('Prefix'),
    )

    next_hop = forms.CharField(
        required=False,
        label=_('Next Hop'),
    )

    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
        label=_('Device'),
    )

    name = forms.CharField(
        required=False,
        label=_('Name'),
    )
    tag = TagFilterField(model)
