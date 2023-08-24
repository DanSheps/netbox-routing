import django_filters
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import gettext as _

from dcim.models import Device
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

    router_id = MultiValueCharFilter(
        method='filter_rid',
        label=_('Router ID'),
    )

    class Meta:
        model = OSPFInstance
        fields = ('device_id', 'device', 'name', 'device', 'router_id', 'process_id')

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

    class Meta:
        model = OSPFInterface
        fields = ('instance', 'area', 'interface', 'bfd', 'priority', 'authentication', 'passphrase')

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

