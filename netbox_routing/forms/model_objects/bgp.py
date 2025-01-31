from django import forms
from django.utils.translation import gettext as _

from dcim.models import Device
from ipam.models import ASN, VRF, IPAddress
from netbox.forms import NetBoxModelForm
from netbox_routing.choices import BGPAddressFamilyChoices, BGPSettingChoices
from netbox_routing.forms.mixins import BGPSettingMixin
from netbox_routing.models import BGPRouter, BGPScope, BGPPeerTemplate, BGPAddressFamily, BGPSessionTemplate, \
    BGPPolicyTemplate, BGPPeer, BGPPeerAddressFamily, BGPSetting
from tenancy.models import Tenant
from utilities.forms.fields import DynamicModelChoiceField, CommentField, DynamicModelMultipleChoiceField
from utilities.forms.rendering import FieldSet, TabbedGroups
from utilities.forms.widgets import BulkEditNullBooleanSelect


__all__ = (
    'BGPSettingForm',
    'BGPRouterForm',
    'BGPScopeForm',
    'BGPAddressFamilyForm',
    'BGPPeerTemplateForm',
    'BGPPolicyTemplateForm',
    'BGPSessionTemplateForm',
    'BGPPeerForm',
    'BGPPeerAddressFamilyForm',
)


class BGPRouterForm(BGPSettingMixin, NetBoxModelForm):
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=True,
        selector=True,
        label=_('Device'),
    )
    asn = DynamicModelChoiceField(
        queryset=ASN.objects.all(),
        required=True,
        selector=True,
        label=_('ASN'),
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        selector=True,
        label=_('Tenant')
    )
    comments = CommentField()

    class Meta:
        model = BGPRouter
        fields = ['device', 'asn', 'tenant', 'description', 'comments', ]

    def get_fieldsets(self):
        return (
            FieldSet('device', 'asn', name=_('Router')),
            FieldSet('tenant', 'description', name=_('Other')),
        )

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class BGPScopeForm(BGPSettingMixin, NetBoxModelForm):
    router = DynamicModelChoiceField(
        queryset=BGPRouter.objects.all(),
        required=True,
        selector=True,
        label=_('Router'),
    )
    vrf = DynamicModelChoiceField(
        queryset=VRF.objects.all(),
        required=False,
        selector=True,
        label=_('VRF'),
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        selector=True,
        label=_('Tenant')
    )
    comments = CommentField()

    class Meta:
        model = BGPScope
        fields = ['router', 'vrf', 'tenant', 'description', 'comments', ]

    def get_fieldsets(self):
        return (
            FieldSet('router', 'vrf', name=_('Scope')),
            FieldSet('tenant', 'description', name=_('Other')),
        )

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class BGPPeerTemplateForm(BGPSettingMixin, NetBoxModelForm):
    remote_as = DynamicModelChoiceField(
        queryset=ASN.objects.all(),
        required=False,
        selector=True,
        label=_('Remote AS'),
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        selector=True,
        label=_('Tenant')
    )
    comments = CommentField()

    class Meta:
        model = BGPPeerTemplate
        fields = ['name', 'remote_as', 'enabled', 'tenant', 'description', 'comments', ]

    def get_fieldsets(self):
        return (
            FieldSet('name', 'remote_as', 'enabled', name=_('Scope')),
            FieldSet('tenant', 'description', name=_('Other')),
        )

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class BGPAddressFamilyForm(BGPSettingMixin, NetBoxModelForm):
    scope = DynamicModelChoiceField(
        queryset=BGPScope.objects.all(),
        required=True,
        selector=True,
        label=_('Scope'),
    )
    address_family = forms.ChoiceField(
        choices=BGPAddressFamilyChoices,
        required=True,
        label=_('Address Family'),
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        selector=True,
        label=_('Tenant')
    )
    comments = CommentField()

    class Meta:
        model = BGPAddressFamily
        fields = ['scope', 'address_family', 'tenant', 'description', 'comments', ]

    def get_fieldsets(self):
        return (
            FieldSet('scope', 'address_family', name=_('Address Family')),
            FieldSet('tenant', 'description', name=_('Other')),
        )

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class BGPSessionTemplateForm(BGPSettingMixin, NetBoxModelForm):
    router = DynamicModelChoiceField(
        queryset=BGPRouter.objects.all(),
        required=True,
        selector=True,
        label=_('Router'),
    )
    parent = DynamicModelChoiceField(
        queryset=BGPSessionTemplate.objects.all(),
        required=True,
        selector=True,
        label=_('Parent Session Template'),
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        selector=True,
        label=_('Tenant')
    )
    comments = CommentField()

    class Meta:
        model = BGPSessionTemplate
        fields = [
            'name', 'router', 'parent', 'enabled', 'asn', 'bfd', 'password', 'tenant', 'description', 'comments',
        ]

    def fieldsets(self):
        return (
            FieldSet('name', 'router', 'parent'),
            FieldSet('enabled', 'asn', 'bfd', 'password', name=_('Settings')),
            FieldSet('tenant', 'description', name=_('Other')),
        )

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class BGPPolicyTemplateForm(BGPSettingMixin, NetBoxModelForm):
    router = DynamicModelChoiceField(
        queryset=BGPRouter.objects.all(),
        required=True,
        selector=True,
        label=_('Router'),
    )
    parents = DynamicModelMultipleChoiceField(
        queryset=BGPPolicyTemplate.objects.all(),
        label=_('Parents'),
        required=False
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        selector=True,
        label=_('Tenant')
    )
    comments = CommentField()

    class Meta:
        model = BGPPolicyTemplate
        fields = [
            'name', 'router', 'enabled', 'prefixlist_in', 'prefixlist_out', 'routemap_in', 'routemap_out',
            'tenant', 'description', 'comments',
        ]

    def fieldsets(self):
        return (
            FieldSet('name', 'router', 'enabled'),
            FieldSet('prefixlist_in', 'prefixlist_out', 'routemap_in', 'routemap_out', name=_('Filtering')),
            FieldSet('tenant', 'description', name=_('Other')),
        )

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class BGPPeerForm(BGPSettingMixin, NetBoxModelForm):
    scope = DynamicModelChoiceField(
        queryset=BGPScope.objects.all(),
        required=True,
        selector=True,
        label=_('Scope'),
    )
    peer = DynamicModelChoiceField(
        queryset=IPAddress.objects.all(),
        required=True,
        selector=True,
        label=_('Peer Address'),
    )
    remote_as = DynamicModelChoiceField(
        queryset=ASN.objects.all(),
        required=True,
        selector=True,
        label=_('Remote AS')
    )
    local_as = DynamicModelChoiceField(
        queryset=ASN.objects.all(),
        required=False,
        selector=True,
        label=_('Local AS')
    )
    enabled = forms.NullBooleanField(
        required=False,
        widget=BulkEditNullBooleanSelect,
        label=_('Enabled')
    )
    bfd = forms.NullBooleanField(
        required=False,
        widget=BulkEditNullBooleanSelect,
        label=_('BFD')
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        selector=True,
        label=_('Tenant')
    )
    comments = CommentField()

    class Meta:
        model = BGPPeer
        fields = [
            'scope', 'peer', 'remote_as', 'local_as', 'enabled', 'bfd', 'password', 'tenant', 'description', 'comments',
        ]
        verbose_name = _('BGP Peer')

    def fieldsets(self):
        return (
            FieldSet('scope', 'peer', 'remote_as', 'local_as', ),
            FieldSet('enabled', 'bfd', 'password', name=_('Peer')),
            FieldSet('tenant', 'description', name=_('Other')),
        )

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class BGPPeerAddressFamilyForm(NetBoxModelForm):
    peer_template = DynamicModelChoiceField(
        queryset=BGPPeerTemplate.objects.all(),
        required=False,
        context={
            'scope': 'scope',
        },
        selector=True,
        label=_('BGP Peer Template'),
    )
    peer = DynamicModelChoiceField(
        queryset=BGPPeer.objects.all(),
        required=False,
        context={
            'scope': 'scope',
        },
        selector=True,
        label=_('BGP Peer'),
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        selector=True,
        label=_('Tenant')
    )
    comments = CommentField()

    class Meta:
        model = BGPPeerAddressFamily
        fields = [
            'peer_template', 'peer', 'address_family', 'peer_policy', 'enabled', 'prefixlist_in', 'prefixlist_out',
            'routemap_in', 'routemap_out', 'tenant', 'description', 'comments', ]
        verbose_name = _('BGP Peer Address Family')

    def fieldsets(self):
        return (
            FieldSet(
                TabbedGroups(
                    FieldSet('peer_template', name=_('BGP Peer Template')),
                    FieldSet('peer', name=_('BGP Peer')),
                ),
                name=_('Assignment')
            ),
            FieldSet('address_family', 'peer_policy', 'enabled', ),
            FieldSet('prefixlist_in', 'prefixlist_out', 'routemap_in', 'routemap_out', name=_('Filtering')),
            FieldSet('tenant', 'description', name=_('Other')),
        )

    def __init__(self, *args, **kwargs):
        # Initialize helper selectors
        instance = kwargs.get('instance')
        initial = kwargs.get('initial', {}).copy()
        if instance:
            if type(instance.assigned_object) is BGPPeerTemplate:
                initial['peer_template'] = instance.assigned_object
            elif type(instance.assigned_object) is BGPPeer:
                initial['peer'] = instance.assigned_object
        kwargs['initial'] = initial

        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        selected_objects = [
            field for field in ('peer_template', 'peer', ) if self.cleaned_data[field]
        ]
        if len(selected_objects) > 1:
            raise forms.ValidationError({
                selected_objects[1]: _("An Peer address family can only be assigned to a single object.")
            })
        elif selected_objects:
            assigned_object = self.cleaned_data[selected_objects[0]]
            self.instance.assigned_object = assigned_object
        else:
            self.instance.assigned_object = None

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class BGPSettingForm(NetBoxModelForm):
    key = forms.ChoiceField(
        choices=BGPSettingChoices,
        required=True,
        label=_('Setting Name'),
    )
    value = forms.CharField(
        required=True,
        label=_('Setting Value'),
    )


    fieldsets = (
        FieldSet('key', 'value', name=_('Settings')),
    )

    class Meta:
        model = BGPSetting
        fields = ['key', 'value', ]
