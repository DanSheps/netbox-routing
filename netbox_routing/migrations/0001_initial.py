# Generated by Django 4.0.3 on 2022-04-01 18:02

import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion
import ipam.fields
import netbox_routing.fields.ip
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ipam', '0057_created_datetimefield'),
        ('extras', '0072_created_datetimefield'),
        ('dcim', '0153_created_datetimefield'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrefixList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('name', models.CharField(max_length=255)),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RouteMap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('name', models.CharField(max_length=255)),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StaticRoute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('prefix', ipam.fields.IPNetworkField()),
                ('next_hop', netbox_routing.fields.ip.IPAddressField()),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('metric', models.PositiveSmallIntegerField()),
                ('permanent', models.BooleanField()),
                ('devices', models.ManyToManyField(related_name='static_routes', to='dcim.device')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
                ('vrf', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='staticroutes', to='ipam.vrf')),
            ],
        ),
        migrations.CreateModel(
            name='RouteMapEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('type', models.CharField(max_length=6)),
                ('sequence', models.PositiveSmallIntegerField()),
                ('route_map', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='entries', to='netbox_routing.routemap')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PrefixListEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('sequence', models.PositiveSmallIntegerField()),
                ('type', models.CharField(max_length=6)),
                ('prefix', ipam.fields.IPNetworkField()),
                ('ge', models.PositiveSmallIntegerField()),
                ('le', models.PositiveSmallIntegerField()),
                ('prefix_list', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='entries', to='netbox_routing.prefixlist')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddConstraint(
            model_name='staticroute',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('metric__lte', 255), ('metric__gte', 0))), name='metric_gte_lte'),
        ),
    ]