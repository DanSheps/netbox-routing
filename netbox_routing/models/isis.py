# SPDX-License-Identifier: Apache-2.0

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from netbox.models import PrimaryModel

from netbox_routing import choices
from netbox_routing.choices.isis import ISISSettingChoices
from netbox_routing.constants.isis import ISISSETTING_ASSIGNMENT_MODELS
from netbox_routing.models.base import SearchAttributeMixin

__all__ = (
    'ISISInstance',
    'ISISInterface',
    'ISISSetting',
    'ISISLevel',
    'ISISInterfaceLevel',
    'ISISSegmentRouting',
    'ISISFlexAlgo',
)


class ISISSetting(SearchAttributeMixin, PrimaryModel):
    """EAV long-tail for IS-IS scalars (mirrors BGPSetting).

    Attaches to an ISISInstance or ISISInterface via a generic FK; the
    divergent/long-tail knobs that don't warrant their own column live
    here as (key, value) pairs validated against ISISSettingChoices.
    """

    assigned_object_type = models.ForeignKey(
        verbose_name=_('Assigned Object Type'),
        to=ContentType,
        limit_choices_to=ISISSETTING_ASSIGNMENT_MODELS,
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        null=True,
    )
    assigned_object_id = models.PositiveBigIntegerField(
        verbose_name=_('Assigned Object ID'), blank=True, null=True
    )
    assigned_object = GenericForeignKey(
        ct_field='assigned_object_type', fk_field='assigned_object_id'
    )
    key = models.CharField(
        verbose_name=_('Setting Name'),
        max_length=64,
        choices=ISISSettingChoices,
    )
    value = models.CharField(
        verbose_name=_('Setting Value'),
        max_length=128,
    )

    class Meta:
        verbose_name = 'IS-IS Setting'
        verbose_name_plural = 'IS-IS Settings'
        ordering = (
            'assigned_object_type',
            'assigned_object_id',
            'key',
        )
        constraints = [
            models.UniqueConstraint(
                fields=('assigned_object_type', 'assigned_object_id', 'key'),
                name='netbox_routing_isissettings_unique',
            ),
            models.CheckConstraint(
                condition=models.Q(
                    assigned_object_type__isnull=False,
                    assigned_object_id__isnull=False,
                ),
                name='netbox_routing_isissetting_assignment_required',
            ),
        ]

    def clean(self):
        super().clean()
        # An ISISSetting is meaningless unless attached to an ISISInstance or
        # ISISInterface. ISISSettingForm.clean() already enforces this for the
        # UI; mirror it at the model layer so the API and bulk-import paths
        # cannot persist orphan rows either (the CheckConstraint is the DB
        # backstop, and NULLs would also defeat the unique constraint).
        if self.assigned_object_type_id is None or self.assigned_object_id is None:
            raise ValidationError(_('An IS-IS Setting must be assigned to an object.'))
        # NB: a *dangling* assigned_object_id (valid type, nonexistent row) is
        # already rejected by NetBox's base NetBoxModel.clean(), which validates
        # every GenericForeignKey's existence. See
        # ISISSettingAssignmentAPITestCase.test_create_with_nonexistent_object_is_rejected.
        # The assigned type must be an IS-IS model: limit_choices_to only constrains the
        # form picker, so without this the API/bulk-import paths could attach a setting to
        # an arbitrary object type and break the EAV contract.
        if (
            self.assigned_object_type.app_label != 'netbox_routing'
            or self.assigned_object_type.model not in ('isisinstance', 'isisinterface')
        ):
            raise ValidationError(
                {'assigned_object_type': _('IS-IS Setting must be assigned to an ISISInstance or ISISInterface.')}
            )
        # The value must match the type the key declares in ISISSettingChoices.FIELD_TYPES.
        # The typed Mixin enforces this for inline editing, but the standalone form / API /
        # import accept free-form text, so a typed knob (integer/boolean) could otherwise be
        # stored with a junk value. (The mixin persist path also calls clean(), so this is a
        # shared backstop.)
        field_type = ISISSettingChoices.FIELD_TYPES.get(self.key)
        if field_type == 'integer':
            try:
                parsed = int(self.value)
            except (TypeError, ValueError):
                raise ValidationError({'value': _('This setting requires an integer value.')})
            # Every integer ISIS setting is a count/timer/metric; the form enforces min_value=0,
            # so the model backstop (API/import/direct writes) must reject negatives too.
            if parsed < 0:
                raise ValidationError({'value': _('This setting requires a non-negative integer value.')})
        elif field_type == 'boolean':
            if str(self.value).strip().lower() not in ('true', 'false', '1', '0', 'yes', 'no'):
                raise ValidationError({'value': _('This setting requires a boolean value.')})

    def __str__(self):
        return f'{self.assigned_object}: {self.key}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:isissetting', args=[self.pk])


class ISISInstance(PrimaryModel):
    device = models.ForeignKey(
        verbose_name=_('Device'),
        to='dcim.Device',
        related_name='isis_instances',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    vrf = models.ForeignKey(
        verbose_name=_('VRF'),
        to='ipam.VRF',
        related_name='isis_instances',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    process_tag = models.CharField(
        verbose_name=_('Process Tag'),
        max_length=100,
        blank=True,
        default='',
        help_text=_(
            "IS-IS process area-tag; empty string for the untagged 'router isis' process"
        ),
    )
    net = models.CharField(
        verbose_name=_('NET'),
        max_length=100,
        blank=True,
        default='',
        help_text=_('Network Entity Title (e.g. 49.0001.0001.0001.0001.00)'),
    )
    is_type = models.CharField(
        verbose_name=_('IS type'),
        max_length=50,
        choices=choices.ISISIsTypeChoices,
        blank=True,
        default='',
        help_text=_('IS type — absent means IOS default (level-1-2)'),
    )
    metric_style = models.CharField(
        verbose_name=_('Metric style'),
        max_length=20,
        choices=choices.ISISMetricStyleChoices,
        blank=True,
        default='',
        help_text=_('Metric style: wide, narrow, or transition. Absent = IOS default (narrow).'),
    )
    overload_bit = models.BooleanField(
        verbose_name=_('Overload bit'),
        null=True,
        blank=True,
        help_text=_('Set the IS-IS overload bit (set-overload-bit).'),
    )
    area_auth_type = models.CharField(
        verbose_name=_('Area auth type'),
        max_length=10,
        choices=choices.ISISAuthTypeChoices,
        blank=True,
        default='',
        help_text=_('IS-IS area password authentication type (md5 or text).'),
    )
    area_auth_key = models.CharField(
        verbose_name=_('Area auth key'),
        max_length=128,
        blank=True,
        default='',
        help_text=_('IS-IS area password authentication key (plaintext — routing-protocol auth, not config access).'),
    )
    domain_auth_type = models.CharField(
        verbose_name=_('Domain auth type'),
        max_length=10,
        choices=choices.ISISAuthTypeChoices,
        blank=True,
        default='',
        help_text=_('IS-IS domain password authentication type (md5 or text).'),
    )
    domain_auth_key = models.CharField(
        verbose_name=_('Domain auth key'),
        max_length=128,
        blank=True,
        default='',
        help_text=_('IS-IS domain password authentication key (plaintext — routing-protocol auth, not config access).'),
    )
    # SPF / LSP timers — initial-delay and max-wait mean the same across Cisco,
    # Nokia, Junos and IOS-XR, so they get their own columns. The backoff
    # sub-knob (second-wait vs rapid-runs) diverges by algorithm → ISISSetting.
    spf_initial_wait = models.PositiveIntegerField(
        verbose_name=_('SPF initial wait'),
        blank=True,
        null=True,
        help_text=_('Initial SPF delay in milliseconds (Cisco initial-wait / Nokia spf-initial-wait / Junos delay).'),
    )
    spf_max_wait = models.PositiveIntegerField(
        verbose_name=_('SPF max wait'),
        blank=True,
        null=True,
        help_text=_('Maximum SPF wait in milliseconds (Cisco maximum-wait / Nokia spf-max-wait / Junos holddown).'),
    )
    lsp_initial_wait = models.PositiveIntegerField(
        verbose_name=_('LSP-gen initial wait'),
        blank=True,
        null=True,
        help_text=_('Initial LSP generation delay in milliseconds.'),
    )
    lsp_max_wait = models.PositiveIntegerField(
        verbose_name=_('LSP-gen max wait'),
        blank=True,
        null=True,
        help_text=_('Maximum LSP generation wait in milliseconds.'),
    )
    lsp_lifetime = models.PositiveIntegerField(
        verbose_name=_('LSP lifetime'),
        blank=True,
        null=True,
        help_text=_('Maximum LSP lifetime in seconds (max-lsp-lifetime).'),
    )
    lsp_refresh_interval = models.PositiveIntegerField(
        verbose_name=_('LSP refresh interval'),
        blank=True,
        null=True,
        help_text=_('LSP refresh interval in seconds (lsp-refresh-interval).'),
    )
    lsp_mtu = models.PositiveIntegerField(
        verbose_name=_('LSP MTU'),
        blank=True,
        null=True,
        help_text=_('LSP MTU / lsp-mtu-size in bytes.'),
    )
    overload_on_startup = models.BooleanField(
        verbose_name=_('Overload on startup'),
        blank=True,
        null=True,
        help_text=_('Set the overload bit on startup (set-overload-bit on-startup).'),
    )
    overload_timeout = models.PositiveIntegerField(
        verbose_name=_('Overload timeout'),
        blank=True,
        null=True,
        help_text=_('Seconds to keep the overload bit set after startup.'),
    )
    te_enabled = models.BooleanField(
        verbose_name=_('Traffic engineering'),
        blank=True,
        null=True,
        help_text=_('IS-IS traffic-engineering enabled.'),
    )
    sr_enabled = models.BooleanField(
        verbose_name=_('Segment routing'),
        blank=True,
        null=True,
        help_text=_('Segment routing (SR-MPLS) enabled for this instance.'),
    )
    sr_node_msd = models.PositiveSmallIntegerField(
        verbose_name=_('SR maximum SID depth'),
        blank=True,
        null=True,
        help_text=_('Segment routing maximum SID depth (MSD).'),
    )
    distance = models.PositiveSmallIntegerField(
        verbose_name=_('Administrative distance'),
        blank=True,
        null=True,
        help_text=_('Administrative distance / route preference.'),
    )
    maximum_paths = models.PositiveSmallIntegerField(
        verbose_name=_('Maximum paths'),
        blank=True,
        null=True,
        help_text=_('Maximum number of equal-cost paths (ECMP).'),
    )
    reference_bandwidth = models.PositiveBigIntegerField(
        verbose_name=_('Reference bandwidth'),
        blank=True,
        null=True,
        help_text=_('Auto-cost reference bandwidth (Mbps).'),
    )
    settings = GenericRelation(
        verbose_name=_('Settings'),
        to='netbox_routing.ISISSetting',
        related_name='isis_instance',
        related_query_name='isis_instance',
        content_type_field='assigned_object_type',
        object_id_field='assigned_object_id',
    )

    clone_fields = (
        'device', 'vrf', 'process_tag', 'is_type', 'metric_style',
        'spf_initial_wait', 'spf_max_wait', 'lsp_initial_wait', 'lsp_max_wait',
        'lsp_lifetime', 'lsp_refresh_interval', 'lsp_mtu', 'te_enabled',
        'sr_enabled', 'distance', 'maximum_paths', 'reference_bandwidth',
    )
    prerequisite_models = ('dcim.Device',)

    class Meta:
        ordering = ['device', 'process_tag']
        verbose_name = 'IS-IS Instance'
        constraints = [
            models.UniqueConstraint(
                fields=('device', 'process_tag'),
                name='netbox_routing_isisinstance_device_process_tag_unique',
            ),
        ]

    def clean(self):
        super().clean()
        # An authentication type and its key are only meaningful together;
        # reject half-configured pairs.
        errors = {}
        for type_field, key_field in (
            ('area_auth_type', 'area_auth_key'),
            ('domain_auth_type', 'domain_auth_key'),
        ):
            has_type = bool(getattr(self, type_field))
            has_key = bool(getattr(self, key_field))
            if has_type and not has_key:
                errors[key_field] = _(
                    'An authentication key is required when an authentication type is set.'
                )
            elif has_key and not has_type:
                errors[type_field] = _(
                    'An authentication type is required when an authentication key is set.'
                )
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        tag = self.process_tag or 'default'
        return f'{self.device} ({tag})'

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:isisinstance', args=[self.pk])


class ISISInterface(PrimaryModel):
    instance = models.ForeignKey(
        verbose_name=_('Instance'),
        to='netbox_routing.ISISInstance',
        related_name='interfaces',
        on_delete=models.PROTECT,
        blank=False,
        null=False,
    )
    interface = models.ForeignKey(
        verbose_name=_('Interface'),
        to='dcim.Interface',
        related_name='isis_interfaces',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    address_family = models.CharField(
        verbose_name=_('Address Family'),
        max_length=10,
        choices=choices.ISISAddressFamilyChoices,
    )
    circuit_type = models.CharField(
        verbose_name=_('Circuit Type'),
        max_length=20,
        choices=choices.ISISCircuitTypeChoices,
        blank=True,
        default='',
    )
    network_type = models.CharField(
        verbose_name=_('Network Type'),
        max_length=20,
        choices=choices.ISISNetworkTypeChoices,
        blank=True,
        default='',
    )
    metric = models.PositiveIntegerField(verbose_name=_('Metric'), blank=True, null=True)
    passive = models.BooleanField(verbose_name=_('Passive'), blank=True, null=True)
    hello_auth_type = models.CharField(
        verbose_name=_('Hello auth type'),
        max_length=10,
        choices=choices.ISISAuthTypeChoices,
        blank=True,
        default='',
        help_text=_('IS-IS per-interface hello (IIH) authentication type (md5 or text).'),
    )
    hello_auth_key = models.CharField(
        verbose_name=_('Hello auth key'),
        max_length=128,
        blank=True,
        default='',
        help_text=_('IS-IS per-interface hello (IIH) authentication key (plaintext — '
                    'routing-protocol auth, not config access).'),
    )
    bfd_enabled = models.BooleanField(
        verbose_name=_('BFD enabled'),
        blank=True,
        null=True,
        help_text=_('BFD enabled for IS-IS on this interface (timers come from the interface BFD config).'),
    )
    csnp_interval = models.PositiveIntegerField(
        verbose_name=_('CSNP interval'),
        blank=True,
        null=True,
        help_text=_('Complete Sequence Number PDU interval in seconds.'),
    )
    retransmit_interval = models.PositiveIntegerField(
        verbose_name=_('Retransmit interval'),
        blank=True,
        null=True,
        help_text=_('LSP retransmission interval in seconds.'),
    )
    lsp_interval = models.PositiveIntegerField(
        verbose_name=_('LSP interval'),
        blank=True,
        null=True,
        help_text=_('LSP transmission pacing interval in milliseconds '
                    '(Nokia lsp-pacing-interval / Junos lsp-interval).'),
    )
    mesh_group = models.CharField(
        verbose_name=_('Mesh group'),
        max_length=32,
        blank=True,
        default='',
        help_text=_("Mesh-group identifier, or 'blocked'."),
    )
    settings = GenericRelation(
        verbose_name=_('Settings'),
        to='netbox_routing.ISISSetting',
        related_name='isis_interface',
        related_query_name='isis_interface',
        content_type_field='assigned_object_type',
        object_id_field='assigned_object_id',
    )

    clone_fields = (
        'instance',
        'interface',
        'address_family',
        'circuit_type',
        'network_type',
        'metric',
        'passive',
        'hello_auth_type',
        'hello_auth_key',
        'bfd_enabled',
        'csnp_interval',
        'retransmit_interval',
        'lsp_interval',
        'mesh_group',
    )
    prerequisite_models = (
        'netbox_routing.ISISInstance',
        'dcim.Interface',
    )

    class Meta:
        verbose_name = 'IS-IS Interface'
        ordering = ('instance', 'interface')
        constraints = [
            models.UniqueConstraint(
                fields=('interface', 'address_family'),
                name='netbox_routing_isisinterface_interface_af_unique',
            ),
        ]

    def clean(self):
        super().clean()
        if (
            self.instance_id
            and self.interface_id
            and self.instance.device != self.interface.device
        ):
            raise ValidationError({
                'interface': _(
                    'The interface must belong to the same device as the IS-IS instance.'
                )
            })
        # Hello auth type and key are only meaningful together (mirrors ISISInstance).
        has_type = bool(self.hello_auth_type)
        has_key = bool(self.hello_auth_key)
        if has_type and not has_key:
            raise ValidationError({
                'hello_auth_key': _('An authentication key is required when a hello auth type is set.')
            })
        if has_key and not has_type:
            raise ValidationError({
                'hello_auth_type': _('An authentication type is required when a hello auth key is set.')
            })

    def __str__(self):
        return f'{self.interface} ({self.address_family})'

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:isisinterface', args=[self.pk])


class ISISLevel(PrimaryModel):
    """Per-level (L1/L2) tuning of an IS-IS instance.

    IS-IS knobs like default-metric and wide-metrics-only are configured
    independently per level on Nokia, Junos and IOS-XR — a structured child
    table rather than flat instance columns.
    """

    instance = models.ForeignKey(
        verbose_name=_('Instance'),
        to='netbox_routing.ISISInstance',
        related_name='levels',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    level = models.PositiveSmallIntegerField(
        verbose_name=_('Level'),
        choices=choices.ISISLevelChoices,
    )
    default_metric = models.PositiveIntegerField(
        verbose_name=_('Default metric'), blank=True, null=True
    )
    wide_metrics_only = models.BooleanField(
        verbose_name=_('Wide metrics only'), blank=True, null=True
    )
    preference = models.PositiveSmallIntegerField(
        verbose_name=_('Preference'), blank=True, null=True
    )
    labeled_preference = models.PositiveSmallIntegerField(
        verbose_name=_('Labeled preference'),
        blank=True,
        null=True,
        help_text=_('Route preference for SR-labeled (MPLS) paths at this level (Junos labeled-preference).'),
    )
    disabled = models.BooleanField(
        verbose_name=_('Disabled'),
        blank=True,
        null=True,
        help_text=_('Level explicitly disabled on this instance (e.g. Junos "level <n> disable").'),
    )
    auth_type = models.CharField(
        verbose_name=_('Auth type'),
        max_length=10,
        choices=choices.ISISAuthTypeChoices,
        blank=True,
        default='',
        help_text=_('Per-level authentication type (md5 or text).'),
    )
    auth_key = models.CharField(
        verbose_name=_('Auth key'),
        max_length=128,
        blank=True,
        default='',
        help_text=_('Per-level authentication key (plaintext — routing-protocol auth, not config access).'),
    )

    clone_fields = (
        'instance', 'default_metric', 'wide_metrics_only', 'preference', 'labeled_preference', 'disabled'
    )
    prerequisite_models = ('netbox_routing.ISISInstance',)

    class Meta:
        verbose_name = 'IS-IS Level'
        ordering = ('instance', 'level')
        constraints = [
            models.UniqueConstraint(
                fields=('instance', 'level'),
                name='netbox_routing_isislevel_instance_level_unique',
            ),
        ]

    def clean(self):
        super().clean()
        has_type = bool(self.auth_type)
        has_key = bool(self.auth_key)
        if has_type and not has_key:
            raise ValidationError({'auth_key': _('An authentication key is required when an auth type is set.')})
        if has_key and not has_type:
            raise ValidationError({'auth_type': _('An authentication type is required when an auth key is set.')})

    def __str__(self):
        return f'{self.instance} L{self.level}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:isislevel', args=[self.pk])


class ISISInterfaceLevel(PrimaryModel):
    """Per-level (L1/L2) tuning of an IS-IS interface.

    hello-interval, hello-multiplier, metric and priority are per-Level on
    Nokia, Junos and IOS-XR (interface.level[n]).
    """

    interface = models.ForeignKey(
        verbose_name=_('Interface'),
        to='netbox_routing.ISISInterface',
        related_name='levels',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    level = models.PositiveSmallIntegerField(
        verbose_name=_('Level'),
        choices=choices.ISISLevelChoices,
    )
    metric = models.PositiveIntegerField(verbose_name=_('Metric'), blank=True, null=True)
    hello_interval = models.PositiveIntegerField(
        verbose_name=_('Hello interval'), blank=True, null=True
    )
    hello_multiplier = models.PositiveIntegerField(
        verbose_name=_('Hello multiplier'), blank=True, null=True
    )
    priority = models.PositiveSmallIntegerField(
        verbose_name=_('Priority'), blank=True, null=True
    )
    passive = models.BooleanField(verbose_name=_('Passive'), blank=True, null=True)

    clone_fields = ('interface', 'metric', 'hello_interval', 'hello_multiplier', 'priority')
    prerequisite_models = ('netbox_routing.ISISInterface',)

    class Meta:
        verbose_name = 'IS-IS Interface Level'
        ordering = ('interface', 'level')
        constraints = [
            models.UniqueConstraint(
                fields=('interface', 'level'),
                name='netbox_routing_isisinterfacelevel_interface_level_unique',
            ),
        ]

    def __str__(self):
        return f'{self.interface} L{self.level}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:isisinterfacelevel', args=[self.pk])


class ISISSegmentRouting(PrimaryModel):
    """Segment Routing (SR-MPLS) configuration of an IS-IS instance (1:1)."""

    instance = models.OneToOneField(
        verbose_name=_('Instance'),
        to='netbox_routing.ISISInstance',
        related_name='segment_routing',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    enabled = models.BooleanField(verbose_name=_('Enabled'), blank=True, null=True)
    prefix_sid_range = models.CharField(
        verbose_name=_('Prefix-SID range'),
        max_length=32,
        blank=True,
        default='',
        help_text=_("Prefix-SID range: 'global' or a named/explicit range."),
    )
    srgb_start = models.PositiveIntegerField(
        verbose_name=_('SRGB start label'), blank=True, null=True
    )
    srgb_range = models.PositiveIntegerField(
        verbose_name=_('SRGB range size'), blank=True, null=True
    )
    node_sid_index = models.PositiveIntegerField(
        verbose_name=_('Node-SID index (IPv4)'), blank=True, null=True
    )
    node_sid_label = models.PositiveIntegerField(
        verbose_name=_('Node-SID label (IPv4)'), blank=True, null=True
    )
    node_sid_v6_index = models.PositiveIntegerField(
        verbose_name=_('Node-SID index (IPv6)'), blank=True, null=True
    )
    node_sid_v6_label = models.PositiveIntegerField(
        verbose_name=_('Node-SID label (IPv6)'), blank=True, null=True
    )
    maximum_sid_depth = models.PositiveSmallIntegerField(
        verbose_name=_('Maximum SID depth'), blank=True, null=True
    )
    tunnel_table_pref = models.PositiveSmallIntegerField(
        verbose_name=_('Tunnel-table preference'), blank=True, null=True
    )

    clone_fields = ('enabled', 'prefix_sid_range', 'srgb_start', 'srgb_range')
    prerequisite_models = ('netbox_routing.ISISInstance',)

    class Meta:
        verbose_name = 'IS-IS Segment Routing'
        verbose_name_plural = 'IS-IS Segment Routing'
        ordering = ('instance',)

    def __str__(self):
        return f'{self.instance} (SR)'

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:isissegmentrouting', args=[self.pk])


class ISISFlexAlgo(PrimaryModel):
    """A flexible-algorithm (Flex-Algo) definition used by an IS-IS instance.

    On Junos the definition lives under routing-options/flex-algorithm and the
    IS-IS instance participates via source-packet-routing/flex-algorithm; on
    Nokia it sits under isis/segment-routing/flexible-algorithms. Modeled here
    per (instance, algo_id) with the common definition knobs.
    """

    instance = models.ForeignKey(
        verbose_name=_('Instance'),
        to='netbox_routing.ISISInstance',
        related_name='flex_algos',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    algo_id = models.PositiveSmallIntegerField(
        verbose_name=_('Algorithm ID'),
        validators=[MinValueValidator(128), MaxValueValidator(255)],
        help_text=_('Flex-Algo identifier (128-255).'),
    )
    metric_type = models.CharField(
        verbose_name=_('Metric type'),
        max_length=40,
        blank=True,
        default='',
        help_text=_('Flex-Algo metric type (e.g. igp-metric, delay-metric, te-metric).'),
    )
    priority = models.PositiveSmallIntegerField(
        verbose_name=_('Priority'), blank=True, null=True
    )
    admin_group_exclude = models.CharField(
        verbose_name=_('Admin-group exclude'),
        max_length=200,
        blank=True,
        default='',
        help_text=_('Comma-separated affinity/admin-group names excluded from this algo.'),
    )
    admin_group_include_any = models.CharField(
        verbose_name=_('Admin-group include-any'),
        max_length=200,
        blank=True,
        default='',
        help_text=_('Comma-separated affinity/admin-group names (include-any).'),
    )
    admin_group_include_all = models.CharField(
        verbose_name=_('Admin-group include-all'),
        max_length=200,
        blank=True,
        default='',
        help_text=_('Comma-separated affinity/admin-group names (include-all).'),
    )

    clone_fields = ('instance', 'metric_type', 'priority')
    prerequisite_models = ('netbox_routing.ISISInstance',)

    class Meta:
        verbose_name = 'IS-IS Flex-Algo'
        ordering = ('instance', 'algo_id')
        constraints = [
            models.UniqueConstraint(
                fields=('instance', 'algo_id'),
                name='netbox_routing_isisflexalgo_instance_algo_id_unique',
            ),
        ]

    def __str__(self):
        return f'{self.instance} flex-algo {self.algo_id}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:isisflexalgo', args=[self.pk])
