import django_filters
from django.db.models import Q
from django.utils.translation import gettext as _

from netbox.filtersets import NetBoxModelFilterSet
from dcim.models import Device
from ipam.models import ASN, VRF, IPAddress
from netbox_routing.models.bgp import *

__all__ = (
    'BGPSettingFilterSet',
    'BGPRouterFilterSet',
    'BGPScopeFilterSet',
    'BGPAddressFamilyFilterSet',
    'BGPPeerFilterSet',
    'BGPPeerTemplateFilterSet',
    'BGPPeerAddressFamilyFilterSet',
)


class BGPSettingFilterSet(NetBoxModelFilterSet):
    key = django_filters.MultipleChoiceFilter(
        choices=BGPSettingChoices, null_value=None, label=_('Setting Name')
    )

    class Meta:
        model = BGPSetting
        fields = ('key',)

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(key__icontains=value)
        return queryset.filter(qs_filter).distinct()


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
        qs_filter = Q(device__name__icontains=value) | Q(asn__asn__icontains=value)
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
            Q(router__device__name__icontains=value)
            | Q(router__asn__asn__icontains=value)
            | Q(vrf__name__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()


class BGPAddressFamilyFilterSet(NetBoxModelFilterSet):
    scope_id = django_filters.ModelMultipleChoiceFilter(
        field_name='scope',
        queryset=Device.objects.all(),
        label=_('Router (ID)'),
    )
    address_family = django_filters.MultipleChoiceFilter(
        choices=BGPAddressFamilyChoices, null_value=None, label=_('Address Family')
    )

    class Meta:
        model = BGPAddressFamily
        fields = ('scope_id', 'address_family')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(address_family__icontains=value)
        return queryset.filter(qs_filter).distinct()


class BGPPeerFilterSet(NetBoxModelFilterSet):
    scope_id = django_filters.ModelMultipleChoiceFilter(
        field_name='scope',
        queryset=BGPScope.objects.all(),
        label=_('Scope (ID)'),
    )
    peer_id = django_filters.ModelMultipleChoiceFilter(
        field_name='peer',
        queryset=IPAddress.objects.all(),
        label=_('Peer (ID)'),
    )
    peer = django_filters.ModelMultipleChoiceFilter(
        field_name='peer__address',
        queryset=IPAddress.objects.all(),
        to_field_name='peer',
        label=_('Peer (Name)'),
    )
    peer_group_id = django_filters.ModelMultipleChoiceFilter(
        field_name='peer_group',
        queryset=BGPPeerTemplate.objects.all(),
        label=_('Peer Group (ID)'),
    )
    remote_as_id = django_filters.ModelMultipleChoiceFilter(
        field_name='remote_as',
        queryset=ASN.objects.all(),
        label=_('Remote AS (ID)'),
    )
    remote_as = django_filters.ModelMultipleChoiceFilter(
        field_name='remote_as__asn',
        queryset=ASN.objects.all(),
        to_field_name='remote_as',
        label=_('Remote AS (ASN)'),
    )
    local_as_id = django_filters.ModelMultipleChoiceFilter(
        field_name='local_as',
        queryset=ASN.objects.all(),
        label=_('Local AS (ID)'),
    )
    local_as = django_filters.ModelMultipleChoiceFilter(
        field_name='local_as__asn',
        queryset=ASN.objects.all(),
        to_field_name='local_as',
        label=_('Local AS (ASN)'),
    )

    class Meta:
        model = BGPPeer
        fields = ('scope_id', 'peer_id', 'remote_as_id', 'local_as_id')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(peer__address__icontains=value)
        qs_filter |= Q(remote_as__asn__icontains=value)
        qs_filter |= Q(local_as__asn__icontains=value)
        return queryset.filter(qs_filter).distinct()


class BGPPeerTemplateFilterSet(NetBoxModelFilterSet):
    peer_id = django_filters.ModelMultipleChoiceFilter(
        field_name='peers',
        queryset=BGPScope.objects.all(),
        label=_('Peer (ID)'),
    )
    address_family_id = django_filters.ModelMultipleChoiceFilter(
        field_name='address_families',
        queryset=BGPPeerAddressFamily.objects.all(),
        label=_('Address Family (ID)'),
    )
    remote_as_id = django_filters.ModelMultipleChoiceFilter(
        field_name='remote_as',
        queryset=ASN.objects.all(),
        label=_('Remote AS (ID)'),
    )
    remote_as = django_filters.ModelMultipleChoiceFilter(
        field_name='remote_as__asn',
        queryset=ASN.objects.all(),
        to_field_name='remote_as',
        label=_('Remote AS (ASN)'),
    )

    class Meta:
        model = BGPPeerTemplate
        fields = (
            'peer_id',
            'address_family_id',
            'remote_as_id',
            'remote_as',
            'enabled',
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(name__icontains=value)
        return queryset.filter(qs_filter).distinct()


class BGPPeerAddressFamilyFilterSet(NetBoxModelFilterSet):
    peer_id = django_filters.ModelMultipleChoiceFilter(
        field_name='peer',
        queryset=BGPScope.objects.all(),
        label=_('Peer (ID)'),
    )
    peer_group_id = django_filters.ModelMultipleChoiceFilter(
        field_name='peer_group',
        queryset=BGPPeerTemplate.objects.all(),
        label=_('Peer Group (ID)'),
    )
    address_family_id = django_filters.ModelMultipleChoiceFilter(
        field_name='address_family',
        queryset=BGPAddressFamily.objects.all(),
        label=_('Address Family (ID)'),
    )

    class Meta:
        model = BGPPeerAddressFamily
        fields = (
            'peer_id',
            'peer_group_id',
            'address_family',
            'enabled',
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(peer__address__icontains=value)
        qs_filter |= Q(remote_as__asn__icontains=value)
        qs_filter |= Q(local_as__asn__icontains=value)
        return queryset.filter(qs_filter).distinct()
