# SPDX-License-Identifier: Apache-2.0

import django_filters
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from dcim.models import Device, Interface
from ipam.models import VRF
from netbox.filtersets import NetBoxModelFilterSet
from utilities.filters import MultiValueCharFilter
from utilities.filtersets import register_filterset

from netbox_routing.choices import (
    ISISAddressFamilyChoices,
    ISISAuthTypeChoices,
    ISISCircuitTypeChoices,
    ISISIsTypeChoices,
    ISISNetworkTypeChoices,
    ISISSettingChoices,
)
from netbox_routing.models import (
    ISISInstance,
    ISISInterface,
    ISISSetting,
    ISISLevel,
    ISISInterfaceLevel,
    ISISSegmentRouting,
    ISISFlexAlgo,
)

__all__ = (
    'ISISInstanceFilterSet',
    'ISISInterfaceFilterSet',
    'ISISSettingFilterSet',
    'ISISLevelFilterSet',
    'ISISInterfaceLevelFilterSet',
    'ISISSegmentRoutingFilterSet',
    'ISISFlexAlgoFilterSet',
)


@register_filterset
class ISISFlexAlgoFilterSet(NetBoxModelFilterSet):
    instance_id = django_filters.ModelMultipleChoiceFilter(
        field_name='instance', queryset=ISISInstance.objects.all(), label='Instance (ID)'
    )

    class Meta:
        model = ISISFlexAlgo
        fields = ('instance_id', 'algo_id', 'metric_type')

    def search(self, queryset, name, value):
        return queryset


@register_filterset
class ISISSettingFilterSet(NetBoxModelFilterSet):
    key = django_filters.MultipleChoiceFilter(
        choices=ISISSettingChoices, null_value=None, label=_('Setting Name')
    )

    class Meta:
        model = ISISSetting
        fields = ('key',)

    def search(self, queryset, name, value):
        value = (value or '').strip()
        if not value:
            return queryset
        qs_filter = Q(key__icontains=value) | Q(value__icontains=value)
        return queryset.filter(qs_filter).distinct()


@register_filterset
class ISISLevelFilterSet(NetBoxModelFilterSet):
    instance_id = django_filters.ModelMultipleChoiceFilter(
        field_name='instance', queryset=ISISInstance.objects.all(), label='Instance (ID)'
    )

    class Meta:
        model = ISISLevel
        fields = ('instance_id', 'level')

    def search(self, queryset, name, value):
        return queryset


@register_filterset
class ISISInterfaceLevelFilterSet(NetBoxModelFilterSet):
    interface_id = django_filters.ModelMultipleChoiceFilter(
        field_name='interface', queryset=ISISInterface.objects.all(), label='Interface (ID)'
    )

    class Meta:
        model = ISISInterfaceLevel
        fields = ('interface_id', 'level')

    def search(self, queryset, name, value):
        return queryset


@register_filterset
class ISISSegmentRoutingFilterSet(NetBoxModelFilterSet):
    instance_id = django_filters.ModelMultipleChoiceFilter(
        field_name='instance', queryset=ISISInstance.objects.all(), label='Instance (ID)'
    )

    class Meta:
        model = ISISSegmentRouting
        fields = ('instance_id', 'enabled')

    def search(self, queryset, name, value):
        return queryset


@register_filterset
class ISISInstanceFilterSet(NetBoxModelFilterSet):
    device_id = django_filters.ModelMultipleChoiceFilter(
        field_name='device',
        queryset=Device.objects.all(),
        label='Device (ID)',
    )
    device = django_filters.ModelMultipleChoiceFilter(
        field_name='device__name',
        queryset=Device.objects.all(),
        to_field_name='name',
        label='Device',
    )
    vrf_id = django_filters.ModelMultipleChoiceFilter(
        field_name='vrf',
        queryset=VRF.objects.all(),
        label='VRF (ID)',
    )
    vrf = django_filters.ModelMultipleChoiceFilter(
        field_name='vrf__name',
        queryset=VRF.objects.all(),
        to_field_name='name',
        label='VRF',
    )
    process_tag = MultiValueCharFilter(label=_('Process Tag'))
    net = MultiValueCharFilter(label=_('NET'))
    is_type = django_filters.MultipleChoiceFilter(
        choices=ISISIsTypeChoices,
        label=_('IS Type'),
    )

    class Meta:
        model = ISISInstance
        fields = (
            'device_id',
            'device',
            'vrf_id',
            'vrf',
            'process_tag',
            'net',
            'is_type',
        )

    def search(self, queryset, name, value):
        value = (value or '').strip()
        if not value:
            return queryset
        qs_filter = (
            Q(process_tag__icontains=value)
            | Q(device__name__icontains=value)
            | Q(net__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()


@register_filterset
class ISISInterfaceFilterSet(NetBoxModelFilterSet):
    instance_id = django_filters.ModelMultipleChoiceFilter(
        field_name='instance',
        queryset=ISISInstance.objects.all(),
        label='Instance (ID)',
    )
    vrf_id = django_filters.ModelMultipleChoiceFilter(
        field_name='instance__vrf',
        queryset=VRF.objects.all(),
        label='VRF (ID)',
    )
    vrf = django_filters.ModelMultipleChoiceFilter(
        field_name='instance__vrf__name',
        queryset=VRF.objects.all(),
        to_field_name='name',
        label='VRF',
    )
    device_id = django_filters.ModelMultipleChoiceFilter(
        field_name='interface__device',
        queryset=Device.objects.all(),
        label='Device (ID)',
    )
    device = django_filters.ModelMultipleChoiceFilter(
        field_name='interface__device__name',
        queryset=Device.objects.all(),
        to_field_name='name',
        label='Device',
    )
    interface_id = django_filters.ModelMultipleChoiceFilter(
        field_name='interface',
        queryset=Interface.objects.all(),
        label='Interface (ID)',
    )
    interface = django_filters.ModelMultipleChoiceFilter(
        field_name='interface__name',
        queryset=Interface.objects.all(),
        to_field_name='name',
        label='Interface',
    )
    address_family = django_filters.MultipleChoiceFilter(
        choices=ISISAddressFamilyChoices,
        label=_('Address Family'),
    )
    circuit_type = django_filters.MultipleChoiceFilter(
        choices=ISISCircuitTypeChoices,
        label=_('Circuit Type'),
    )
    network_type = django_filters.MultipleChoiceFilter(
        choices=ISISNetworkTypeChoices,
        label=_('Network Type'),
    )
    hello_auth_type = django_filters.MultipleChoiceFilter(
        choices=ISISAuthTypeChoices,
        label=_('Hello Auth Type'),
    )

    class Meta:
        model = ISISInterface
        fields = (
            'instance_id',
            'vrf_id',
            'vrf',
            'device_id',
            'device',
            'interface_id',
            'interface',
            'address_family',
            'circuit_type',
            'network_type',
            'metric',
            'passive',
            'hello_auth_type',
        )

    def search(self, queryset, name, value):
        value = (value or '').strip()
        if not value:
            return queryset
        qs_filter = (
            Q(instance__process_tag__icontains=value)
            | Q(instance__net__icontains=value)
            | Q(interface__name__icontains=value)
            | Q(interface__label__icontains=value)
            | Q(interface__device__name__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()
