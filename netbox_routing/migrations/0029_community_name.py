from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_routing', '0028_staticroute_interface_next_hop_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
