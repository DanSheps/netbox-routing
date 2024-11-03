import django_filters
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import gettext as _

from netbox.filtersets import NetBoxModelFilterSet
from dcim.models import Device
from ipam.models import ASN, VRF, IPAddress
from netbox_routing.choices.bgp import BGPSettingChoices, BGPAddressFamilyChoices
from netbox_routing.models.bgp import *


__all__ = (
    'BGPRouterFilterSet',
    'BGPScopeFilterSet',
    'BGPSessionTemplateFilterSet',
    'BGPPolicyTemplateFilterSet',
    'BGPAddressFamilyFilterSet',
    'BGPPeerFilterSet',
    'BGPPeerTemplateFilterSet',
    'BGPPeerAddressFamilyFilterSet',
    'BGPSettingFilterSet',
)

from tenancy.models import Tenant
from utilities.filters import MultiValueCharFilter, MultiValueNumberFilter


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
    tenant_id = django_filters.ModelMultipleChoiceFilter(
        field_name='tenant__name',
        queryset=Tenant.objects.all(),
        label=_('Tenant (ID)'),
    )
    tenant = django_filters.ModelMultipleChoiceFilter(
        field_name='tenant',
        queryset=Tenant.objects.all(),
        to_field_name='name',
        label=_('Tenant'),
    )

    class Meta:
        model = BGPRouter
        fields = ('device_id', 'device', 'asn_id', 'asn', 'tenant_id', 'tenant')

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
    tenant_id = django_filters.ModelMultipleChoiceFilter(
        field_name='tenant__name',
        queryset=Tenant.objects.all(),
        label=_('Tenant (ID)'),
    )
    tenant = django_filters.ModelMultipleChoiceFilter(
        field_name='tenant',
        queryset=Tenant.objects.all(),
        to_field_name='name',
        label=_('Tenant'),
    )

    class Meta:
        model = BGPScope
        fields = ('router_id', 'vrf_id', 'vrf', 'tenant_id', 'tenant')

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
    tenant_id = django_filters.ModelMultipleChoiceFilter(
        field_name='tenant__name',
        queryset=Tenant.objects.all(),
        label=_('Tenant (ID)'),
    )
    tenant = django_filters.ModelMultipleChoiceFilter(
        field_name='tenant',
        queryset=Tenant.objects.all(),
        to_field_name='name',
        label=_('Tenant'),
    )

    class Meta:
        model = BGPAddressFamily
        fields = ('scope_id', 'address_family', 'tenant_id', 'tenant')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(address_family__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()


class BGPSessionTemplateFilterSet(NetBoxModelFilterSet):
    router_id = django_filters.ModelMultipleChoiceFilter(
        field_name='router',
        queryset=BGPRouter.objects.all(),
        label=_('Router (ID)'),
    )
    parent_id = django_filters.ModelMultipleChoiceFilter(
        field_name='parent',
        queryset=BGPSessionTemplate.objects.all(),
        label=_('Parent Session Template (ID)'),
    )
    tenant_id = django_filters.ModelMultipleChoiceFilter(
        field_name='tenant__name',
        queryset=Tenant.objects.all(),
        label=_('Tenant (ID)'),
    )
    tenant = django_filters.ModelMultipleChoiceFilter(
        field_name='tenant',
        queryset=Tenant.objects.all(),
        to_field_name='name',
        label=_('Tenant'),
    )

    class Meta:
        model = BGPSessionTemplate
        fields = ('router_id', 'parent_id', 'tenant_id', 'tenant')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(router__name__icontains=value),
            Q(parent__name__icontains=value),
            Q(name__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()


class BGPPolicyTemplateFilterSet(NetBoxModelFilterSet):
    router_id = django_filters.ModelMultipleChoiceFilter(
        field_name='router',
        queryset=BGPRouter.objects.all(),
        label=_('Router (ID)'),
    )
    router = django_filters.ModelMultipleChoiceFilter(
        field_name='router',
        queryset=BGPRouter.objects.all(),
        to_field_name='name',
        label=_('Router'),
    )
    tenant_id = django_filters.ModelMultipleChoiceFilter(
        field_name='tenant__name',
        queryset=Tenant.objects.all(),
        label=_('Tenant (ID)'),
    )
    tenant = django_filters.ModelMultipleChoiceFilter(
        field_name='tenant',
        queryset=Tenant.objects.all(),
        to_field_name='name',
        label=_('Tenant'),
    )

    class Meta:
        model = BGPSessionTemplate
        fields = ('router_id', 'tenant_id', 'tenant')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(router__name__icontains=value),
            Q(name__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()


class BGPPeerTemplateFilterSet(NetBoxModelFilterSet):
    remote_as_id = django_filters.ModelMultipleChoiceFilter(
        field_name='remote_as',
        queryset=ASN.objects.all(),
        label=_('Remote AS (ID)'),
    )
    remote_as = django_filters.ModelMultipleChoiceFilter(
        field_name='remote_as',
        queryset=ASN.objects.all(),
        to_field_name='name',
        label=_('Remote AS (ID)'),
    )
    tenant_id = django_filters.ModelMultipleChoiceFilter(
        field_name='tenant__name',
        queryset=Tenant.objects.all(),
        label=_('Tenant (ID)'),
    )
    tenant = django_filters.ModelMultipleChoiceFilter(
        field_name='tenant',
        queryset=Tenant.objects.all(),
        to_field_name='name',
        label=_('Tenant'),
    )

    class Meta:
        model = BGPPeerTemplate
        fields = ('remote_as_id', 'remote_as', 'tenant_id', 'tenant')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()


class BGPPeerFilterSet(NetBoxModelFilterSet):
    peer_id = django_filters.ModelMultipleChoiceFilter(
        field_name='peer',
        queryset=IPAddress.objects.all(),
        label=_('Peer Address (ID)'),
    )
    tenant_id = django_filters.ModelMultipleChoiceFilter(
        field_name='tenant__name',
        queryset=Tenant.objects.all(),
        label=_('Tenant (ID)'),
    )
    tenant = django_filters.ModelMultipleChoiceFilter(
        field_name='tenant',
        queryset=Tenant.objects.all(),
        to_field_name='name',
        label=_('Tenant'),
    )

    class Meta:
        model = BGPPeer
        fields = ('peer_id', 'tenant_id', 'tenant')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(address__address__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()


class BGPPeerAddressFamilyFilterSet(NetBoxModelFilterSet):
    peer_template = MultiValueCharFilter(
        method='filter_peertemplate',
        field_name='name',
        label=_('Peer (name)'),
    )
    peer_template_id = MultiValueNumberFilter(
        method='filter_peertemplate',
        field_name='pk',
        label=_('Peer (ID)'),
    )
    peer = MultiValueCharFilter(
        method='filter_peer',
        field_name='name',
        label=_('Peer (name)'),
    )
    peer_id = MultiValueNumberFilter(
        method='filter_peer',
        field_name='pk',
        label=_('Peer (ID)'),
    )
    tenant_id = django_filters.ModelMultipleChoiceFilter(
        field_name='tenant__name',
        queryset=Tenant.objects.all(),
        label=_('Tenant (ID)'),
    )
    tenant = django_filters.ModelMultipleChoiceFilter(
        field_name='tenant',
        queryset=Tenant.objects.all(),
        to_field_name='name',
        label=_('Tenant'),
    )

    class Meta:
        model = BGPPeerAddressFamily
        fields = ('peer_id', 'peer', 'tenant_id', 'tenant')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(peer__address__address__icontains=value) |
            Q(peer__remote_as=value) |
            Q(peer__description=value)
        )
        return queryset.filter(qs_filter).distinct()

    def filter_peer(self, queryset, name, value):
        assigned_objects = BGPPeer.objects.filter(**{'{}__in'.format(name): value})
        if not assigned_objects.exists():
            return queryset.none()
        ids = assigned_objects.values_list('id', flat=True)

        try:
            return queryset.filter(peer__in=ids)
        except ValidationError:
            return queryset.none()

    def filter_peertemplate(self, queryset, name, value):
        assigned_objects = BGPPeerTemplate.objects.filter(**{'{}__in'.format(name): value})
        if not assigned_objects.exists():
            return queryset.none()
        ids = assigned_objects.values_list('id', flat=True)

        try:
            return queryset.filter(peer__in=ids)
        except ValidationError:
            return queryset.none()


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
