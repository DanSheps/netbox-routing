from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from dcim.models import Interface, Device
from ipam.models import VRF
from netbox.forms import PrimaryModelForm
from utilities.forms import BOOLEAN_WITH_BLANK_CHOICES
from utilities.forms.fields import DynamicModelChoiceField
from utilities.forms.rendering import FieldSet

from virtualization.models import VirtualMachine

from netbox_routing.models import OSPFArea, OSPFInstance, OSPFInterface

__all__ = (
    'OSPFAreaForm',
    'OSPFInstanceForm',
    'OSPFInterfaceForm',
)



class OSPFInstanceForm(PrimaryModelForm):
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
        label=_('Device'),
    )
    virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        selector=True,
        label=_('Virtual Machine'),
    )
    vrf = DynamicModelChoiceField(
        queryset=VRF.objects.all(),
        required=False,
        selector=True,
        label=_('VRF'),
    )

    fieldsets = (
        FieldSet('name', 'description'),
        FieldSet('device', 'virtual_machine', name=_('Device')),
        FieldSet('process_id', 'router_id', 'vrf', name=_('Instance')),
    )

    class Meta:
        model = OSPFInstance
        fields = (
            'name',
            'router_id',
            'process_id',
            'vrf',
            'description',
            'comments',
            'tags',
            'owner',
        )

    def clean(self):
        super().clean()
        device = self.cleaned_data.get('device')
        virtual_machine = self.cleaned_data.get('virtual_machine')
        if not device and not virtual_machine:
            raise ValidationError(_('Either Device or Virtual Machine must be specified.'))
        if device and virtual_machine:
            raise ValidationError(_('Cannot specify both Device and Virtual Machine.'))

    def save(self, commit=True):
        instance = super().save(commit=False)
        device = self.cleaned_data.get('device')
        virtual_machine = self.cleaned_data.get('virtual_machine')
        if device:
            instance.device_type = ContentType.objects.get_for_model(Device)
            instance.device_id = device.pk
        elif virtual_machine:
            instance.device_type = ContentType.objects.get_for_model(VirtualMachine)
            instance.device_id = virtual_machine.pk
        if commit:
            instance.save()
            self.save_m2m()
        return instance

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.device_type and self.instance.device_id:
            ct = self.instance.device_type
            if ct.model == 'device':
                self.initial['device'] = self.instance.device_id
            elif ct.model == 'virtualmachine':
                self.initial['virtual_machine'] = self.instance.device_id


class OSPFAreaForm(PrimaryModelForm):

    class Meta:
        model = OSPFArea
        fields = (
            'area_id',
            'area_type',
            'description',
            'comments',
            'tags',
            'owner',
        )


from virtualization.models import VirtualMachine, VMInterface

class OSPFInterfaceForm(PrimaryModelForm):
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
        label=_('Device'),
    )
    virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        selector=True,
        label=_('Virtual Machine'),
    )
    instance = DynamicModelChoiceField(
        queryset=OSPFInstance.objects.all(),
        required=True,
        selector=True,
        label=_('Instance'),
    )
    area = DynamicModelChoiceField(
        queryset=OSPFArea.objects.all(),
        required=True,
        selector=True,
        label=_('Area'),
    )
    interface = DynamicModelChoiceField(
        queryset=Interface.objects.all(),
        required=False,
        selector=True,
        label=_('Interface (Device)'),
        query_params={'device_id': '$device'},
    )
    vm_interface = DynamicModelChoiceField(
        queryset=VMInterface.objects.all(),
        required=False,
        selector=True,
        label=_('Interface (VM)'),
        query_params={'virtual_machine_id': '$virtual_machine'},
    )

    fieldsets = (
        FieldSet('area', 'description', name=_('Session')),
        FieldSet('device', 'virtual_machine', 'instance', name=_('Instance')),
        FieldSet('interface', 'vm_interface', 'priority', 'passive', 'bfd', name=_('Interface')),
        FieldSet('authentication', 'passphrase', name=_('Authentication')),
    )

    class Meta:
        model = OSPFInterface
        fields = (
            'instance', 'area',
            'passive', 'priority', 'bfd',
            'authentication', 'passphrase',
            'description', 'comments', 'tags', 'owner',
        )
        widgets = {
            'bfd': forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
            'passive': forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
        }

    def clean(self):
        super().clean()
        interface = self.cleaned_data.get('interface')
        vm_interface = self.cleaned_data.get('vm_interface')
        if not interface and not vm_interface:
            raise ValidationError(_('Either Interface or VM Interface must be specified.'))
        if interface and vm_interface:
            raise ValidationError(_('Cannot specify both Interface and VM Interface.'))

    def save(self, commit=True):
        instance = super().save(commit=False)
        interface = self.cleaned_data.get('interface')
        vm_interface = self.cleaned_data.get('vm_interface')
        from django.contrib.contenttypes.models import ContentType
        if interface:
            instance.interface_type = ContentType.objects.get_for_model(Interface)
            instance.interface_id = interface.pk
        elif vm_interface:
            instance.interface_type = ContentType.objects.get_for_model(VMInterface)
            instance.interface_id = vm_interface.pk
        if commit:
            instance.save()
            self.save_m2m()
        return instance
