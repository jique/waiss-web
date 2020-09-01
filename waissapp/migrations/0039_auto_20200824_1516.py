# Generated by Django 3.0.8 on 2020-08-24 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waissapp', '0038_auto_20200820_1644'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sensornumber',
            options={'get_latest_by': 'timestamp', 'verbose_name_plural': 'Site: Sensors'},
        ),
        migrations.RenameField(
            model_name='moisturecontent',
            old_name='sensor',
            new_name='data_storage',
        ),
        migrations.RemoveField(
            model_name='moisturecontent',
            name='farm_name',
        ),
        migrations.RemoveField(
            model_name='moisturecontent',
            name='soil_mc',
        ),
        migrations.RemoveField(
            model_name='sensornumber',
            name='farm_name',
        ),
        migrations.AddField(
            model_name='moisturecontent',
            name='raw_data',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Analog Reading'),
        ),
        migrations.AddField(
            model_name='moisturecontent',
            name='timestamp',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Time Measured'),
        ),
    ]
