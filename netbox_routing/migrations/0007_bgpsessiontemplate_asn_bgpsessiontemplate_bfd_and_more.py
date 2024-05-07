# Generated by Django 4.2.4 on 2024-05-07 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ipam', '0069_gfk_indexes'),
        ('netbox_routing', '0006_bgp'),
    ]

    operations = [
        migrations.AddField(
            model_name='bgpsessiontemplate',
            name='asn',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='session_templates', to='ipam.asn'),
        ),
        migrations.AddField(
            model_name='bgpsessiontemplate',
            name='bfd',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='bgpsessiontemplate',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='netbox_routing.bgpsessiontemplate'),
        ),
        migrations.AddField(
            model_name='bgpsessiontemplate',
            name='password',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]