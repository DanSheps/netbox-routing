import netaddr
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from netbox.models import PrimaryModel

from netbox_routing import choices
from netbox_routing.choices.ospf import (
    OSPFAreaTypeChoices,
    OSPFDefaultInformationOriginateChoices,
    OSPFMetricTypeChoices,
    OSPFNetworkTypeChoices,
)
from netbox_routing.constants import ERROR_UNIQUENESS_CONSTRAINT
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
    reference_bandwidth = models.PositiveIntegerField(
        verbose_name=_('Reference Bandwidth (Mbps)'),
        blank=True,
        null=True,
        validators=[MinValueValidator(1)],
    )
    timers_spf_initial = models.PositiveIntegerField(
        verbose_name=_('SPF Initial Delay (ms)'), blank=True, null=True
    )
    timers_spf_hold = models.PositiveIntegerField(
        verbose_name=_('SPF Hold Time (ms)'), blank=True, null=True
    )
    timers_spf_max = models.PositiveIntegerField(
        verbose_name=_('SPF Max Wait (ms)'), blank=True, null=True
    )
    timers_lsa_initial = models.PositiveIntegerField(
        verbose_name=_('LSA Initial Delay (ms)'), blank=True, null=True
    )
    timers_lsa_hold = models.PositiveIntegerField(
        verbose_name=_('LSA Hold Time (ms)'), blank=True, null=True
    )
    timers_lsa_max = models.PositiveIntegerField(
        verbose_name=_('LSA Max Wait (ms)'), blank=True, null=True
    )
    distance = models.PositiveSmallIntegerField(
        verbose_name=_('Distance'),
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(255)],
    )
    distance_intra_area = models.PositiveSmallIntegerField(
        verbose_name=_('Intra-Area Distance'),
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(255)],
    )
    distance_inter_area = models.PositiveSmallIntegerField(
        verbose_name=_('Inter-Area Distance'),
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(255)],
    )
    distance_external = models.PositiveSmallIntegerField(
        verbose_name=_('External Distance'),
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(255)],
    )
    default_information_originate = models.CharField(
        verbose_name=_('Default Information Originate'),
        max_length=50,
        choices=OSPFDefaultInformationOriginateChoices,
        blank=True,
        null=True,
    )
    default_information_metric = models.PositiveIntegerField(
        verbose_name=_('Default Information Metric'),
        blank=True,
        null=True,
        validators=[MaxValueValidator(16777214)],
    )
    default_information_metric_type = models.CharField(
        verbose_name=_('Default Information Metric Type'),
        max_length=50,
        choices=OSPFMetricTypeChoices,
        blank=True,
        null=True,
    )
    max_metric_router_lsa = models.BooleanField(
        verbose_name=_('Max Metric Router LSA'), blank=True, null=True
    )
    max_metric_on_startup = models.PositiveIntegerField(
        verbose_name=_('Max Metric On Startup (s)'),
        blank=True,
        null=True,
        validators=[MinValueValidator(5), MaxValueValidator(86400)],
    )
    passive_interface_default = models.BooleanField(
        verbose_name=_('Passive Interface Default'), blank=True, null=True
    )

    clone_fields = (
        'name',
        'router_id',
        'process_id',
        'device',
        'vrf',
        'reference_bandwidth',
        'timers_spf_initial',
        'timers_spf_hold',
        'timers_spf_max',
        'timers_lsa_initial',
        'timers_lsa_hold',
        'timers_lsa_max',
        'distance',
        'distance_intra_area',
        'distance_inter_area',
        'distance_external',
        'default_information_originate',
        'default_information_metric',
        'default_information_metric_type',
        'max_metric_router_lsa',
        'max_metric_on_startup',
        'passive_interface_default',
    )
    prerequisite_models = ('dcim.Device',)

    class Meta:
        ordering = ['vrf', 'router_id', 'process_id', 'pk']
        verbose_name = 'OSPF Instance'
        constraints = (
            models.UniqueConstraint(
                fields=('device', 'name'),
                name='%(app_label)s_%(class)s_unique_device_name',
                violation_error_message=ERROR_UNIQUENESS_CONSTRAINT,
                nulls_distinct=False,
            ),
        )

    def __str__(self):
        return f'{self.name} ({self.router_id})'

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:ospfinstance', args=[self.pk])

    def clean(self):
        super().clean()
        if not self.default_information_originate:
            errors = {
                field: _('Requires Default Information Originate')
                for field in (
                    'default_information_metric',
                    'default_information_metric_type',
                )
                if getattr(self, field) is not None
            }
            if errors:
                raise ValidationError(errors)


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
    clone_fields = ('area_id', 'area_type')

    class Meta:
        ordering = ['area_id', 'pk']
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
    interface = models.OneToOneField(
        to='dcim.Interface',
        related_name='ospf_interfaces',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    passive = models.BooleanField(verbose_name='Passive', blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    bfd = models.BooleanField(blank=True, null=True, verbose_name='BFD')
    network_type = models.CharField(
        verbose_name=_('Network Type'),
        max_length=50,
        choices=OSPFNetworkTypeChoices,
        blank=True,
        null=True,
    )
    authentication = models.CharField(
        max_length=50, choices=choices.AuthenticationChoices, blank=True, null=True
    )
    passphrase = models.CharField(max_length=200, blank=True, null=True)

    clone_fields = (
        'instance',
        'area',
        'interface',
        'passive',
        'priority',
        'bfd',
        'network_type',
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

    def __str__(self):
        return f'{self.interface.name}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:ospfinterface', args=[self.pk])
