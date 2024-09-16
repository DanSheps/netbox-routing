# Generated by Django 5.0.8 on 2024-09-16 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_routing', '0008_convert_to_primarymodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staticroute',
            name='metric',
            field=models.PositiveSmallIntegerField(blank=True, default=1),
        ),
        migrations.AlterField(
            model_name='staticroute',
            name='permanent',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
