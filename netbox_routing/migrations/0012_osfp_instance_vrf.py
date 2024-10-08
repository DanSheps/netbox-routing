# Generated by Django 5.0.8 on 2024-09-28 04:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipam', '0070_vlangroup_vlan_id_ranges'),
        ('netbox_routing', '0011_osfp_passive_interface'),
    ]

    operations = [
        migrations.AddField(
            model_name='ospfinstance',
            name='vrf',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='ospf_instances',
                to='ipam.vrf',
            ),
        ),
    ]
