# Generated by Django 3.0.8 on 2020-08-24 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waissapp', '0039_auto_20200824_1516'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moisturecontent',
            name='timestamp',
        ),
        migrations.AddField(
            model_name='sensornumber',
            name='timestamp',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Time Measured'),
        ),
    ]
