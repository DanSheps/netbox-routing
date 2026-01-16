from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext as _

from netbox.models import PrimaryModel

from netbox_routing.choices import ActionChoices, CommunityStatusChoices

__all__ = (
    'CommunityList',
    'Community',
)


class CommunityList(PrimaryModel):
    name = models.CharField(
        verbose_name=_('List'),
        max_length=255,
    )
    communities = models.ManyToManyField(
        verbose_name=_('Communities'),
        to='netbox_routing.Community',
        related_name='community_lists',
    )
    tenant = models.ForeignKey(
        verbose_name=_('Tenant'),
        to='tenancy.Tenant',
        on_delete=models.PROTECT,
        related_name='community_lists',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('Community List')
        verbose_name_plural = 'Community Lists'
        unique_together = ['name']
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse('plugins:netbox_routing:communitylist', args=[self.pk])


class Community(PrimaryModel):
    community = models.CharField(
        verbose_name=_('Community'),
        max_length=255,
        validators=[RegexValidator(r'^[\d\.]+(?::[\d\.]+(?::[\d\.]+)?)?$')],
    )

    status = models.CharField(
        max_length=50,
        choices=CommunityStatusChoices,
        default=CommunityStatusChoices.STATUS_ACTIVE,
    )
    role = models.ForeignKey(
        to='ipam.Role', on_delete=models.SET_NULL, null=True, blank=True
    )
    tenant = models.ForeignKey(
        verbose_name=_('Tenant'),
        to='tenancy.Tenant',
        on_delete=models.PROTECT,
        related_name='communities',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('Community')
        verbose_name_plural = 'Communities'
        ordering = ['community']

    def __str__(self):
        return f'{self.community}'

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse('plugins:netbox_routing:community', args=[self.pk])

    def get_status_color(self):
        return CommunityStatusChoices.colors.get(self.status)


class CommunityListEntry(PrimaryModel):
    """ """

    community_list = models.ForeignKey(
        to=CommunityList, on_delete=models.CASCADE, related_name='communitylistentries'
    )
    action = models.CharField(max_length=30, choices=ActionChoices)
    community = models.ForeignKey(
        to=Community,
        related_name='communitylistentries',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('community_list', 'community')

    def __str__(self):
        return f'{self.community_list}: {self.action} {self.community}'

    def get_action_color(self):
        return ActionChoices.colors.get(self.action)

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse('plugins:netbox_routing:communitylistentry', args=[self.pk])
