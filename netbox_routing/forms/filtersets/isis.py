# SPDX-License-Identifier: Apache-2.0

from django import forms
from django.utils.translation import gettext_lazy as _

from dcim.models import Device, Interface
from ipam.models import VRF
from netbox.forms import NetBoxModelFilterSetForm
from utilities.forms import BOOLEAN_WITH_BLANK_CHOICES, add_blank_choice
from utilities.forms.fields import DynamicModelMultipleChoiceField, TagFilterField
from utilities.forms.rendering import FieldSet

from netbox_routing.choices import (
    ISISAddressFamilyChoices,
    ISISAuthTypeChoices,
    ISISCircuitTypeChoices,
    ISISIsTypeChoices,
    ISISNetworkTypeChoices,
)
from netbox_routing.models import (
    ISISInstance,
    ISISInterface,
    ISISSetting,
    ISISLevel,
    ISISInterfaceLevel,
    ISISSegmentRouting,
    ISISFlexAlgo,
    ISISPrefixSID,
    ISISSRv6Locator,
)

__all__ = (
    'ISISInstanceFilterForm',
    'ISISInterfaceFilterForm',
    'ISISSettingFilterForm',
    'ISISLevelFilterForm',
    'ISISInterfaceLevelFilterForm',
    'ISISSegmentRoutingFilterForm',
    'ISISFlexAlgoFilterForm',
    'ISISPrefixSIDFilterForm',
    'ISISSRv6LocatorFilterForm',
)


class ISISFlexAlgoFilterForm(NetBoxModelFilterSetForm):
    model = ISISFlexAlgo
    fieldsets = (FieldSet('q', 'filter_id', 'tag'),)
    tag = TagFilterField(model)


class ISISPrefixSIDFilterForm(NetBoxModelFilterSetForm):
    model = ISISPrefixSID
    fieldsets = (FieldSet('q', 'filter_id', 'tag'),)
    tag = TagFilterField(model)


class ISISSRv6LocatorFilterForm(NetBoxModelFilterSetForm):
    model = ISISSRv6Locator
    fieldsets = (FieldSet('q', 'filter_id', 'tag'),)
    tag = TagFilterField(model)


class ISISSettingFilterForm(NetBoxModelFilterSetForm):
    model = ISISSetting
    fieldsets = (FieldSet('q', 'filter_id', 'tag'),)
    tag = TagFilterField(model)


class ISISLevelFilterForm(NetBoxModelFilterSetForm):
    model = ISISLevel
    fieldsets = (FieldSet('q', 'filter_id', 'tag'),)
    tag = TagFilterField(model)


class ISISInterfaceLevelFilterForm(NetBoxModelFilterSetForm):
    model = ISISInterfaceLevel
    fieldsets = (FieldSet('q', 'filter_id', 'tag'),)
    tag = TagFilterField(model)


class ISISSegmentRoutingFilterForm(NetBoxModelFilterSetForm):
    model = ISISSegmentRouting
    fieldsets = (FieldSet('q', 'filter_id', 'tag'),)
    tag = TagFilterField(model)


class ISISInstanceFilterForm(NetBoxModelFilterSetForm):
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
        label=_('Device'),
    )
    vrf_id = DynamicModelMultipleChoiceField(
        queryset=VRF.objects.all(),
        required=False,
        selector=True,
        label=_('VRF'),
    )
    process_tag = forms.CharField(required=False, label=_('Process Tag'))
    net = forms.CharField(required=False, label=_('NET'))
    is_type = forms.ChoiceField(
        choices=add_blank_choice(ISISIsTypeChoices),
        required=False,
        label=_('IS Type'),
    )

    model = ISISInstance
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
        FieldSet(
            'device_id', 'vrf_id', 'process_tag', 'net', 'is_type', name=_('IS-IS')
        ),
    )
    tag = TagFilterField(model)


class ISISInterfaceFilterForm(NetBoxModelFilterSetForm):
    model = ISISInterface
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
        FieldSet(
            'instance_id',
            'address_family',
            'circuit_type',
            'network_type',
            name=_('IS-IS'),
        ),
        FieldSet('device_id', 'interface_id', 'vrf_id', name=_('Device')),
        FieldSet('metric', 'passive', 'hello_auth_type', name=_('Attributes')),
    )
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
        label=_('Device'),
    )
    vrf_id = DynamicModelMultipleChoiceField(
        queryset=VRF.objects.all(),
        required=False,
        selector=True,
        label=_('VRF'),
    )
    instance_id = DynamicModelMultipleChoiceField(
        queryset=ISISInstance.objects.all(),
        required=False,
        selector=True,
        label=_('Instance'),
    )
    interface_id = DynamicModelMultipleChoiceField(
        queryset=Interface.objects.all(),
        required=False,
        selector=True,
        label=_('Interface'),
    )
    address_family = forms.ChoiceField(
        choices=add_blank_choice(ISISAddressFamilyChoices),
        required=False,
        label=_('Address Family'),
    )
    circuit_type = forms.ChoiceField(
        choices=add_blank_choice(ISISCircuitTypeChoices),
        required=False,
        label=_('Circuit Type'),
    )
    network_type = forms.ChoiceField(
        choices=add_blank_choice(ISISNetworkTypeChoices),
        required=False,
        label=_('Network Type'),
    )
    passive = forms.NullBooleanField(
        required=False,
        label=_('Passive'),
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )
    hello_auth_type = forms.MultipleChoiceField(
        choices=ISISAuthTypeChoices,
        required=False,
        label=_('Hello Auth Type'),
    )
    metric = forms.IntegerField(required=False, label=_('Metric'))
    tag = TagFilterField(model)
