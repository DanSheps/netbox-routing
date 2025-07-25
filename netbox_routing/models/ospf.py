import netaddr
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from netbox.models import PrimaryModel

from netbox_routing import choices
from netbox_routing.choices.ospf import OSPFAreaTypeChoices
from netbox_routing.fields.ip import IPAddressField


__all__ = (
    'OSPFInstance',
    'OSPFArea',
    'OSPFInterface',
)


class OSPFInstance(PrimaryModel):
    name = models.CharField(max_length=100)
    router_id = IPAddressField(verbose_name=_('Router ID'))
    process_id = models.IntegerField(verbose_name=_('Process ID'))
    device = models.ForeignKey(
        to='dcim.Device',
        related_name='ospf_instances',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    vrf = models.ForeignKey(
        verbose_name=_('VRF'),
        to='ipam.VRF',
        related_name='ospf_instances',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    clone_fields = ('device',)
    prerequisite_models = ('dcim.Device',)

    class Meta:
        verbose_name = 'OSPF Instance'

    def __str__(self):
        return f'{self.name} ({self.router_id})'

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:ospfinstance', args=[self.pk])


class OSPFArea(PrimaryModel):
    area_id = models.CharField(max_length=100, verbose_name='Area ID')
    area_type = models.CharField(
        verbose_name=_('Area Type'),
        choices=OSPFAreaTypeChoices,
        blank=False,
        null=False,
        default='standard',
    )
    prerequisite_models = ()
    clone_fields = ()

    class Meta:
        verbose_name = 'OSPF Area'

    def __str__(self):
        return f'{self.area_id}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:ospfarea', args=[self.pk])

    def clean(self):
        super().clean()
        area_id = self.area_id
        try:
            int(area_id)
        except ValueError:
            try:
                str(netaddr.IPAddress(area_id))
            except netaddr.core.AddrFormatError:
                raise ValidationError(
                    {
                        'area_id': [
                            'This field must be an integer or a valid net address'
                        ]
                    }
                )


class OSPFInterface(PrimaryModel):
    instance = models.ForeignKey(
        to='netbox_routing.OSPFInstance',
        related_name='interfaces',
        on_delete=models.PROTECT,
        blank=False,
        null=False,
    )
    area = models.ForeignKey(
        to='netbox_routing.OSPFArea',
        on_delete=models.CASCADE,
        related_name='interfaces',
        blank=False,
        null=False,
    )
    interface = models.ForeignKey(
        to='dcim.Interface',
        related_name='ospf_interfaces',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    passive = models.BooleanField(verbose_name='Passive', blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    bfd = models.BooleanField(blank=True, null=True, verbose_name='BFD')
    authentication = models.CharField(
        max_length=50, choices=choices.AuthenticationChoices, blank=True, null=True
    )
    passphrase = models.CharField(max_length=200, blank=True, null=True)

    clone_fields = (
        'instance',
        'area',
        'priority',
        'bfd',
        'authentication',
        'passphrase',
    )
    prerequisite_models = (
        'netbox_routing.OSPFInstance',
        'netbox_routing.OSPFArea',
        'dcim.Interface',
    )

    class Meta:
        verbose_name = 'OSPF Interface'
        ordering = ('instance', 'area', 'interface')  # Name may be non-unique
        constraints = (
            models.UniqueConstraint(
                fields=('interface',), name='%(app_label)s_%(class)s_unique_interface'
            ),
        )

    def __str__(self):
        return f'{self.interface.name}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:ospfinterface', args=[self.pk])
