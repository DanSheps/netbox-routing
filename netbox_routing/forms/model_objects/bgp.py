from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.forms import fields
from django.utils.translation import gettext as _

from dcim.models import Device, Region, SiteGroup, Site, Location
from ipam.models import ASN, VRF, IPAddress
from netbox.forms import PrimaryModelForm
from tenancy.forms import TenancyForm
from utilities.forms.fields import (
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
)
from utilities.forms.rendering import FieldSet, TabbedGroups
from virtualization.models import Cluster, VirtualMachine, ClusterGroup

from netbox_routing.choices.bgp import *
from netbox_routing.models.objects import *
from netbox_routing.models.bgp import *

__all__ = (
    'BGPSettingForm',
    'BGPRouterForm',
    'BGPScopeForm',
    'BGPAddressFamilyForm',
    'BGPPeerForm',
    'BGPPeerAddressFamilyForm',
    'BGPPeerTemplateForm',
    'BGPPolicyTemplateForm',
    'BGPSessionTemplateForm',
    'BFDProfileForm',
)


class BGPSettingMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._append_settings_fields()

    def _append_settings_fields(self):
        fieldsets = list(self.fieldsets)
        assigned_fields = []
        setting_fields = [
            'router_id',
            'asdot',
            'timers_keepalive',
            'timers_hold',
            'auto_summary',
            'default_metric',
            'default_information_originate',
            'distance_ebgp',
            'distance_ibgp',
            'distance_embgp',
            'distance_imbgp',
            'paths_maximum',
            'paths_maximum_secondary',
            'graceful_restart',
            'additional_paths_receive',
            'additional_paths_send',
            'additional_paths_install',
            'test',
        ]
        for key, label in BGPSettingChoices.CHOICES:
            initial = None
            if hasattr(self, 'instance'):
                setting = BGPSetting.objects.filter(
                    assigned_object_type=ContentType.objects.get_for_model(
                        self.Meta.model
                    ),
                    assigned_object_id=self.instance.pk,
                    key=key,
                ).first()
                if setting:
                    initial = setting.value
            if BGPSettingChoices.FIELD_TYPES[key] == 'ipaddr':
                self.fields[key] = fields.CharField(
                    label=label, required=False, initial=initial, max_length=128
                )
                css = self.fields[key].widget.attrs.get('class', '')
                self.fields[key].widget.attrs['class'] = f'{css} form-control'
            elif BGPSettingChoices.FIELD_TYPES[key] == 'integer':
                self.fields[key] = fields.IntegerField(
                    label=label,
                    required=False,
                    initial=initial,
                    min_value=0,
                    max_value=65535,
                )
                css = self.fields[key].widget.attrs.get('class', '')
                self.fields[key].widget.attrs['class'] = f'{css} form-control'
            elif BGPSettingChoices.FIELD_TYPES[key] == 'boolean':
                choices = (
                    (None, '---------'),
                    (True, _('True')),
                    (False, _('False')),
                )
                self.fields[key] = fields.NullBooleanField(
                    label=label,
                    required=False,
                    initial=initial,
                    widget=forms.Select(choices=choices),
                )
                css = self.fields[key].widget.attrs.get('class', '')
                self.fields[key].widget.attrs['class'] = f'{css} form-control'
            assigned_fields.append(key)
            if key not in setting_fields:
                setting_fields.append(key)

        fieldset = FieldSet(
            *setting_fields,
            name=_('Settings'),
        )
        fieldsets.append(fieldset)
        if fieldset not in self.fieldsets:
            self.fieldsets = fieldsets

    def _clean_fieldset(self):
        pass

    def save(self, *args, **kwargs):
        settings = {}
        for key, name in BGPSettingChoices.CHOICES:
            if key in self.cleaned_data:
                settings[key] = self.cleaned_data.pop(key)
        obj = super().save(*args, **kwargs)

        for key, name in BGPSettingChoices.CHOICES:
            value = settings.get(key, None)
            setting = BGPSetting.objects.filter(
                assigned_object_type=self.get_assigned_object_type(),
                assigned_object_id=self.get_assigned_object_id(),
                key=key,
            ).first()
            # print(f'{key}')
            if setting and value:
                # print('\tPrev: {setting.value}')
                # print('\tNew: {value}')
                setting.value = settings.get(key)
                setting.clean()
                setting.save()
            elif value:
                # print('\tNew: {value}')
                setting = BGPSetting(
                    assigned_object=self.instance,
                    key=key,
                    value=settings.get(key, None),
                )
                setting.clean()
                setting.save()
            elif setting:
                # print('\tPrev: {setting.value}')
                setting.delete()

        return obj

    def get_assigned_object_type(self):
        return ContentType.objects.get_for_model(self.instance).pk

    def get_assigned_object_id(self):
        return self.instance.pk


class BGPSettingForm(PrimaryModelForm):

    router = DynamicModelChoiceField(
        queryset=BGPRouter.objects.all(),
        required=True,
        selector=True,
        label=_('Router'),
    )
    scope = DynamicModelChoiceField(
        queryset=BGPScope.objects.all(),
        required=True,
        selector=True,
        label=_('Scope'),
    )
    addressfamily = DynamicModelChoiceField(
        queryset=BGPAddressFamily.objects.all(),
        required=True,
        selector=True,
        label=_('Address Family'),
    )
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
        FieldSet(
            TabbedGroups(
                FieldSet('router', name=_('Router')),
                FieldSet('scope', name=_('Scope')),
                FieldSet('addressfamily', name=_('Address Family')),
            ),
            name='Assigned Object',
        ),
        FieldSet('key', 'value', name=_('Settings')),
    )

    class Meta:
        model = BGPSetting
        fields = [
            'router',
            'scope',
            'addressfamily',
            'key',
            'value',
            'tags',
            'owner',
        ]

    def __init__(self, *args, **kwargs):

        # Initialize helper selectors
        instance = kwargs.get('instance')
        initial = kwargs.get('initial', {}).copy()
        if instance:
            if type(instance.assigned_object) is BGPRouter:
                initial['router'] = instance.assigned_object
            elif type(instance.assigned_object) is BGPScope:
                initial['scope'] = instance.assigned_object
            elif type(instance.assigned_object) is BGPAddressFamily:
                initial['addressfamily'] = instance.assigned_object
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()

        # Handle object assignment
        selected_objects = [
            field
            for field in ('router', 'scope', 'addressfamily')
            if self.cleaned_data[field]
        ]
        if len(selected_objects) > 1:
            raise forms.ValidationError(
                {
                    selected_objects[1]: _(
                        "A BGP Setting can only be assigned to a single object."
                    )
                }
            )
        elif selected_objects:
            self.instance.assigned_object = self.cleaned_data[selected_objects[0]]
        else:
            raise ValidationError(_('A BGP Setting must be assigned to an object.'))


class BGPPeerTemplateForm(TenancyForm, PrimaryModelForm):
    remote_as = DynamicModelChoiceField(
        queryset=ASN.objects.all(),
        required=False,
        selector=True,
        label=_('Remote ASN'),
    )

    fieldsets = (
        FieldSet('name', 'remote_as', 'enabled'),
        FieldSet('tenant_group', 'tenant', name=_('Tenancy')),
    )

    class Meta:
        model = BGPPeerTemplate
        fields = [
            'name',
            'remote_as',
            'tenant_group',
            'tenant',
            'tags',
            'owner',
        ]


class BGPPolicyTemplateForm(TenancyForm, PrimaryModelForm):
    parents = DynamicModelMultipleChoiceField(
        queryset=BGPPeerTemplate.objects.all(),
        required=False,
        selector=True,
        label=_('Parent Policy Templates'),
    )
    prefixlist_out = DynamicModelChoiceField(
        queryset=PrefixList.objects.all(),
        required=False,
        selector=True,
        label=_('Prefix List (out)'),
    )
    prefixlist_in = DynamicModelChoiceField(
        queryset=PrefixList.objects.all(),
        required=False,
        selector=True,
        label=_('Prefix List (in)'),
    )
    routemap_out = DynamicModelChoiceField(
        queryset=RouteMap.objects.all(),
        required=False,
        selector=True,
        label=_('Route Map (out)'),
    )
    routemap_in = DynamicModelChoiceField(
        queryset=RouteMap.objects.all(),
        required=False,
        selector=True,
        label=_('Route Map (in)'),
    )

    fieldsets = (
        FieldSet(
            'name',
            'parents',
        ),
        FieldSet(
            'prefixlist_out',
            'prefixlist_in',
            'routemap_out',
            'routemap_in',
            name=_('Setings'),
        ),
        FieldSet('tenant_group', 'tenant', name=_('Tenancy')),
    )

    class Meta:
        model = BGPPolicyTemplate
        fields = [
            'name',
            'parents',
            'prefixlist_out',
            'prefixlist_in',
            'routemap_out',
            'routemap_in',
            'tenant_group',
            'tenant',
            'tags',
            'owner',
        ]


class BGPSessionTemplateForm(TenancyForm, PrimaryModelForm):
    parent = DynamicModelChoiceField(
        queryset=BGPSessionTemplate.objects.all(),
        required=False,
        selector=True,
        label=_('Parent Peer Template'),
    )
    remote_as = DynamicModelChoiceField(
        queryset=ASN.objects.all(),
        required=False,
        selector=True,
        label=_('Remote ASN'),
    )
    local_as = DynamicModelChoiceField(
        queryset=ASN.objects.all(),
        required=False,
        selector=True,
        label=_('Remote ASN'),
    )

    fieldsets = (
        FieldSet(
            'name',
            'parent',
            'remote_as',
            'local_as',
        ),
        FieldSet('pasword', 'bfd', 'ttl', 'enabled', name=_('Setings')),
        FieldSet('tenant_group', 'tenant', name=_('Tenancy')),
    )

    class Meta:
        model = BGPSessionTemplate
        fields = [
            'name',
            'parent',
            'enabled',
            'remote_as',
            'local_as',
            'bfd',
            'ttl',
            'password',
            'tenant_group',
            'tenant',
            'tags',
            'owner',
        ]


class BGPRouterForm(BGPSettingMixin, TenancyForm, PrimaryModelForm):
    region = DynamicModelChoiceField(
        queryset=Region.objects.all(),
        required=False,
        selector=True,
        label=_('Region'),
    )
    site_group = DynamicModelChoiceField(
        queryset=SiteGroup.objects.all(),
        required=False,
        selector=True,
        label=_('Site Group'),
    )
    site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        required=False,
        selector=True,
        label=_('Site'),
    )
    location = DynamicModelChoiceField(
        queryset=Location.objects.all(),
        required=False,
        selector=True,
        label=_('Location'),
    )
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
        label=_('Device'),
    )
    cluster_group = DynamicModelChoiceField(
        queryset=ClusterGroup.objects.all(),
        required=False,
        selector=True,
        label=_('Cluster Group'),
    )
    cluster = DynamicModelChoiceField(
        queryset=Cluster.objects.all(),
        required=False,
        selector=True,
        label=_('Cluster'),
    )
    virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        selector=True,
        label=_('Device'),
    )
    asn = DynamicModelChoiceField(
        queryset=ASN.objects.all(),
        required=True,
        selector=True,
        label=_('ASN'),
    )
    policy_templates = DynamicModelMultipleChoiceField(
        queryset=BGPPolicyTemplate.objects.all(),
        required=False,
        selector=False,
        label=_('Policy Templates'),
    )
    session_templates = DynamicModelMultipleChoiceField(
        queryset=BGPSessionTemplate.objects.all(),
        required=False,
        selector=False,
        label=_('Session Templates'),
    )
    peer_templates = DynamicModelMultipleChoiceField(
        queryset=BGPPeerTemplate.objects.all(),
        required=False,
        selector=False,
        label=_('Session Templates'),
    )

    fieldsets = [
        FieldSet(
            'name',
        ),
        FieldSet(
            TabbedGroups(
                FieldSet(
                    'region', 'site_group', 'site', 'location', name=_('Locations')
                ),
                FieldSet('device', name=_('Device')),
                FieldSet(
                    'cluster_group',
                    'cluster',
                    'virtual_machine',
                    name=_('Virtualization'),
                ),
            ),
            name=_('Assigned Object'),
        ),
        FieldSet('asn', name=_('Router')),
        FieldSet(
            'peer_templates',
            'policy_templates',
            'session_templates',
            name=_('Templates'),
        ),
        FieldSet('tenant_group', 'tenant', name=_('Tenancy')),
    ]

    class Meta:
        model = BGPRouter
        fields = [
            'name',
            'region',
            'site_group',
            'site',
            'location',
            'device',
            'cluster_group',
            'cluster',
            'virtual_machine',
            'asn',
            'policy_templates',
            'session_templates',
            'peer_templates',
            'tenant_group',
            'tenant',
            'tags',
            'owner',
        ]

    def __init__(self, *args, **kwargs):

        # Initialize helper selectors
        instance = kwargs.get('instance')
        initial = kwargs.get('initial', {}).copy()
        if instance:
            if type(instance.assigned_object) is Region:
                initial['region'] = instance.assigned_object
            elif type(instance.assigned_object) is SiteGroup:
                initial['site_group'] = instance.assigned_object
            elif type(instance.assigned_object) is Site:
                initial['site'] = instance.assigned_object
            elif type(instance.assigned_object) is Location:
                initial['location'] = instance.assigned_object
            elif type(instance.assigned_object) is Device:
                initial['device'] = instance.assigned_object
            elif type(instance.assigned_object) is ClusterGroup:
                initial['cluster_group'] = instance.assigned_object
            elif type(instance.assigned_object) is Cluster:
                initial['cluster'] = instance.assigned_object
            elif type(instance.assigned_object) is VirtualMachine:
                initial['virtual_machine'] = instance.assigned_object
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()

        # Handle object assignment
        selected_objects = [
            field
            for field in (
                'region',
                'site_group',
                'site',
                'location',
                'device',
                'cluster_group',
                'cluster',
                'virtual_machine',
            )
            if self.cleaned_data[field]
        ]
        if len(selected_objects) > 1:
            raise forms.ValidationError(
                {
                    selected_objects[1]: _(
                        "A BGP Router can only be assigned to a single object."
                    )
                }
            )
        elif selected_objects:
            self.instance.assigned_object = self.cleaned_data[selected_objects[0]]
        else:
            self.instance.assigned_object = None

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class BGPScopeForm(BGPSettingMixin, TenancyForm, PrimaryModelForm):
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

    fieldsets = (
        FieldSet('router', 'vrf', name=_('Scope')),
        FieldSet('tenant_group', 'tenant', name=_('Tenancy')),
    )

    class Meta:
        model = BGPScope
        fields = [
            'router',
            'vrf',
            'tenant_group',
            'tenant',
            'tags',
            'owner',
        ]

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class BGPAddressFamilyForm(BGPSettingMixin, TenancyForm, PrimaryModelForm):
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

    fieldsets = (
        FieldSet('scope', 'address_family', name=_('Address Family')),
        FieldSet('tenant_group', 'tenant', name=_('Tenancy')),
    )

    class Meta:
        model = BGPAddressFamily
        fields = [
            'scope',
            'address_family',
            'tenant_group',
            'tenant',
            'tags',
            'owner',
        ]

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class BGPPeerForm(BGPSettingMixin, TenancyForm, PrimaryModelForm):
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
        label=_('Peer'),
    )
    remote_as = DynamicModelChoiceField(
        queryset=ASN.objects.all(),
        required=False,
        selector=True,
        label=_('Remote AS'),
    )
    local_as = DynamicModelChoiceField(
        queryset=ASN.objects.all(),
        required=False,
        selector=True,
        label=_('Local AS'),
    )

    fieldsets = (
        FieldSet(
            'name',
        ),
        FieldSet('scope', 'peer', 'status', name=_('Peer')),
        FieldSet('remote_as', 'local_as', name=_('ASNs')),
        FieldSet('enabled', 'bfd', 'password', 'ttl', name=_('Peer Settings')),
        FieldSet('tenant_group', 'tenant', name=_('Tenancy')),
    )

    class Meta:
        model = BGPPeer
        fields = [
            'name',
            'scope',
            'peer',
            'remote_as',
            'local_as',
            'tenant',
            'enabled',
            'status',
            'ttl',
            'bfd',
            'password',
            'tenant_group',
            'tenant',
            'tags',
            'owner',
        ]

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class BGPPeerAddressFamilyForm(BGPSettingMixin, TenancyForm, PrimaryModelForm):
    peer = DynamicModelChoiceField(
        queryset=BGPPeer.objects.all(),
        required=False,
        selector=True,
        label=_('Peer'),
    )
    peer_group = DynamicModelChoiceField(
        queryset=BGPPeerTemplate.objects.all(),
        required=False,
        selector=True,
        label=_('Peer Group'),
    )
    address_family = DynamicModelChoiceField(
        queryset=BGPAddressFamily.objects.all(),
        required=True,
        selector=True,
        label=_('Address Family'),
    )

    prefix_list_in = DynamicModelChoiceField(
        queryset=PrefixList.objects.all(),
        required=False,
        selector=True,
        label=_('Prefix List (in)'),
    )
    prefix_list_out = DynamicModelChoiceField(
        queryset=PrefixList.objects.all(),
        required=False,
        selector=True,
        label=_('Prefix List (out)'),
    )
    route_map_in = DynamicModelChoiceField(
        queryset=RouteMap.objects.all(),
        required=False,
        selector=True,
        label=_('Prefix List (in)'),
    )
    route_map_out = DynamicModelChoiceField(
        queryset=RouteMap.objects.all(),
        required=False,
        selector=True,
        label=_('Prefix List (out)'),
    )

    fieldsets = (
        FieldSet(
            TabbedGroups(
                FieldSet('peer', name=_('Peer')),
                FieldSet('peer_group', name=_('Peer Group')),
            ),
            name=_('Assigned Object'),
        ),
        FieldSet('address_family', 'enabled'),
        FieldSet(
            'route_map_in',
            'route_map_out',
            'prefix_list_in',
            'prefix_list_out',
            name=_('Filtering'),
        ),
        FieldSet('tenant_group', 'tenant', name=_('Tenancy')),
    )

    class Meta:
        model = BGPPeerAddressFamily
        fields = [
            'peer',
            'peer_group',
            'address_family',
            'enabled',
            'route_map_in',
            'route_map_out',
            'prefix_list_in',
            'prefix_list_out',
            'tenant_group',
            'tenant',
            'tags',
            'owner',
        ]

    def __init__(self, *args, **kwargs):

        # Initialize helper selectors
        instance = kwargs.get('instance')
        initial = kwargs.get('initial', {}).copy()
        if instance:
            if type(instance.assigned_object) is BGPPeer:
                initial['peer'] = instance.assigned_object
            elif type(instance.assigned_object) is BGPPeerTemplate:
                initial['peer_group'] = instance.assigned_object
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()

        # Handle object assignment
        selected_objects = [
            field for field in ('peer', 'peer_group') if self.cleaned_data[field]
        ]
        if len(selected_objects) > 1:
            raise forms.ValidationError(
                {
                    selected_objects[1]: _(
                        "A BGP Peer Address Family can only be assigned to a single object."
                    )
                }
            )
        elif selected_objects:
            self.instance.assigned_object = self.cleaned_data[selected_objects[0]]
        else:
            raise ValidationError(
                _('A BGP Peer Address Family must specify an Peer or Peer Group.')
            )

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class BFDProfileForm(TenancyForm, PrimaryModelForm):

    fieldsets = (
        FieldSet(
            'name',
            'description',
        ),
        FieldSet(
            'min_tx_int',
            'min_tx_int',
            'multiplier',
            'hold',
            name=_('BFD Parameters'),
        ),
        FieldSet('tenant_group', 'tenant', name=_('Tenancy')),
    )

    class Meta:
        model = BFDProfile
        fields = [
            'name',
            'min_tx_int',
            'min_rx_int',
            'multiplier',
            'hold',
            'description',
            'comments',
            'tenant_group',
            'tenant',
            'tags',
            'owner',
        ]
