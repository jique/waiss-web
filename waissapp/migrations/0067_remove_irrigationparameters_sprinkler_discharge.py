# Generated by Django 3.0.8 on 2020-11-27 04:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('waissapp', '0066_auto_20201127_1135'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='irrigationparameters',
            name='sprinkler_discharge',
        ),
    ]
