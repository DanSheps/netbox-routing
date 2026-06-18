# SPDX-License-Identifier: Apache-2.0

from django import forms
from django.utils.translation import gettext_lazy as _

from dcim.models import Device
from ipam.models import VRF
from netbox.forms import NetBoxModelBulkEditForm
from utilities.forms import BOOLEAN_WITH_BLANK_CHOICES, add_blank_choice
from utilities.forms.fields import CommentField, DynamicModelChoiceField
from utilities.forms.rendering import FieldSet

from netbox_routing.choices import (
    ISISAddressFamilyChoices,
    ISISAuthTypeChoices,
    ISISCircuitTypeChoices,
    ISISIsTypeChoices,
    ISISMetricStyleChoices,
    ISISNetworkTypeChoices,
)
from netbox_routing.models import ISISInstance, ISISInterface, ISISSetting

__all__ = (
    'ISISInstanceBulkEditForm',
    'ISISInterfaceBulkEditForm',
    'ISISSettingBulkEditForm',
)


class ISISSettingBulkEditForm(NetBoxModelBulkEditForm):
    description = forms.CharField(
        label=_('Description'), max_length=200, required=False
    )
    comments = CommentField()

    model = ISISSetting
    fieldsets = (FieldSet('description', 'comments'),)
    nullable_fields = ('description',)


class ISISInstanceBulkEditForm(NetBoxModelBulkEditForm):
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(), label=_('Device'), required=False, selector=True
    )
    vrf = DynamicModelChoiceField(
        queryset=VRF.objects.all(), label=_('VRF'), required=False, selector=True
    )
    process_tag = forms.CharField(label=_('Process Tag'), required=False)
    net = forms.CharField(label=_('NET'), required=False)
    is_type = forms.ChoiceField(
        label=_('IS Type'),
        choices=add_blank_choice(ISISIsTypeChoices),
        required=False,
    )
    metric_style = forms.ChoiceField(
        label=_('Metric Style'),
        choices=add_blank_choice(ISISMetricStyleChoices),
        required=False,
    )
    lsp_lifetime = forms.IntegerField(label=_('LSP Lifetime'), min_value=0, required=False)
    lsp_refresh_interval = forms.IntegerField(
        label=_('LSP Refresh Interval'), min_value=0, required=False
    )
    lsp_mtu = forms.IntegerField(label=_('LSP MTU'), min_value=0, required=False)
    distance = forms.IntegerField(label=_('Distance'), min_value=0, required=False)
    maximum_paths = forms.IntegerField(label=_('Maximum Paths'), min_value=0, required=False)
    description = forms.CharField(
        label=_('Description'), max_length=200, required=False
    )
    comments = CommentField()

    model = ISISInstance
    fieldsets = (
        FieldSet('device', 'vrf', 'process_tag', 'net', 'is_type', 'metric_style', name='IS-IS'),
        FieldSet(
            'lsp_lifetime', 'lsp_refresh_interval', 'lsp_mtu', 'distance', 'maximum_paths',
            name='Attributes',
        ),
        FieldSet('description', 'comments'),
    )
    nullable_fields = (
        'vrf',
        'description',
        'is_type',
        'metric_style',
        'lsp_lifetime',
        'lsp_refresh_interval',
        'lsp_mtu',
        'distance',
        'maximum_paths',
    )


class ISISInterfaceBulkEditForm(NetBoxModelBulkEditForm):
    instance = DynamicModelChoiceField(
        queryset=ISISInstance.objects.all(),
        label=_('IS-IS Instance'),
        required=False,
        selector=True,
    )
    address_family = forms.ChoiceField(
        label=_('Address Family'),
        choices=add_blank_choice(ISISAddressFamilyChoices),
        required=False,
    )
    circuit_type = forms.ChoiceField(
        label=_('Circuit Type'),
        choices=add_blank_choice(ISISCircuitTypeChoices),
        required=False,
    )
    network_type = forms.ChoiceField(
        label=_('Network Type'),
        choices=add_blank_choice(ISISNetworkTypeChoices),
        required=False,
    )
    metric = forms.IntegerField(label=_('Metric'), min_value=0, required=False)
    passive = forms.ChoiceField(
        label=_('Passive'), choices=BOOLEAN_WITH_BLANK_CHOICES, required=False
    )
    hello_auth_type = forms.ChoiceField(
        label=_('Hello Auth Type'),
        choices=add_blank_choice(ISISAuthTypeChoices),
        required=False,
    )
    hello_auth_key = forms.CharField(label=_('Hello Auth Key'), required=False)
    csnp_interval = forms.IntegerField(label=_('CSNP Interval'), min_value=0, required=False)
    retransmit_interval = forms.IntegerField(
        label=_('Retransmit Interval'), min_value=0, required=False
    )
    lsp_interval = forms.IntegerField(label=_('LSP Interval'), min_value=0, required=False)
    mesh_group = forms.CharField(label=_('Mesh Group'), required=False)
    description = forms.CharField(
        label=_('Description'), max_length=200, required=False
    )
    comments = CommentField()

    model = ISISInterface
    fieldsets = (
        FieldSet('instance', name='IS-IS'),
        FieldSet(
            'address_family',
            'circuit_type',
            'network_type',
            'metric',
            'passive',
            'hello_auth_type',
            'hello_auth_key',
            name='Attributes',
        ),
        FieldSet(
            'csnp_interval', 'retransmit_interval', 'lsp_interval', 'mesh_group',
            name='Timers',
        ),
        FieldSet('description', 'comments'),
    )
    nullable_fields = (
        'description',
        'circuit_type',
        'network_type',
        'metric',
        'passive',
        'hello_auth_type',
        'hello_auth_key',
        'csnp_interval',
        'retransmit_interval',
        'lsp_interval',
        'mesh_group',
    )
