from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from ipam.choices import IPAddressFamilyChoices
from netbox.models import PrimaryModel
from netbox_routing import choices
from netbox_routing.choices.eigrp import EIGRPRouterChoices
from netbox_routing.fields.ip import IPAddressField

__all__ = (
    'EIGRPRouter',
    'EIGRPAddressFamily',
    'EIGRPNetwork',
    'EIGRPInterface',
)


class EIGRPRouter(PrimaryModel):
    device = models.ForeignKey(
        verbose_name=_('Device'),
        to='dcim.Device',
        related_name='eigrp',
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    mode = models.CharField(
        verbose_name=_('Mode'),
        max_length=10,
        choices=EIGRPRouterChoices
    )
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=100,
        blank=True,
        null=True
    )
    pid = models.PositiveIntegerField(
        verbose_name=_('Process ID'),
        blank=True,
        null=True
    )
    rid = IPAddressField(
        verbose_name=_('Router ID'),
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'EIGRP Router'

    def __str__(self):
        if self.pid:
            return f'Process {self.pid} ({self.rid})'
        return f'{self.name} ({self.rid})'

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:eigrprouter', args=[self.pk])

    @property
    def identifier(self):
        if self.name:
            return f'{self.name}'
        elif self.pid:
            return f'{self.pid}'
        return f'{self}'


class EIGRPAddressFamily(PrimaryModel):
    router = models.ForeignKey(
        verbose_name=_('Router'),
        to=EIGRPRouter,
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    vrf = models.ForeignKey(
        verbose_name=_('VRF'),
        to='ipam.VRF',
        related_name='eigrp_address_families',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    family = models.PositiveSmallIntegerField(
        verbose_name=_('Address Family'),
        choices=IPAddressFamilyChoices,
        blank=False,
        null=False
    )
    rid = IPAddressField(
        verbose_name=_('Router ID'),
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'EIGRP Address Family'
        constraints = (
            models.UniqueConstraint(
                fields=('router', 'vrf', 'family'),
                name='%(app_label)s_%(class)s_unique_af'
            ),
        )

    def __str__(self):
        if self.vrf:
            return f'{self.router.identifier} ({self.family} vrf {self.vrf.name})'
        return f'{self.router.identifier} ({self.family})'

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:eigrpaddressfamily', args=[self.pk])


class EIGRPNetwork(PrimaryModel):
    router = models.ForeignKey(
        verbose_name=_('Router'),
        to=EIGRPRouter,
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    address_family = models.ForeignKey(
        verbose_name=_('Address Family'),
        to=EIGRPAddressFamily,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    network = models.ForeignKey(
        verbose_name=_('Network'),
        to='ipam.Prefix',
        related_name='eigrp',
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )

    class Meta:
        verbose_name = 'EIGRP Network'
        constraints = (
            models.UniqueConstraint(
                fields=('router', 'address_family', 'network',),
                name='%(app_label)s_%(class)s_unique_network'
            ),
        )

    def __str__(self):
        if self.address_family:
            return f'{self.network} ({self.router.identifier} {self.address_family})'
        return f'{self.network} ({self.router.identifier})'

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:eigrpnetwork', args=[self.pk])


class EIGRPInterface(PrimaryModel):
    router = models.ForeignKey(
        verbose_name=_('Router'),
        to=EIGRPRouter,
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    address_family = models.ForeignKey(
        verbose_name=_('Address Family'),
        to=EIGRPAddressFamily,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    interface = models.ForeignKey(
        verbose_name=_('Interface'),
        to='dcim.Interface',
        related_name='eigrp',
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    passive = models.BooleanField(
        verbose_name=_('Passive'),
    )
    bfd = models.BooleanField(
        verbose_name=_('BFD'),
    )
    authentication = models.CharField(
        verbose_name=_('Authentication'),
        max_length=50,
        choices=choices.AuthenticationChoices,
        blank=True,
        null=True
    )
    passphrase = models.CharField(
        verbose_name=_('Passphrase'),
        max_length=200,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'EIGRP Interface'
        constraints = (
            models.UniqueConstraint(
                fields=('router', 'address_family', 'interface',),
                name='%(app_label)s_%(class)s_unique_interface'
            ),
        )

    def __str__(self):
        if self.address_family:
            return f'{self.interface.name} ({self.router.identifier} {self.address_family})'
        return f'{self.interface.name} ({self.router.identifier})'

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:eigrpinterface', args=[self.pk])
