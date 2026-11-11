from django import forms
from django.utils.translation import gettext as _

from dcim.models import Device
from ipam.models import VRF
from netbox.forms import NetBoxModelBulkEditForm
from utilities.forms import BOOLEAN_WITH_BLANK_CHOICES, add_blank_choice
from utilities.forms.fields import DynamicModelChoiceField, CommentField

from netbox_routing import choices
from netbox_routing.choices.ospf import (
    OSPFAreaTypeChoices,
    OSPFDefaultInformationOriginateChoices,
    OSPFMetricTypeChoices,
    OSPFNetworkTypeChoices,
)
from netbox_routing.models import OSPFArea, OSPFInstance, OSPFInterface

__all__ = (
    'OSPFInterfaceBulkEditForm',
    'OSPFInstanceBulkEditForm',
    'OSPFAreaBulkEditForm',
)

from utilities.forms.rendering import FieldSet


class OSPFInstanceBulkEditForm(NetBoxModelBulkEditForm):
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(), label=_('Device'), required=False, selector=True
    )
    vrf = DynamicModelChoiceField(
        queryset=VRF.objects.all(), label=_('VRF'), required=False, selector=True
    )
    reference_bandwidth = forms.IntegerField(
        label=_('Reference Bandwidth (Mbps)'), min_value=1, required=False
    )
    passive_interface_default = forms.ChoiceField(
        label=_('Passive Interface Default'),
        choices=BOOLEAN_WITH_BLANK_CHOICES,
        required=False,
    )
    timers_spf_initial = forms.IntegerField(
        label=_('SPF Initial Delay (ms)'), min_value=0, required=False
    )
    timers_spf_hold = forms.IntegerField(
        label=_('SPF Hold Time (ms)'), min_value=0, required=False
    )
    timers_spf_max = forms.IntegerField(
        label=_('SPF Max Wait (ms)'), min_value=0, required=False
    )
    timers_lsa_initial = forms.IntegerField(
        label=_('LSA Initial Delay (ms)'), min_value=0, required=False
    )
    timers_lsa_hold = forms.IntegerField(
        label=_('LSA Hold Time (ms)'), min_value=0, required=False
    )
    timers_lsa_max = forms.IntegerField(
        label=_('LSA Max Wait (ms)'), min_value=0, required=False
    )
    distance = forms.IntegerField(
        label=_('Distance'), min_value=1, max_value=255, required=False
    )
    distance_intra_area = forms.IntegerField(
        label=_('Intra-Area Distance'), min_value=1, max_value=255, required=False
    )
    distance_inter_area = forms.IntegerField(
        label=_('Inter-Area Distance'), min_value=1, max_value=255, required=False
    )
    distance_external = forms.IntegerField(
        label=_('External Distance'), min_value=1, max_value=255, required=False
    )
    default_information_originate = forms.ChoiceField(
        label=_('Default Information Originate'),
        choices=add_blank_choice(OSPFDefaultInformationOriginateChoices),
        required=False,
    )
    default_information_metric = forms.IntegerField(
        label=_('Default Information Metric'),
        min_value=0,
        max_value=16777214,
        required=False,
    )
    default_information_metric_type = forms.ChoiceField(
        label=_('Default Information Metric Type'),
        choices=add_blank_choice(OSPFMetricTypeChoices),
        required=False,
    )
    max_metric_router_lsa = forms.ChoiceField(
        label=_('Max Metric Router LSA'),
        choices=BOOLEAN_WITH_BLANK_CHOICES,
        required=False,
    )
    max_metric_on_startup = forms.IntegerField(
        label=_('Max Metric On Startup (s)'),
        min_value=5,
        max_value=86400,
        required=False,
    )

    description = forms.CharField(
        label=_('Description'), max_length=200, required=False
    )
    comments = CommentField()

    model = OSPFInstance
    fieldsets = (
        FieldSet('device', 'vrf', name='OSPF'),
        FieldSet(
            'reference_bandwidth', 'passive_interface_default', name=_('Settings')
        ),
        FieldSet(
            'timers_spf_initial',
            'timers_spf_hold',
            'timers_spf_max',
            'timers_lsa_initial',
            'timers_lsa_hold',
            'timers_lsa_max',
            name=_('Timers'),
        ),
        FieldSet(
            'distance',
            'distance_intra_area',
            'distance_inter_area',
            'distance_external',
            name=_('Distance'),
        ),
        FieldSet(
            'default_information_originate',
            'default_information_metric',
            'default_information_metric_type',
            name=_('Default Information'),
        ),
        FieldSet(
            'max_metric_router_lsa', 'max_metric_on_startup', name=_('Max Metric')
        ),
        FieldSet(
            'description',
        ),
    )
    nullable_fields = (
        'vrf',
        'reference_bandwidth',
        'passive_interface_default',
        'timers_spf_initial',
        'timers_spf_hold',
        'timers_spf_max',
        'timers_lsa_initial',
        'timers_lsa_hold',
        'timers_lsa_max',
        'distance',
        'distance_intra_area',
        'distance_inter_area',
        'distance_external',
        'default_information_originate',
        'default_information_metric',
        'default_information_metric_type',
        'max_metric_router_lsa',
        'max_metric_on_startup',
        'description',
    )


class OSPFAreaBulkEditForm(NetBoxModelBulkEditForm):
    area_type = forms.ChoiceField(
        label=_('Area Type'), choices=OSPFAreaTypeChoices, required=False
    )
    description = forms.CharField(
        label=_('Description'), max_length=200, required=False
    )
    comments = CommentField()

    model = OSPFArea
    fieldsets = (FieldSet('description'),)
    nullable_fields = ()


class OSPFInterfaceBulkEditForm(NetBoxModelBulkEditForm):
    instance = DynamicModelChoiceField(
        queryset=OSPFInstance.objects.all(),
        label=_('OSPF Instance'),
        required=False,
        selector=True,
    )
    area = DynamicModelChoiceField(
        queryset=OSPFArea.objects.all(),
        label=_('OSPF Area'),
        required=False,
        selector=True,
    )
    passive = forms.ChoiceField(
        label=_('Passive'), choices=BOOLEAN_WITH_BLANK_CHOICES, required=False
    )
    priority = forms.IntegerField(label=_('Priority'), required=False)
    bfd = forms.ChoiceField(
        label=_('BFD'), choices=BOOLEAN_WITH_BLANK_CHOICES, required=False
    )
    network_type = forms.ChoiceField(
        label=_('Network Type'),
        choices=add_blank_choice(OSPFNetworkTypeChoices),
        required=False,
    )
    authentication = forms.ChoiceField(
        label=_('Authentication'),
        choices=add_blank_choice(choices.AuthenticationChoices),
        required=False,
    )
    passphrase = forms.CharField(label=_('Passphrase'), required=False)

    description = forms.CharField(
        label=_('Description'), max_length=200, required=False
    )
    comments = CommentField()

    model = OSPFInterface
    fieldsets = (
        FieldSet('instance', 'area', name='OSPF'),
        FieldSet(
            'network_type',
            'passive',
            'priority',
            'bfd',
            'authentication',
            'passphrase',
            name='Attributes',
        ),
        FieldSet('description'),
    )
    nullable_fields = ('network_type',)
