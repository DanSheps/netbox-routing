# Generated by Django 5.0.8 on 2024-09-27 13:00

import django.db.models.deletion
import netbox_routing.fields.ip
import taggit.managers
import utilities.json
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dcim', '0190_nested_modules'),
        ('extras', '0121_customfield_related_object_filter'),
        ('ipam', '0070_vlangroup_vlan_id_ranges'),
        ('netbox_routing', '0009_alter_staticroute_metric_alter_staticroute_permanent'),
    ]

    operations = [
        migrations.CreateModel(
            name='EIGRPAddressFamily',
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
                ('family', models.PositiveSmallIntegerField()),
                ('rid', netbox_routing.fields.ip.IPAddressField(blank=True, null=True)),
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
                        related_name='eigrp_address_families',
                        to='ipam.vrf',
                    ),
                ),
            ],
            options={
                'verbose_name': 'EIGRP Address Family',
            },
        ),
        migrations.CreateModel(
            name='EIGRPRouter',
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
                ('mode', models.CharField(max_length=10)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('pid', models.PositiveIntegerField(blank=True, null=True)),
                ('rid', netbox_routing.fields.ip.IPAddressField(blank=True, null=True)),
                (
                    'device',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='eigrp',
                        to='dcim.device',
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
                'verbose_name': 'EIGRP Router',
            },
        ),
        migrations.CreateModel(
            name='EIGRPNetwork',
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
                    'address_family',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to='netbox_routing.eigrpaddressfamily',
                    ),
                ),
                (
                    'network',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='eigrp',
                        to='ipam.prefix',
                    ),
                ),
                (
                    'tags',
                    taggit.managers.TaggableManager(
                        through='extras.TaggedItem', to='extras.Tag'
                    ),
                ),
                (
                    'router',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='netbox_routing.eigrprouter',
                    ),
                ),
            ],
            options={
                'verbose_name': 'EIGRP Network',
            },
        ),
        migrations.CreateModel(
            name='EIGRPInterface',
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
                ('passive', models.BooleanField()),
                ('bfd', models.BooleanField()),
                (
                    'authentication',
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ('passphrase', models.CharField(blank=True, max_length=200, null=True)),
                (
                    'address_family',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to='netbox_routing.eigrpaddressfamily',
                    ),
                ),
                (
                    'interface',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='eigrp',
                        to='dcim.interface',
                    ),
                ),
                (
                    'tags',
                    taggit.managers.TaggableManager(
                        through='extras.TaggedItem', to='extras.Tag'
                    ),
                ),
                (
                    'router',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='netbox_routing.eigrprouter',
                    ),
                ),
            ],
            options={
                'verbose_name': 'EIGRP Interface',
            },
        ),
        migrations.AddField(
            model_name='eigrpaddressfamily',
            name='router',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='netbox_routing.eigrprouter',
            ),
        ),
        migrations.AddConstraint(
            model_name='eigrpnetwork',
            constraint=models.UniqueConstraint(
                fields=('router', 'address_family', 'network'),
                name='netbox_routing_eigrpnetwork_unique_network',
            ),
        ),
        migrations.AddConstraint(
            model_name='eigrpinterface',
            constraint=models.UniqueConstraint(
                fields=('router', 'address_family', 'interface'),
                name='netbox_routing_eigrpinterface_unique_interface',
            ),
        ),
        migrations.AddConstraint(
            model_name='eigrpaddressfamily',
            constraint=models.UniqueConstraint(
                fields=('router', 'vrf', 'family'),
                name='netbox_routing_eigrpaddressfamily_unique_af',
            ),
        ),
    ]
