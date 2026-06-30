# SPDX-License-Identifier: Apache-2.0

import django.core.validators
import django.db.models.deletion
import netbox.models.deletion
import taggit.managers
import utilities.json
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('dcim', '0234_cablepath_nodes_index'),
        ('extras', '0138_customfieldchoiceset_choice_colors'),
        ('ipam', '0089_default_ordering_indexes'),
        ('netbox_routing', '0032_fix_eigrp_router_ordering'),
        ('users', '0016_default_ordering_indexes'),
    ]

    operations = [
        migrations.CreateModel(
            name='ISISInstance',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                (
                    'custom_field_data',
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder,
                    ),
                ),
                ('description', models.CharField(blank=True, max_length=200)),
                ('comments', models.TextField(blank=True)),
                (
                    'process_tag',
                    models.CharField(blank=True, default='', max_length=100),
                ),
                ('net', models.CharField(blank=True, default='', max_length=100)),
                ('is_type', models.CharField(blank=True, default='', max_length=50)),
                (
                    'metric_style',
                    models.CharField(blank=True, default='', max_length=20),
                ),
                ('overload_bit', models.BooleanField(blank=True, null=True)),
                (
                    'area_auth_type',
                    models.CharField(blank=True, default='', max_length=10),
                ),
                (
                    'area_auth_key',
                    models.CharField(blank=True, default='', max_length=128),
                ),
                (
                    'domain_auth_type',
                    models.CharField(blank=True, default='', max_length=10),
                ),
                (
                    'domain_auth_key',
                    models.CharField(blank=True, default='', max_length=128),
                ),
                (
                    'device',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='isis_instances',
                        to='dcim.device',
                    ),
                ),
                (
                    'owner',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to='users.owner',
                    ),
                ),
                (
                    'tags',
                    taggit.managers.TaggableManager(
                        through='extras.TaggedItem', to='extras.Tag'
                    ),
                ),
                (
                    'vrf',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='isis_instances',
                        to='ipam.vrf',
                    ),
                ),
                ('distance', models.PositiveSmallIntegerField(blank=True, null=True)),
                (
                    'lsp_initial_wait',
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                ('lsp_lifetime', models.PositiveIntegerField(blank=True, null=True)),
                ('lsp_max_wait', models.PositiveIntegerField(blank=True, null=True)),
                ('lsp_mtu', models.PositiveIntegerField(blank=True, null=True)),
                (
                    'lsp_refresh_interval',
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                (
                    'maximum_paths',
                    models.PositiveSmallIntegerField(blank=True, null=True),
                ),
                ('overload_on_startup', models.BooleanField(blank=True, null=True)),
                (
                    'overload_timeout',
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                (
                    'reference_bandwidth',
                    models.PositiveBigIntegerField(blank=True, null=True),
                ),
                (
                    'spf_initial_wait',
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                ('spf_max_wait', models.PositiveIntegerField(blank=True, null=True)),
                ('te_enabled', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'IS-IS Instance',
                'ordering': ['device', 'process_tag'],
                'constraints': [
                    models.UniqueConstraint(
                        fields=('device', 'process_tag'),
                        name='netbox_routing_isisinstance_device_process_tag_unique',
                    )
                ],
            },
            bases=(netbox.models.deletion.DeleteMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ISISInterface',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                (
                    'custom_field_data',
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder,
                    ),
                ),
                ('description', models.CharField(blank=True, max_length=200)),
                ('comments', models.TextField(blank=True)),
                ('address_family', models.CharField(max_length=10)),
                (
                    'circuit_type',
                    models.CharField(blank=True, default='', max_length=20),
                ),
                (
                    'network_type',
                    models.CharField(blank=True, default='', max_length=20),
                ),
                ('metric', models.PositiveIntegerField(blank=True, null=True)),
                ('passive', models.BooleanField(blank=True, null=True)),
                (
                    'instance',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='interfaces',
                        to='netbox_routing.isisinstance',
                    ),
                ),
                (
                    'interface',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='isis_interfaces',
                        to='dcim.interface',
                    ),
                ),
                (
                    'owner',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to='users.owner',
                    ),
                ),
                (
                    'tags',
                    taggit.managers.TaggableManager(
                        through='extras.TaggedItem', to='extras.Tag'
                    ),
                ),
                (
                    'hello_auth_type',
                    models.CharField(blank=True, default='', max_length=10),
                ),
                (
                    'hello_auth_key',
                    models.CharField(blank=True, default='', max_length=128),
                ),
                ('bfd_enabled', models.BooleanField(blank=True, null=True)),
                ('csnp_interval', models.PositiveIntegerField(blank=True, null=True)),
                ('lsp_interval', models.PositiveIntegerField(blank=True, null=True)),
                ('mesh_group', models.CharField(blank=True, default='', max_length=32)),
                (
                    'retransmit_interval',
                    models.PositiveIntegerField(blank=True, null=True),
                ),
            ],
            options={
                'verbose_name': 'IS-IS Interface',
                'ordering': ('instance', 'interface'),
                'constraints': [
                    models.UniqueConstraint(
                        fields=('interface', 'address_family'),
                        name='netbox_routing_isisinterface_interface_af_unique',
                    )
                ],
            },
            bases=(netbox.models.deletion.DeleteMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ISISSetting',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                (
                    'custom_field_data',
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder,
                    ),
                ),
                ('description', models.CharField(blank=True, max_length=200)),
                ('comments', models.TextField(blank=True)),
                (
                    'assigned_object_id',
                    models.PositiveBigIntegerField(blank=True, null=True),
                ),
                ('key', models.CharField(max_length=64)),
                ('value', models.CharField(max_length=128)),
                (
                    'assigned_object_type',
                    models.ForeignKey(
                        blank=True,
                        limit_choices_to=models.Q(
                            models.Q(
                                models.Q(
                                    ('app_label', 'netbox_routing'),
                                    ('model', 'isisinstance'),
                                ),
                                models.Q(
                                    ('app_label', 'netbox_routing'),
                                    ('model', 'isisinterface'),
                                ),
                                _connector='OR',
                            )
                        ),
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='+',
                        to='contenttypes.contenttype',
                    ),
                ),
                (
                    'owner',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to='users.owner',
                    ),
                ),
                (
                    'tags',
                    taggit.managers.TaggableManager(
                        through='extras.TaggedItem', to='extras.Tag'
                    ),
                ),
            ],
            options={
                'verbose_name': 'IS-IS Setting',
                'verbose_name_plural': 'IS-IS Settings',
                'ordering': ('assigned_object_type', 'assigned_object_id', 'key'),
                'constraints': [
                    models.UniqueConstraint(
                        fields=('assigned_object_type', 'assigned_object_id', 'key'),
                        name='netbox_routing_isissettings_unique',
                    ),
                    models.CheckConstraint(
                        condition=models.Q(
                            ('assigned_object_id__isnull', False),
                            ('assigned_object_type__isnull', False),
                        ),
                        name='netbox_routing_isissetting_assignment_required',
                    ),
                ],
            },
            bases=(netbox.models.deletion.DeleteMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ISISSegmentRouting',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                (
                    'custom_field_data',
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder,
                    ),
                ),
                ('description', models.CharField(blank=True, max_length=200)),
                ('comments', models.TextField(blank=True)),
                ('enabled', models.BooleanField(blank=True, null=True)),
                (
                    'prefix_sid_range',
                    models.CharField(blank=True, default='', max_length=32),
                ),
                ('srgb_start', models.PositiveIntegerField(blank=True, null=True)),
                ('srgb_range', models.PositiveIntegerField(blank=True, null=True)),
                ('node_sid_index', models.PositiveIntegerField(blank=True, null=True)),
                ('node_sid_label', models.PositiveIntegerField(blank=True, null=True)),
                (
                    'node_sid_v6_index',
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                (
                    'node_sid_v6_label',
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                (
                    'maximum_sid_depth',
                    models.PositiveSmallIntegerField(blank=True, null=True),
                ),
                (
                    'tunnel_table_pref',
                    models.PositiveSmallIntegerField(blank=True, null=True),
                ),
                (
                    'instance',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='segment_routing',
                        to='netbox_routing.isisinstance',
                    ),
                ),
                (
                    'owner',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to='users.owner',
                    ),
                ),
                (
                    'tags',
                    taggit.managers.TaggableManager(
                        through='extras.TaggedItem', to='extras.Tag'
                    ),
                ),
            ],
            options={
                'verbose_name': 'IS-IS Segment Routing',
                'verbose_name_plural': 'IS-IS Segment Routing',
                'ordering': ('instance',),
            },
            bases=(netbox.models.deletion.DeleteMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ISISInterfaceLevel',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                (
                    'custom_field_data',
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder,
                    ),
                ),
                ('description', models.CharField(blank=True, max_length=200)),
                ('comments', models.TextField(blank=True)),
                ('level', models.PositiveSmallIntegerField()),
                ('metric', models.PositiveIntegerField(blank=True, null=True)),
                ('hello_interval', models.PositiveIntegerField(blank=True, null=True)),
                (
                    'hello_multiplier',
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                ('priority', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('passive', models.BooleanField(blank=True, null=True)),
                (
                    'interface',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='levels',
                        to='netbox_routing.isisinterface',
                    ),
                ),
                (
                    'owner',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to='users.owner',
                    ),
                ),
                (
                    'tags',
                    taggit.managers.TaggableManager(
                        through='extras.TaggedItem', to='extras.Tag'
                    ),
                ),
            ],
            options={
                'verbose_name': 'IS-IS Interface Level',
                'ordering': ('interface', 'level'),
                'constraints': [
                    models.UniqueConstraint(
                        fields=('interface', 'level'),
                        name='netbox_routing_isisinterfacelevel_interface_level_unique',
                    )
                ],
            },
            bases=(netbox.models.deletion.DeleteMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ISISLevel',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                (
                    'custom_field_data',
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder,
                    ),
                ),
                ('description', models.CharField(blank=True, max_length=200)),
                ('comments', models.TextField(blank=True)),
                ('level', models.PositiveSmallIntegerField()),
                ('default_metric', models.PositiveIntegerField(blank=True, null=True)),
                ('wide_metrics_only', models.BooleanField(blank=True, null=True)),
                ('preference', models.PositiveSmallIntegerField(blank=True, null=True)),
                (
                    'labeled_preference',
                    models.PositiveSmallIntegerField(blank=True, null=True),
                ),
                ('disabled', models.BooleanField(blank=True, null=True)),
                ('auth_type', models.CharField(blank=True, default='', max_length=10)),
                ('auth_key', models.CharField(blank=True, default='', max_length=128)),
                (
                    'instance',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='levels',
                        to='netbox_routing.isisinstance',
                    ),
                ),
                (
                    'owner',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to='users.owner',
                    ),
                ),
                (
                    'tags',
                    taggit.managers.TaggableManager(
                        through='extras.TaggedItem', to='extras.Tag'
                    ),
                ),
            ],
            options={
                'verbose_name': 'IS-IS Level',
                'ordering': ('instance', 'level'),
                'constraints': [
                    models.UniqueConstraint(
                        fields=('instance', 'level'),
                        name='netbox_routing_isislevel_instance_level_unique',
                    )
                ],
            },
            bases=(netbox.models.deletion.DeleteMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ISISFlexAlgo',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                (
                    'custom_field_data',
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder,
                    ),
                ),
                ('description', models.CharField(blank=True, max_length=200)),
                ('comments', models.TextField(blank=True)),
                (
                    'algo_id',
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(128),
                            django.core.validators.MaxValueValidator(255),
                        ]
                    ),
                ),
                (
                    'metric_type',
                    models.CharField(blank=True, default='', max_length=40),
                ),
                ('priority', models.PositiveSmallIntegerField(blank=True, null=True)),
                (
                    'admin_group_exclude',
                    models.CharField(blank=True, default='', max_length=200),
                ),
                (
                    'admin_group_include_any',
                    models.CharField(blank=True, default='', max_length=200),
                ),
                (
                    'admin_group_include_all',
                    models.CharField(blank=True, default='', max_length=200),
                ),
                (
                    'instance',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='flex_algos',
                        to='netbox_routing.isisinstance',
                    ),
                ),
                (
                    'owner',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to='users.owner',
                    ),
                ),
                (
                    'tags',
                    taggit.managers.TaggableManager(
                        through='extras.TaggedItem', to='extras.Tag'
                    ),
                ),
            ],
            options={
                'verbose_name': 'IS-IS Flex-Algo',
                'ordering': ('instance', 'algo_id'),
                'constraints': [
                    models.UniqueConstraint(
                        fields=('instance', 'algo_id'),
                        name='netbox_routing_isisflexalgo_instance_algo_id_unique',
                    ),
                    models.CheckConstraint(
                        condition=models.Q(
                            ('algo_id__gte', 128), ('algo_id__lte', 255)
                        ),
                        name='netbox_routing_isisflexalgo_algo_id_range',
                    ),
                ],
            },
            bases=(netbox.models.deletion.DeleteMixin, models.Model),
        ),
    ]
