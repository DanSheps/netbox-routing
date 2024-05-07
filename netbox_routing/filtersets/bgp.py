import django_filters
from django.db.models import Q
from django.utils.translation import gettext as _

from netbox.filtersets import NetBoxModelFilterSet
from dcim.models import Device
from ipam.models import ASN, VRF
from netbox_routing.choices.bgp import BGPSettingChoices, BGPAddressFamilyChoices
from netbox_routing.models import BGPRouter, BGPSetting, BGPAddressFamily, BGPScope


__all__ = (
    'BGPRouterFilterSet',
    'BGPScopeFilterSet',
    'BGPAddressFamilyFilterSet',
    'BGPSettingFilterSet',
)



class BGPRouterFilterSet(NetBoxModelFilterSet):
    device_id = django_filters.ModelMultipleChoiceFilter(
        field_name='device',
        queryset=Device.objects.all(),
        label=_('Device (ID)'),
    )
    device = django_filters.ModelMultipleChoiceFilter(
        field_name='device__name',
        queryset=Device.objects.all(),
        to_field_name='name',
        label=_('Device'),
    )
    asn_id = django_filters.ModelMultipleChoiceFilter(
        field_name='asn',
        queryset=ASN.objects.all(),
        label=_('AS Number (ID)'),
    )
    asn = django_filters.ModelMultipleChoiceFilter(
        field_name='asn__asn',
        queryset=ASN.objects.all(),
        to_field_name='asn',
        label=_('AS Number'),
    )

    class Meta:
        model = BGPRouter
        fields = ('device_id', 'device', 'asn_id', 'asn')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(device__name__icontains=value) |
            Q(asn__asn__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()



class BGPScopeFilterSet(NetBoxModelFilterSet):
    router_id = django_filters.ModelMultipleChoiceFilter(
        field_name='router',
        queryset=BGPRouter.objects.all(),
        label=_('Router (ID)'),
    )
    vrf_id = django_filters.ModelMultipleChoiceFilter(
        field_name='vrf',
        queryset=VRF.objects.all(),
        label=_('VRF (ID)'),
    )
    vrf = django_filters.ModelMultipleChoiceFilter(
        field_name='vrf__name',
        queryset=VRF.objects.all(),
        to_field_name='vrf',
        label=_('VRF'),
    )

    class Meta:
        model = BGPScope
        fields = ('router_id', 'vrf_id', 'vrf')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(router__device__name__icontains=value) |
            Q(router__asn__asn__icontains=value) |
            Q(vrf__name__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()



class BGPAddressFamilyFilterSet(NetBoxModelFilterSet):
    scope_id = django_filters.ModelMultipleChoiceFilter(
        field_name='scope',
        queryset=Device.objects.all(),
        label=_('Router (ID)'),
    )
    address_family = django_filters.MultipleChoiceFilter(
        choices=BGPAddressFamilyChoices,
        null_value=None,
        label=_('Address Family')
    )

    class Meta:
        model = BGPAddressFamily
        fields = ('scope_id', 'address_family')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(address_family__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()


class BGPSettingFilterSet(NetBoxModelFilterSet):
    key = django_filters.MultipleChoiceFilter(
        choices=BGPSettingChoices,
        null_value=None,
        label=_('Setting Name')
    )

    class Meta:
        model = BGPSetting
        fields = ('key', )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(key__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()
