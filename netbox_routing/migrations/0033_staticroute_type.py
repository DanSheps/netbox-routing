from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_routing', '0032_fix_eigrp_router_ordering'),
    ]

    operations = [
        migrations.AddField(
            model_name='staticroute',
            name='type',
            field=models.CharField(
                choices=[
                    ('unicast', 'Unicast'),
                    ('blackhole', 'Blackhole'),
                    ('unreachable', 'Unreachable'),
                ],
                default='unicast',
                max_length=20,
                verbose_name='Type',
            ),
        ),
    ]
