import django_filters
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import gettext as _

from dcim.models import Device, Interface
from ipam.models import VRF
from utilities.filters import MultiValueCharFilter

from netbox.filtersets import NetBoxModelFilterSet
from netbox_routing.models import OSPFArea, OSPFInstance, OSPFInterface


__all__ = (
    'OSPFAreaFilterSet',
    'OSPFInstanceFilterSet',
    'OSPFInterfaceFilterSet'
)



class OSPFInstanceFilterSet(NetBoxModelFilterSet):
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

    router_id = MultiValueCharFilter(
        method='filter_rid',
        label=_('Router ID'),
    )

    class Meta:
        model = OSPFInstance
        fields = ('device_id', 'device', 'name', 'vrf_id', 'vrf', 'router_id', 'process_id')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value) |
            Q(device__name__icontains=value) |
            Q(router_id__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()

    def filter_rid(self, queryset, name, value):
        try:
            return queryset.filter(**{f'{name}__in': value})
        except ValidationError:
            return queryset.none()


class OSPFAreaFilterSet(NetBoxModelFilterSet):
    area_id = MultiValueCharFilter(
        method='filter_aid',
        label=_('Area ID'),
    )

    class Meta:
        model = OSPFArea
        fields = ('area_id', )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(area_id__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()

    def filter_aid(self, queryset, name, value):
        try:
            return queryset.filter(**{f'{name}__in': value})
        except ValidationError:
            return queryset.none()


class OSPFInterfaceFilterSet(NetBoxModelFilterSet):
    instance_id = django_filters.ModelMultipleChoiceFilter(
        field_name='instance',
        queryset=OSPFInstance.objects.all(),
        label='Instance (ID)',
    )
    instance = django_filters.ModelMultipleChoiceFilter(
        field_name='instance__name',
        queryset=OSPFInstance.objects.all(),
        to_field_name='name',
        label='Instance',
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
    area_id = django_filters.ModelMultipleChoiceFilter(
        field_name='area',
        queryset=OSPFArea.objects.all(),
        label='Area (ID)',
    )
    area = django_filters.ModelMultipleChoiceFilter(
        field_name='area__area_id',
        queryset=OSPFArea.objects.all(),
        to_field_name='area_id',
        label='Area',
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
        label='Area (ID)',
    )
    interface = django_filters.ModelMultipleChoiceFilter(
        field_name='interface__name',
        queryset=Interface.objects.all(),
        to_field_name='name',
        label='Area',
    )

    class Meta:
        model = OSPFInterface
        fields = ('instance', 'area', 'interface', 'passive', 'bfd', 'priority', 'authentication', 'passphrase')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(instance__name__icontains=value) |
            Q(area__area_id__icontains=value) |
            Q(interface__name__icontains=value) |
            Q(interface__label__icontains=value) |
            Q(interface__device__name__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()

