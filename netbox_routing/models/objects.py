from django.urls import reverse

from django.db import models
from django.db.models import F, Q, CheckConstraint
from django.core.exceptions import ValidationError

from ipam.fields import IPNetworkField
from netbox.models import NetBoxModel
from netbox_routing.choices.objects import PermitDenyChoices


__all__ = (
    'RouteMap',
    'RouteMapEntry',
    'PrefixList',
    'PrefixListEntry'
)


class RouteMap(NetBoxModel):
    name = models.CharField(
        max_length=255
    )

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:routemap', args=[self.pk])

class RouteMapEntry(NetBoxModel):
    route_map = models.ForeignKey(
        to="netbox_routing.RouteMap",
        on_delete=models.PROTECT,
        related_name='entries',
        verbose_name='Route Map'
    )
    type = models.CharField(max_length=6, choices=PermitDenyChoices)
    sequence = models.PositiveSmallIntegerField()

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:routemapentry', args=[self.pk])


class PrefixList(NetBoxModel):
    name = models.CharField(
        max_length=255
    )

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:prefixlist', args=[self.pk])


class PrefixListEntry(NetBoxModel):
    prefix_list = models.ForeignKey(
        to="netbox_routing.PrefixList",
        on_delete=models.PROTECT,
        related_name='entries',
        verbose_name='Prefix List'
    )
    sequence = models.PositiveSmallIntegerField()
    type = models.CharField(max_length=6, choices=PermitDenyChoices)
    prefix = IPNetworkField(help_text='IPv4 or IPv6 network with mask')
    ge = models.PositiveSmallIntegerField()
    le = models.PositiveSmallIntegerField()

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:prefixlistentry', args=[self.pk])

    def clean(self):
        super().clean()

        if self.prefix.version == 6:
            if self.le is not None and self.le > 128:
                raise ValidationError({
                    'le': 'LE value cannot be longer then 128'
                })
            if self.ge is not None and self.ge > 128:
                raise ValidationError({
                    'ge': 'GE value cannot be longer then 128'
                })
        elif self.prefix.version == 4:
            if self.le is not None and self.le > 32:
                raise ValidationError({
                    'le': 'LE value cannot be longer then 32'
                })
            if self.ge is not None and self.ge > 32:
                raise ValidationError({
                    'ge': 'GE value cannot be longer then 32'
                })

        if self.ge and self.le and self.ge < self.le:
            raise ValidationError({
                    'ge': 'GE cannot be more then LE',
                    'le': 'LE cannot be less then GE'
            })

        if self.ge is not None and self.prefix.prefix.prefixlen >= self.ge:
            raise ValidationError('Prefix\'s length cannot be longer then greater or equals value')

        if self.le is not None and self.prefix.prefix.prefixlen >= self.le:
            raise ValidationError('Prefix\'s length cannot be longer then greater or equals value')

