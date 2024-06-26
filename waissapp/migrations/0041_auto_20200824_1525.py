# Generated by Django 3.0.8 on 2020-08-24 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waissapp', '0040_auto_20200824_1520'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fieldunit',
            options={'ordering': ['timestamp'], 'verbose_name_plural': 'Site: Field Units'},
        ),
        migrations.AlterModelOptions(
            name='sensornumber',
            options={'verbose_name_plural': 'Site: Sensors'},
        ),
        migrations.RemoveField(
            model_name='sensornumber',
            name='timestamp',
        ),
        migrations.AddField(
            model_name='fieldunit',
            name='timestamp',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Time Measured'),
        ),
    ]
