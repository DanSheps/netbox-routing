from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from django.db import models
from django.core.exceptions import ValidationError

from ipam.choices import IPAddressFamilyChoices
from ipam.fields import IPNetworkField
from netbox.models import PrimaryModel
from netbox_routing.choices import ActionChoices
from netbox_routing.constants.objects import PREFIX_ASSIGNMENT_MODELS

__all__ = (
    'ASPath',
    'ASPathEntry',
    'PrefixList',
    'PrefixListEntry',
    'CustomPrefix',
    'RouteMap',
    'RouteMapEntry',
)


class PermitDenyChoiceMixin:
    def get_action_color(self):
        return ActionChoices.colors.get(self.action)


class ASPath(PrimaryModel):
    name = models.CharField(max_length=100)

    clone_fields = ()
    prerequisite_models = ()

    class Meta:
        ordering = [
            'name',
        ]
        constraints = (
            models.UniqueConstraint(
                Lower('name'),
                name='%(app_label)s_%(class)s_unique_name',
                violation_error_message="Name must be unique.",
            ),
        )

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:aspath', args=[self.pk])


class ASPathEntry(PermitDenyChoiceMixin, PrimaryModel):
    aspath = models.ForeignKey(
        to=ASPath,
        on_delete=models.CASCADE,
        related_name='aspath_entries',
        verbose_name=_('AS-Path'),
    )
    sequence = models.PositiveSmallIntegerField()
    action = models.CharField(max_length=6, choices=ActionChoices)
    pattern = models.CharField(
        max_length=200,
    )

    clone_fields = (
        'aspath',
        'action',
    )
    prerequisite_models = ('netbox_routing.ASPath',)

    class Meta:
        ordering = ['aspath', 'sequence']
        constraints = (
            models.UniqueConstraint(
                fields=(
                    'aspath',
                    'sequence',
                ),
                name='%(app_label)s_%(class)s_unique_aspath_sequence',
                violation_error_message="Prefix List sequence must be unique.",
            ),
        )

    def __str__(self):
        # Workaround for bug with nulled aspath entry.
        if hasattr(self, 'aspath'):
            return f'{self.aspath.name} {self.action} {self.sequence}'
        return super().__str__()

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:aspathentry', args=[self.pk])


class PrefixList(PrimaryModel):
    name = models.CharField(max_length=100)
    family = models.PositiveSmallIntegerField(choices=IPAddressFamilyChoices, default=4)

    clone_fields = ()
    prerequisite_models = ()

    class Meta:
        ordering = [
            'name',
        ]
        constraints = (
            models.UniqueConstraint(
                Lower('name'),
                name='%(app_label)s_%(class)s_unique_name',
                violation_error_message="Name must be unique.",
            ),
        )

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:prefixlist', args=[self.pk])


class PrefixListEntry(PermitDenyChoiceMixin, PrimaryModel):
    prefix_list = models.ForeignKey(
        to=PrefixList,
        on_delete=models.CASCADE,
        related_name='prefix_list_entries',
        verbose_name='Prefix List',
    )
    assigned_prefix_type = models.ForeignKey(
        verbose_name=_('Prefix Type'),
        to=ContentType,
        limit_choices_to=PREFIX_ASSIGNMENT_MODELS,
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        null=True,
    )
    assigned_prefix_id = models.PositiveBigIntegerField(
        verbose_name=_('Prefix ID'), blank=True, null=True
    )
    assigned_prefix = GenericForeignKey(
        ct_field='assigned_prefix_type',
        fk_field='assigned_prefix_id',
    )
    sequence = models.PositiveSmallIntegerField()
    action = models.CharField(max_length=6, choices=ActionChoices)
    ge = models.PositiveSmallIntegerField(
        verbose_name='GE',
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(128)],
    )
    le = models.PositiveSmallIntegerField(
        verbose_name='LE',
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(128)],
    )

    clone_fields = (
        'prefix_list',
        'action',
    )
    prerequisite_models = ('netbox_routing.PrefixList',)

    class Meta:
        ordering = ['prefix_list', 'sequence']
        constraints = (
            models.UniqueConstraint(
                fields=(
                    'prefix_list',
                    'sequence',
                ),
                name='%(app_label)s_%(class)s_unique_prefixlist_sequence',
                violation_error_message="Prefix List sequence must be unique.",
            ),
        )

    def __str__(self):
        return f'{self.prefix_list.name} {self.action} {self.sequence}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:prefixlistentry', args=[self.pk])

    def clean(self):
        super().clean()
        if self.assigned_prefix:
            prefix = self.assigned_prefix.prefix
            boundary = 32 if prefix.version == 4 else 128

            if self.le is not None and self.le > boundary:
                raise ValidationError({'le': 'LE value cannot be longer then 32'})
            if self.ge is not None and self.ge > boundary:
                raise ValidationError({'ge': 'GE value cannot be longer then 32'})

            if self.ge and self.le and self.ge < self.le:
                raise ValidationError(
                    {
                        'ge': 'GE cannot be more then LE',
                        'le': 'LE cannot be less then GE',
                    }
                )

            if self.ge is not None and prefix.prefixlen >= self.ge:
                raise ValidationError(
                    'Prefix\'s length cannot be longer then greater or equals value'
                )

            if self.le is not None and prefix.prefixlen >= self.le:
                raise ValidationError(
                    'Prefix\'s length cannot be longer then greater or equals value'
                )


class CustomPrefix(PrimaryModel):
    prefix = IPNetworkField(help_text='IPv4 or IPv6 network with mask')

    prefix_list_enties = GenericRelation(
        verbose_name=_('Settings'),
        to='netbox_routing.PrefixListEntry',
        related_name='custom_prefixes',
        related_query_name='custom_prefixes',
        content_type_field='assigned_prefix_type',
        object_id_field='assigned_prefix_id',
    )

    clone_fields = ('prefix',)
    prerequisite_models = ()

    class Meta:
        ordering = [
            'prefix',
        ]
        constraints = (
            models.UniqueConstraint(
                fields=('prefix',),
                name='%(app_label)s_%(class)s_unique_prefix',
                violation_error_message="Prefix must be unique.",
            ),
        )

    def __str__(self):
        return f'{self.prefix}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:customprefix', args=[self.pk])


class RouteMap(PrimaryModel):
    name = models.CharField(max_length=100)

    clone_fields = ()
    prerequisite_models = ()

    class Meta:
        ordering = [
            'name',
        ]
        constraints = (
            models.UniqueConstraint(
                Lower('name'),
                name='%(app_label)s_%(class)s_unique_name',
                violation_error_message="Name must be unique.",
            ),
        )

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:routemap', kwargs={'pk': self.pk})


class RouteMapEntry(PermitDenyChoiceMixin, PrimaryModel):
    route_map = models.ForeignKey(
        to=RouteMap,
        on_delete=models.CASCADE,
        related_name='route_map_entries',
        verbose_name='Route Map',
    )
    action = models.CharField(max_length=6, choices=ActionChoices)
    sequence = models.PositiveSmallIntegerField()
    match = models.JSONField(
        blank=True,
        null=True,
        verbose_name=_('Set parameters'),
        help_text=_("JSON blob of options to match "),
    )
    set = models.JSONField(
        blank=True,
        null=True,
        verbose_name=_('Set parameters'),
        help_text=_("JSON blob of options to set "),
    )

    clone_fields = (
        'route_map',
        'action',
    )
    prerequisite_models = ('netbox_routing.RouteMap',)

    class Meta:
        ordering = ['route_map', 'sequence']
        constraints = (
            models.UniqueConstraint(
                fields=(
                    'route_map',
                    'sequence',
                ),
                name='%(app_label)s_%(class)s_unique_routemap_sequence',
                violation_error_message="Route Map sequence must be unique.",
            ),
        )

    def __str__(self):
        return f'{self.route_map.name} {self.action} {self.sequence}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:routemapentry', args=[self.pk])
