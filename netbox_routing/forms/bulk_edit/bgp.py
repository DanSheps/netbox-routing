from django import forms
from django.utils.translation import gettext as _

from ipam.models import ASN, IPAddress, VRF
from netbox.forms import PrimaryModelBulkEditForm
from netbox_routing.forms.bulk_edit.base import EnableMixin, TenantBulkEditMixin
from netbox_routing.models import RouteMap, PrefixList
from utilities.forms.fields import (
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
)
from utilities.forms.rendering import FieldSet

from netbox_routing.choices.bgp import *
from netbox_routing.models.bgp import *

__all__ = (
    'BGPSettingBulkEditForm',
    'BGPRouterBulkEditForm',
    'BGPScopeBulkEditForm',
    'BGPAddressFamilyBulkEditForm',
    'BGPPeerTemplateBulkEditForm',
    'BGPPolicyTemplateBulkEditForm',
    'BGPSessionTemplateBulkEditForm',
    'BGPPeerBulkEditForm',
    'BGPPeerAddressFamilyBulkEditForm',
    'BFDProfileBulkEditForm',
)


class BGPPolicyMixin:
    prefix_list_in = DynamicModelChoiceField(
        label=_('Prefix List (in)'),
        queryset=PrefixList.objects.all(),
        required=False,
        selector=True,
    )
    prefix_list_out = DynamicModelChoiceField(
        label=_('Prefix List (out)'),
        queryset=PrefixList.objects.all(),
        required=False,
        selector=True,
    )
    routemap_in = DynamicModelChoiceField(
        label=_('Route Map (in)'),
        queryset=RouteMap.objects.all(),
        required=False,
        selector=True,
    )
    routemap_out = DynamicModelChoiceField(
        label=_('Route Map (out)'),
        queryset=RouteMap.objects.all(),
        required=False,
        selector=True,
    )


class BGPSessionMixin:
    remote_as = DynamicModelChoiceField(
        label=_('Remote AS'), queryset=ASN.objects.all(), required=False, selector=True
    )
    local_as = DynamicModelChoiceField(
        label=_('Local AS'), queryset=ASN.objects.all(), required=False, selector=True
    )


class BGPSettingBulkEditForm(TenantBulkEditMixin, PrimaryModelBulkEditForm):
    model = BGPSetting
    fieldsets = (
        FieldSet(
            'description',
        ),
    )
    nullable_fields = ('description',)


class BGPRouterBulkEditForm(TenantBulkEditMixin, PrimaryModelBulkEditForm):
    asn = DynamicModelChoiceField(
        label=_('ASN'), queryset=ASN.objects.all(), required=False, selector=True
    )
    peer_templates = DynamicModelMultipleChoiceField(
        label=_('Assigned Peer Template'),
        queryset=BGPPeerTemplate.objects.all(),
        required=False,
        selector=True,
    )
    policy_templates = DynamicModelMultipleChoiceField(
        label=_('Assigned Policy Template'),
        queryset=BGPPolicyTemplate.objects.all(),
        required=False,
        selector=True,
    )
    session_templates = DynamicModelMultipleChoiceField(
        label=_('Assigned Session Template'),
        queryset=BGPSessionTemplate.objects.all(),
        required=False,
        selector=True,
    )
    model = BGPRouter
    fieldsets = (
        FieldSet(
            'asn',
            'policy_templates',
            'session_templates',
            'peer_templates',
            'description',
        ),
        FieldSet('tenant', name=_('Tenancy')),
    )
    nullable_fields = (
        'policy_templates',
        'session_templates',
        'peer_templates',
        'description',
        'tenant',
    )


class BGPScopeBulkEditForm(TenantBulkEditMixin, PrimaryModelBulkEditForm):
    router = DynamicModelChoiceField(
        label=_('Router'),
        queryset=BGPRouter.objects.all(),
        required=False,
        selector=True,
    )
    vrf = DynamicModelChoiceField(
        label=_('VRF'), queryset=VRF.objects.all(), required=False, selector=True
    )
    model = BGPScope
    fieldsets = (
        FieldSet(
            'router',
            'vrf',
            'description',
        ),
        FieldSet('tenant', name=_('Tenancy')),
    )
    nullable_fields = (
        'router',
        'vrf',
        'description',
        'tenant',
    )


class BGPAddressFamilyBulkEditForm(TenantBulkEditMixin, PrimaryModelBulkEditForm):
    scope = DynamicModelChoiceField(
        label=_('Scope'), queryset=BGPScope.objects.all(), required=False, selector=True
    )
    address_family = forms.ChoiceField(
        label=_('Status'),
        choices=BGPAddressFamilyChoices,
        required=False,
    )
    model = BGPAddressFamily
    fieldsets = (
        FieldSet(
            'scope',
            'address_family',
            'description',
        ),
        FieldSet('tenant', name=_('Tenancy')),
    )
    nullable_fields = (
        'scope',
        'description',
        'tenant',
    )


class BGPPeerTemplateBulkEditForm(
    EnableMixin, TenantBulkEditMixin, PrimaryModelBulkEditForm
):
    asn = DynamicModelChoiceField(
        label=_('ASN'), queryset=ASN.objects.all(), required=False, selector=True
    )

    model = BGPPeerTemplate
    fieldsets = (
        FieldSet(
            'enabled',
            'remote_as',
        ),
        FieldSet('tenant', name=_('Tenancy')),
    )
    nullable_fields = (
        'remote_as',
        'enabled',
        'tenant',
    )


class BGPPolicyTemplateBulkEditForm(
    EnableMixin, BGPPolicyMixin, TenantBulkEditMixin, PrimaryModelBulkEditForm
):
    parents = DynamicModelMultipleChoiceField(
        label=_('Parent Policy Templates'),
        queryset=BGPPolicyTemplate.objects.all(),
        required=False,
        selector=True,
    )
    model = BGPPolicyTemplate
    fieldsets = (
        FieldSet(
            'enabled',
            'parents',
        ),
        FieldSet(
            'prefixlist_in',
            'prefixlist_out',
            'routemap_in',
            'routemap_out',
        ),
        FieldSet('tenant', name=_('Tenancy')),
    )
    nullable_fields = (
        'enabled',
        'parents',
        'prefixlist_in',
        'prefixlist_out',
        'routemap_in',
        'routemap_out',
        'tenant',
    )


class BGPSessionTemplateBulkEditForm(
    EnableMixin, BGPSessionMixin, TenantBulkEditMixin, PrimaryModelBulkEditForm
):
    parent = DynamicModelChoiceField(
        label=_('Parent'),
        queryset=BGPSessionTemplate.objects.all(),
        required=False,
        selector=True,
    )
    bfd = forms.BooleanField(label=_('BFD Enabled'), required=False)
    password = forms.CharField(label=_('Password'), required=False)

    model = BGPSessionTemplate
    fieldsets = (
        FieldSet(
            'parent',
            'enabled',
            'remote_as',
            'local_as',
            'bfd',
            'ttl',
            'password',
        ),
        FieldSet('tenant', name=_('Tenancy')),
    )
    nullable_fields = (
        'parent',
        'enabled',
        'remote_as',
        'local_as',
        'bfd',
        'ttl',
        'password',
        'tenant',
    )


class BGPPeerBulkEditForm(
    EnableMixin, BGPSessionMixin, TenantBulkEditMixin, PrimaryModelBulkEditForm
):
    scope = DynamicModelChoiceField(
        label=_('Scope'), queryset=BGPScope.objects.all(), required=False, selector=True
    )
    peer = DynamicModelChoiceField(
        label=_('Peer'), queryset=IPAddress.objects.all(), required=False, selector=True
    )
    source = DynamicModelChoiceField(
        label=_('Source'),
        queryset=IPAddress.objects.all(),
        required=False,
        selector=True,
    )
    peer_group = DynamicModelChoiceField(
        label=_('Peer Group'),
        queryset=BGPPeerTemplate.objects.all(),
        required=False,
        selector=True,
    )
    peer_session = DynamicModelChoiceField(
        label=_('Peer Session'),
        queryset=BGPSessionTemplate.objects.all(),
        required=False,
        selector=True,
    )
    bfd = forms.BooleanField(label=_('BFD Enabled'), required=False)
    password = forms.CharField(label=_('Password'), required=False)
    model = BGPPeer
    fieldsets = (
        FieldSet(
            'scope',
            'peer',
            'status',
            'enabled',
            'source',
            'remote_as',
            'local_as',
        ),
        FieldSet(
            'peer_group',
            'peer_session',
            'bfd',
            'ttl',
            'password',
        ),
        FieldSet('tenant', name=_('Tenancy')),
    )
    nullable_fields = (
        'source',
        'peer_group',
        'peer_session',
        'local_as',
        'status',
        'ttl',
        'enabled',
        'password',
        'tenant',
    )


class BGPPeerAddressFamilyBulkEditForm(
    EnableMixin, BGPPolicyMixin, TenantBulkEditMixin, PrimaryModelBulkEditForm
):
    peer_policy = DynamicModelChoiceField(
        label=_('Peer Policy'),
        queryset=BGPPolicyTemplate.objects.all(),
        required=False,
        selector=True,
    )
    model = BGPPeerAddressFamily
    fieldsets = (
        FieldSet(
            'enabled',
            'peer_policy',
        ),
        FieldSet(
            'prefixlist_out',
            'prefixlist_in',
            'routemap_out',
            'routemap_in',
        ),
        FieldSet('tenant', name=_('Tenancy')),
    )
    nullable_fields = (
        'peer_policy',
        'prefixlist_out',
        'prefixlist_in',
        'routemap_out',
        'routemap_in',
        'tenant',
    )


class BFDProfileBulkEditForm(TenantBulkEditMixin, PrimaryModelBulkEditForm):
    model = BFDProfile
    fieldsets = (
        FieldSet(
            'description',
        ),
        FieldSet(
            'min_tx_int',
            'min_rx_int',
            'multiplier',
            'hold',
        ),
        FieldSet('tenant', name=_('Tenancy')),
    )
    nullable_fields = (
        'hold',
        'description',
        'tenant',
    )
