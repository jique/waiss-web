# Generated by Django 3.0.8 on 2020-12-03 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waissapp', '0068_auto_20201127_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='irrigationparameters',
            name='irrig',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Type'),
        ),
    ]
