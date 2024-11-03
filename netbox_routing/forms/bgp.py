from django.contrib.contenttypes.models import ContentType
from django import forms
from django.forms import fields
from django.utils.translation import gettext as _


from dcim.models import Device
from ipam.models import ASN, VRF, IPAddress
from netbox.forms import NetBoxModelForm
from netbox_routing.choices.bgp import BGPSettingChoices, BGPAddressFamilyChoices, BGPPolicySettingChoices
from netbox_routing.models.bgp import *
from tenancy.models import Tenant
from utilities.forms.fields import DynamicModelChoiceField, CommentField, DynamicModelMultipleChoiceField
from utilities.forms.rendering import FieldSet, TabbedGroups
from utilities.forms.widgets import BulkEditNullBooleanSelect

__all__ = (
    'BGPRouterForm',
    'BGPScopeForm',
    'BGPSessionTemplateForm',
    'BGPPolicyTemplateForm',
    'BGPPeerTemplateForm',
    'BGPAddressFamilyForm',
    'BGPPeerForm',
    'BGPPeerAddressFamilyForm',
    'BGPSettingForm',
)


class BGPSettingMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_fields()

    def get_choice_types(self):
        classname = self.__class__.__name__
        if classname in ['BGPRouterForm', 'BGPScopeForm', ]:
            choices = BGPSettingChoices
        elif classname in ['BGPAddressFamilyForm', ]:
            choices = BGPPolicySettingChoices
        elif classname in ['BGPPeerTemplateForm', 'BGPPeerForm']:
            choices = None
        else:
            choices = None

        return choices

    def _init_fields(self):
        SettingChoices = self.get_choice_types()
        if SettingChoices is None:
            return

        for key, label in SettingChoices.CHOICES:
            initial = None
            if hasattr(self, 'instance'):
                setting = BGPSetting.objects.filter(
                    assigned_object_type=ContentType.objects.get_for_model(self.Meta.model),
                    assigned_object_id=self.instance.pk,
                    key=key
                ).first()
                if setting:
                    initial = setting.value
            if self.fields and key in self.fields:
                continue
            elif SettingChoices.FIELD_TYPES[key] == 'ipaddr':
                self.fields[key] = fields.CharField(
                    label=label,
                    required=False,
                    initial=initial,
                    max_length=128
                )
                css = self.fields[key].widget.attrs.get('class', '')
                self.fields[key].widget.attrs['class'] = f'{css} form-control'
            elif SettingChoices.FIELD_TYPES[key] == 'integer':
                self.fields[key] = fields.IntegerField(
                    label=label,
                    required=False,
                    initial=initial,
                    min_value=0,
                    max_value=65535
                )
                css = self.fields[key].widget.attrs.get('class', '')
                self.fields[key].widget.attrs['class'] = f'{css} form-control'
            elif SettingChoices.FIELD_TYPES[key] == 'boolean':
                choices = (
                    (None, '---------'),
                    (True, _('True')),
                    (False, _('False')),
                )
                self.fields[key] = fields.NullBooleanField(
                    label=label,
                    required=False,
                    initial=initial,
                    widget=forms.Select(choices=choices)
                )
                css = self.fields[key].widget.attrs.get('class', '')
                self.fields[key].widget.attrs['class'] = f'{css} form-control'

    def _append_settings_fields(self):
        choices = self.get_choice_types()
        if choices is None:
            return

        fieldset = FieldSet(
            *choices.FIELD_TYPES.keys(),
            name=_('Settings'),
        )
        return fieldset

    @property
    def fieldsets(self):
        fieldsets = list(self.get_fieldsets())

        settings_fieldset = self._append_settings_fields()
        if settings_fieldset:
            fieldsets.append(settings_fieldset)

        return fieldsets

    def _clean_fieldset(self):
        pass

    def save(self, *args, **kwargs):
        SettingChoices = self.get_choice_types()
        if SettingChoices is None:
            return super().save(*args, **kwargs)

        settings = {}
        for key, _ in SettingChoices.CHOICES:
            if key in self.cleaned_data:
                settings[key] = self.cleaned_data.pop(key)
        obj = super().save(*args, **kwargs)

        for key, _ in SettingChoices.CHOICES:
            value = settings.get(key, None)
            setting = BGPSetting.objects.filter(
                    assigned_object_type=self.get_assigned_object_type(),
                    assigned_object_id=self.get_assigned_object_id(),
                    key=key
            ).first()
            if setting is not None and value is not None and value != '':
                setting.value = settings.get(key)
                setting.clean()
                setting.save()
            elif value is not None and value != '':
                setting = BGPSetting(
                    assigned_object=self.instance,
                    key=key,
                    value=settings.get(key, None)
                )
                setting.clean()
                setting.save()
            elif setting is not None and (value is None or value == ''):
                setting.delete()

        return obj

    def get_assigned_object_type(self):
        return ContentType.objects.get_for_model(self.instance).pk

    def get_assigned_object_id(self):
        return self.instance.pk


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
