import django_filters
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import gettext as _

from dcim.models import Device, Interface
from virtualization.models import VirtualMachine, VMInterface
from ipam.models import VRF
from utilities.filters import MultiValueCharFilter
from utilities.filtersets import register_filterset

from netbox.filtersets import NetBoxModelFilterSet
from netbox_routing.choices.ospf import OSPFAreaTypeChoices
from netbox_routing.models import OSPFArea, OSPFInstance, OSPFInterface

__all__ = ('OSPFAreaFilterSet', 'OSPFInstanceFilterSet', 'OSPFInterfaceFilterSet')


@register_filterset
class OSPFInstanceFilterSet(NetBoxModelFilterSet):
    device_id = django_filters.ModelMultipleChoiceFilter(
        method='filter_device_id',
        queryset=Device.objects.all(),
        label='Device (ID)',
    )
    device = django_filters.ModelMultipleChoiceFilter(
        method='filter_device',
        queryset=Device.objects.all(),
        to_field_name='name',
        label='Device',
    )
    virtual_machine_id = django_filters.ModelMultipleChoiceFilter(
        method='filter_vm_id',
        queryset=VirtualMachine.objects.all(),
        label='Virtual Machine (ID)',
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
        fields = ('name', 'vrf_id', 'vrf', 'router_id', 'process_id')

    def filter_device_id(self, queryset, name, value):
        if not value:
            return queryset
        ct = ContentType.objects.get_for_model(Device)
        ids = [d.pk for d in value]
        return queryset.filter(device_type=ct, device_id__in=ids)

    def filter_device(self, queryset, name, value):
        if not value:
            return queryset
        ct = ContentType.objects.get_for_model(Device)
        ids = [d.pk for d in value]
        return queryset.filter(device_type=ct, device_id__in=ids)

    def filter_vm_id(self, queryset, name, value):
        if not value:
            return queryset
        ct = ContentType.objects.get_for_model(VirtualMachine)
        ids = [vm.pk for vm in value]
        return queryset.filter(device_type=ct, device_id__in=ids)

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        device_ct = ContentType.objects.get_for_model(Device)
        vm_ct = ContentType.objects.get_for_model(VirtualMachine)
        device_ids = Device.objects.filter(name__icontains=value).values_list('pk', flat=True)
        vm_ids = VirtualMachine.objects.filter(name__icontains=value).values_list('pk', flat=True)
        qs_filter = (
            Q(name__icontains=value)
            | Q(router_id__icontains=value)
            | Q(device_type=device_ct, device_id__in=device_ids)
            | Q(device_type=vm_ct, device_id__in=vm_ids)
        )
        return queryset.filter(qs_filter).distinct()

    def filter_rid(self, queryset, name, value):
        try:
            return queryset.filter(**{f'{name}__in': value})
        except ValidationError:
            return queryset.none()


@register_filterset
class OSPFAreaFilterSet(NetBoxModelFilterSet):
    area_id = MultiValueCharFilter(
        method='filter_aid',
        label=_('Area ID'),
    )
    area_type = django_filters.MultipleChoiceFilter(
        choices=OSPFAreaTypeChoices,
        label=_('Area Type'),
    )

    class Meta:
        model = OSPFArea
        fields = ('area_id', 'area_type')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(area_id__icontains=value)).distinct()

    def filter_aid(self, queryset, name, value):
        try:
            return queryset.filter(**{f'{name}__in': value})
        except ValidationError:
            return queryset.none()


@register_filterset
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
        method='filter_device_id',
        queryset=Device.objects.all(),
        label='Device (ID)',
    )
    virtual_machine_id = django_filters.ModelMultipleChoiceFilter(
        method='filter_vm_id',
        queryset=VirtualMachine.objects.all(),
        label='Virtual Machine (ID)',
    )
    interface_id = django_filters.ModelMultipleChoiceFilter(
        method='filter_interface_id',
        queryset=Interface.objects.all(),
        label='Interface (ID)',
    )
    vm_interface_id = django_filters.ModelMultipleChoiceFilter(
        method='filter_vm_interface_id',
        queryset=VMInterface.objects.all(),
        label='VM Interface (ID)',
    )

    class Meta:
        model = OSPFInterface
        fields = ('instance', 'area', 'passive', 'bfd', 'priority', 'authentication', 'passphrase')

    def filter_device_id(self, queryset, name, value):
        if not value:
            return queryset
        ct = ContentType.objects.get_for_model(Interface)
        iface_ids = Interface.objects.filter(device__in=value).values_list('pk', flat=True)
        return queryset.filter(interface_type=ct, interface_id__in=iface_ids)

    def filter_vm_id(self, queryset, name, value):
        if not value:
            return queryset
        ct = ContentType.objects.get_for_model(VMInterface)
        iface_ids = VMInterface.objects.filter(virtual_machine__in=value).values_list('pk', flat=True)
        return queryset.filter(interface_type=ct, interface_id__in=iface_ids)

    def filter_interface_id(self, queryset, name, value):
        if not value:
            return queryset
        ct = ContentType.objects.get_for_model(Interface)
        return queryset.filter(interface_type=ct, interface_id__in=[i.pk for i in value])

    def filter_vm_interface_id(self, queryset, name, value):
        if not value:
            return queryset
        ct = ContentType.objects.get_for_model(VMInterface)
        return queryset.filter(interface_type=ct, interface_id__in=[i.pk for i in value])

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(instance__name__icontains=value)
            | Q(area__area_id__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()