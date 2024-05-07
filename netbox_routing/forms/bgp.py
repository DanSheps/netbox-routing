from django.contrib.contenttypes.models import ContentType
from django import forms
from django.forms import fields
from django.utils.translation import gettext as _


from dcim.models import Device
from ipam.models import ASN, VRF
from netbox.forms import NetBoxModelForm
from netbox_routing.choices.bgp import BGPSettingChoices, BGPAddressFamilyChoices
from netbox_routing.models import BGPSetting, BGPRouter, BGPScope, BGPAddressFamily
from utilities.forms.fields import DynamicModelChoiceField


__all__ = (
    'BGPRouterForm',
    'BGPScopeForm',
    'BGPAddressFamilyForm',
    'BGPSettingForm',
)


class BGPSettingMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._append_settings_fields()


    def _append_settings_fields(self):
        assigned_fields = []
        fieldset = (
            _('Settings'), [
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
        )
        for key, label in BGPSettingChoices.CHOICES:
            initial = None
            if hasattr(self, 'instance'):
                setting = BGPSetting.objects.filter(
                        assigned_object_type=ContentType.objects.get_for_model(self.Meta.model),
                        assigned_object_id=self.instance.pk,
                        key=key
                ).first()
                if setting:
                    initial = setting.value
            if BGPSettingChoices.FIELD_TYPES[key] == 'ipaddr':
                self.fields[key] = fields.CharField(
                    label=label,
                    required=False,
                    initial=initial,
                    max_length=128
                )
                css = self.fields[key].widget.attrs.get('class', '')
                self.fields[key].widget.attrs['class'] = f'{css} form-control'
            elif BGPSettingChoices.FIELD_TYPES[key] == 'integer':
                self.fields[key] = fields.IntegerField(
                    label=label,
                    required=False,
                    initial=initial,
                    min_value=0,
                    max_value=65535
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
                    widget=forms.Select(choices=choices)
                )
                css = self.fields[key].widget.attrs.get('class', '')
                self.fields[key].widget.attrs['class'] = f'{css} form-control'
            assigned_fields.append(key)
            if key not in fieldset[1]:
                fieldset[1].append(key)
        if fieldset not in self.fieldsets:
            self.fieldsets.append(fieldset)

    def _clean_fieldset(self):
        pass

    def save(self, *args, **kwargs):
        settings = {}
        for key, _ in BGPSettingChoices.CHOICES:
            if key in self.cleaned_data:
                settings[key] = self.cleaned_data.pop(key)
        obj = super().save(*args, **kwargs)



        for key, _ in BGPSettingChoices.CHOICES:
            value = settings.get(key, None)
            setting = BGPSetting.objects.filter(
                    assigned_object_type=self.get_assigned_object_type(),
                    assigned_object_id=self.get_assigned_object_id(),
                    key=key
            ).first()
            print(f'{key}')
            if setting and value:
                print('\tPrev: {setting.value}')
                print('\tNew: {value}')
                setting.value = settings.get(key)
                setting.clean()
                setting.save()
            elif value:
                print('\tNew: {value}')
                setting = BGPSetting(
                    assigned_object=self.instance,
                    key=key,
                    value=settings.get(key, None)
                )
                setting.clean()
                setting.save()
            elif setting:
                print('\tPrev: {setting.value}')
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


    fieldsets = [
        (_('Router'), (
            'device', 'asn',
        )),
    ]

    class Meta:
        model = BGPRouter
        fields = ['device', 'asn', ]

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


    fieldsets = [
        (_('Scope'), (
            'router', 'vrf',
        )),
    ]

    class Meta:
        model = BGPScope
        fields = ['router', 'vrf', ]

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


    fieldsets = [
        (_('Address Family'), (
            'scope', 'address_family',
        )),
    ]

    class Meta:
        model = BGPAddressFamily
        fields = ['scope', 'address_family', ]

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


    fieldsets = [
        (_('Settings'), (
            'key', 'value',
        )),
    ]

    class Meta:
        model = BGPSetting
        fields = ['key', 'value', ]
