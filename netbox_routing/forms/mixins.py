from django import forms
from django.contrib.contenttypes.models import ContentType
from django.forms import fields
from django.utils.translation import gettext as _

from netbox_routing.choices import BGPSettingChoices, BGPPolicySettingChoices
from netbox_routing.models import BGPSetting
from utilities.forms.rendering import FieldSet


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
