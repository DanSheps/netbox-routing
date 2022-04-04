from dcim.models import Device
from ipam.models import VRF
from netbox.forms import NetBoxModelForm
from netbox_routing.models import StaticRoute
from utilities.forms.fields import DynamicModelChoiceField, DynamicModelMultipleChoiceField


class StaticRouteForm(NetBoxModelForm):
    devices = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all()
    )
    vrf = DynamicModelChoiceField(
        queryset=VRF.objects.all(),
        required=False,
        label='VRF'
    )

    class Meta:
        model = StaticRoute
        fields = ('devices', 'vrf', 'prefix', 'next_hop', 'name', 'metric', 'permanent')

    def __init__(self, data=None, instance=None, *args, **kwargs):
        super().__init__(data=data, instance=instance, *args, **kwargs)

        if self.instance and self.instance.pk is not None:
            self.fields['devices'].initial = self.instance.devices.all().values_list('id', flat=True)

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        instance.devices.set(self.cleaned_data['devices'])
        return instance
